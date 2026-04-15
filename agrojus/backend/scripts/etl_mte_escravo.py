import os
import httpx
import pdfplumber
import logging
from datetime import datetime, timezone

from app.models.database import get_session, EnvironmentalAlert

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# URL comum do repositório da união (Atualizada Semestralmente)
# Nota: Muitas vezes a URL muda, usaremos uma fallback ou faremos download manual se falhar
MTE_PDF_URL = "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/areas-de-atuacao/cadastro_de_empregadores.pdf"
DATA_DIR = "/app/data"
PDF_PATH = os.path.join(DATA_DIR, "mte_trabalho_escravo.pdf")

def fetch_pdf():
    os.makedirs(DATA_DIR, exist_ok=True)
    logger.info(f"Baixando Cadastro de Empregadores MTE de {MTE_PDF_URL}...")
    try:
        response = httpx.get(MTE_PDF_URL, timeout=30.0, follow_redirects=True, verify=False)
        response.raise_for_status()
        with open(PDF_PATH, 'wb') as f:
            f.write(response.content)
        logger.info("PDF baixado com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao baixar PDF MTE: {e}")
        return False

def parse_pdf_and_insert():
    if not os.path.exists(PDF_PATH):
        logger.error("PDF não encontrado.")
        return
        
    db = get_session()
    
    # Limpa dados antigos da fonte MTE
    deleted = db.query(EnvironmentalAlert).filter(
        EnvironmentalAlert.source == "MTE"
    ).delete()
    logger.info(f"{deleted} registros antigos do MTE apagados.")
    
    count = 0
    logger.info("Iniciando extração de Tabelas via PDFPlumber...")
    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                # O PDF do governo geralmente tem um cabeçalho repetido.
                # Ex de colunas: 0=Empregador, 1=Nome Fantasia/Fazenda, 2=CNPJ/CPF, 3=Empregados, 4=Município, 5=UF...
                for row_idx, row in enumerate(table): # iterando pelas linhas
                    # Ignora a primeira linha se for cabeçalho
                    if row_idx == 0 and ("EMPREGADOR" in str(row[0]).upper() or "CPF" in str(row).upper()):
                        continue
                        
                    if not row or len(row) < 5:
                        continue
                        
                    # Limpeza das células (Linebreaks do PDF)
                    cleaned_row = [str(cell).replace('\n', ' ').strip() if cell else "" for cell in row]
                    
                    empregador = cleaned_row[0]
                    fazenda = cleaned_row[1]
                    cpf_cnpj = cleaned_row[2]
                    
                    # Evitar linhas de sumário ou sujeiras do PDF
                    if not cpf_cnpj or len(cpf_cnpj) < 11:
                        continue
                        
                    cpf_cnpj_clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
                    
                    municipio = cleaned_row[4] if len(cleaned_row) > 4 else ""
                    uf = cleaned_row[5] if len(cleaned_row) > 5 else ""
                    trabalhadores = cleaned_row[3] if len(cleaned_row) > 3 else "N/A"
                    
                    raw_data = {
                        "EMPREGADOR": empregador,
                        "ESTABELECIMENTO": fazenda,
                        "CPF_CNPJ": cpf_cnpj,
                        "TRABALHADORES": trabalhadores,
                        "MUNICIPIO": municipio,
                        "UF": uf
                    }
                    
                    desc = f"Trabalho Análogo à Escravidão - {empregador} ({fazenda}) - Trabalhadores resgatados: {trabalhadores} - {municipio}/{uf}"
                    
                    record = EnvironmentalAlert(
                        property_car_code="N/A", # MTE nao tem CAR atrelado, cruzamos pelo Documento
                        cpf_cnpj=cpf_cnpj_clean,
                        alert_type="trabalho_escravo",
                        source="MTE",
                        description=desc,
                        raw_data=raw_data,
                        created_at=datetime.now(timezone.utc),
                    )
                    db.add(record)
                    count += 1
            
            logger.info(f"Página {page_num + 1}/{len(pdf.pages)} processada.")
            
    db.commit()
    db.close()
    logger.info(f"✔ Sucesso! {count} CNPJs/CPFs indexados com violação de Direitos Humanos e Trabalhistas.")

if __name__ == '__main__':
    if fetch_pdf():
        parse_pdf_and_insert()
