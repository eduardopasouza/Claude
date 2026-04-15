import httpx
import os

# URLs Públicas Conhecidas
SICAR_BASE_URL = "https://car.gov.br/publico/imoveis/index"
IBAMA_GEO_URL = "http://siscom.ibama.gov.br/geoserver/ows"

def verify_sicar_access():
    print("Testando acesso aos serviços base do SICAR...")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = httpx.get(SICAR_BASE_URL, headers=headers, timeout=15.0, verify=False)
        # 200 significa que o portal web está acessível.
        # Captchas são acionados ao fazer queries de download direto.
        if response.status_code == 200:
            print("✅ Portal Público do SICAR está ACESSÍVEL.")
            print("Status: Para consumo programático em massa, a leitura direta de SHP via bases estaduais ou uso do CAPTCHA bypasser (Playwright) será necessária.")
        else:
            print(f"❌ Portal do SICAR retornou: {response.status_code}")
    except Exception as e:
        print(f"❌ Falha ao acessar SICAR: {e}")

def verify_ibama_geoserver():
    print("\nTestando GeoServer do IBAMA (Áreas Embargadas Polígonos)...")
    url = f"https://siscom.ibama.gov.br/geoserver/ows?service=WFS&version=1.0.0&request=GetCapabilities"
    try:
        response = httpx.get(url, timeout=15.0, verify=False)
        if response.status_code == 200 and b"WFS_Capabilities" in response.content:
            print("✅ GeoServer do IBAMA está OPERACIONAL e respondendo WFS.")
        else:
            print(f"❌ Erro ou payload não-WFS. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Falha de rede para GeoServer IBAMA: {e}")

if __name__ == "__main__":
    verify_sicar_access()
    verify_ibama_geoserver()
