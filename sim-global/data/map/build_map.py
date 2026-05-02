"""Generates world-political.svg and countries.json from Natural Earth GeoJSON.

Inputs:
  /home/user/Claude/sim-global/data/map/world-110m.geojson  (used for SVG paths)
  /home/user/Claude/sim-global/data/map/world-50m.geojson   (used to enrich countries.json
                                                             so it has >= 200 entries)

Outputs:
  /home/user/Claude/sim-global/data/map/world-political.svg
  /home/user/Claude/sim-global/data/map/countries.json

Projection: equirectangular into a 1000x500 canvas.
  x = (lon + 180) / 360 * 1000
  y = (90 - lat) / 180 * 500
"""

import json
import os
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.abspath(__file__))
GEO_110 = os.path.join(BASE, "world-110m.geojson")
GEO_50 = os.path.join(BASE, "world-50m.geojson")
SVG_OUT = os.path.join(BASE, "world-political.svg")
JSON_OUT = os.path.join(BASE, "countries.json")

# Portuguese names for game-relevant countries.
NAME_PT = {
    "BRA": "Brasil",
    "ARG": "Argentina",
    "URY": "Uruguai",
    "PRY": "Paraguai",
    "CHL": "Chile",
    "BOL": "Bolívia",
    "PER": "Peru",
    "COL": "Colômbia",
    "VEN": "Venezuela",
    "ECU": "Equador",
    "GUY": "Guiana",
    "SUR": "Suriname",
    "MEX": "México",
    "USA": "Estados Unidos",
    "CAN": "Canadá",
    "GBR": "Reino Unido",
    "IRL": "Irlanda",
    "FRA": "França",
    "DEU": "Alemanha",
    "ITA": "Itália",
    "ESP": "Espanha",
    "PRT": "Portugal",
    "NLD": "Países Baixos",
    "BEL": "Bélgica",
    "CHE": "Suíça",
    "AUT": "Áustria",
    "POL": "Polônia",
    "RUS": "Rússia",
    "TUR": "Turquia",
    "EGY": "Egito",
    "ZAF": "África do Sul",
    "MAR": "Marrocos",
    "DZA": "Argélia",
    "JPN": "Japão",
    "CHN": "China",
    "KOR": "Coreia do Sul",
    "PRK": "Coreia do Norte",
    "IND": "Índia",
    "AUS": "Austrália",
    "NZL": "Nova Zelândia",
    # extras
    "GRC": "Grécia",
    "SWE": "Suécia",
    "NOR": "Noruega",
    "FIN": "Finlândia",
    "DNK": "Dinamarca",
    "ISL": "Islândia",
    "CZE": "República Tcheca",
    "HUN": "Hungria",
    "ROU": "Romênia",
    "UKR": "Ucrânia",
    "IRN": "Irã",
    "IRQ": "Iraque",
    "SAU": "Arábia Saudita",
    "ISR": "Israel",
    "SYR": "Síria",
    "AFG": "Afeganistão",
    "PAK": "Paquistão",
    "BGD": "Bangladesh",
    "THA": "Tailândia",
    "VNM": "Vietnã",
    "IDN": "Indonésia",
    "PHL": "Filipinas",
    "MYS": "Malásia",
    "SGP": "Singapura",
    "KEN": "Quênia",
    "NGA": "Nigéria",
    "ETH": "Etiópia",
    "CUB": "Cuba",
    "DOM": "República Dominicana",
    "HTI": "Haiti",
    "JAM": "Jamaica",
    "PAN": "Panamá",
    "CRI": "Costa Rica",
}


def project(lon, lat):
    x = (lon + 180.0) / 360.0 * 1000.0
    y = (90.0 - lat) / 180.0 * 500.0
    return x, y


def ring_to_path(ring):
    """ring is a list of [lon,lat] coords. Returns 'M x,y L x,y ... Z'"""
    parts = []
    for i, pt in enumerate(ring):
        x, y = project(pt[0], pt[1])
        cmd = "M" if i == 0 else "L"
        parts.append(f"{cmd}{x:.2f},{y:.2f}")
    parts.append("Z")
    return "".join(parts)


def feature_to_path_d(geom):
    """Geometry -> SVG path 'd' attribute (string)."""
    t = geom["type"]
    coords = geom["coordinates"]
    parts = []
    if t == "Polygon":
        for ring in coords:
            parts.append(ring_to_path(ring))
    elif t == "MultiPolygon":
        for poly in coords:
            for ring in poly:
                parts.append(ring_to_path(ring))
    else:
        return ""
    return " ".join(parts)


def _ring_bbox(ring):
    min_lon = min(p[0] for p in ring)
    max_lon = max(p[0] for p in ring)
    min_lat = min(p[1] for p in ring)
    max_lat = max(p[1] for p in ring)
    return min_lon, min_lat, max_lon, max_lat


def _ring_area(ring):
    """Crude planar area for ranking ring sizes (degrees^2)."""
    n = len(ring)
    if n < 3:
        return 0.0
    s = 0.0
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        s += (x2 - x1) * (y2 + y1)
    return abs(s) / 2.0


def bbox_centroid(geom):
    """Return [lon, lat] centroid of the LARGEST outer ring.

    Using the largest ring avoids antimeridian-spanning bbox issues
    (e.g., USA + Aleutian islands giving a centroid in the Atlantic).
    """
    t = geom["type"]
    coords = geom["coordinates"]
    rings = []
    if t == "Polygon":
        if coords:
            rings.append(coords[0])
    elif t == "MultiPolygon":
        for poly in coords:
            if poly:
                rings.append(poly[0])
    else:
        return None
    if not rings:
        return None
    biggest = max(rings, key=_ring_area)
    min_lon, min_lat, max_lon, max_lat = _ring_bbox(biggest)
    return [round((min_lon + max_lon) / 2.0, 2), round((min_lat + max_lat) / 2.0, 2)]


def pick_iso3(props):
    """Pick best ISO3 code. ISO_A3 may be '-99' for disputed; fall back to ADM0_A3."""
    iso = props.get("ISO_A3")
    if iso and iso != "-99":
        return iso
    a3 = props.get("ADM0_A3")
    if a3 and a3 != "-99":
        return a3
    return None


def pick_name(props):
    return (
        props.get("NAME_EN")
        or props.get("NAME_LONG")
        or props.get("NAME")
        or props.get("ADMIN")
        or "Unknown"
    )


def build_svg():
    with open(GEO_110) as f:
        gj = json.load(f)
    paths_xml = []
    seen_ids = set()
    for ft in gj["features"]:
        props = ft["properties"]
        iso = pick_iso3(props)
        name = pick_name(props)
        if not iso:
            iso = (props.get("ADMIN") or "X")[:3].upper()
        # Avoid duplicate ids
        original = iso
        suffix = 1
        while iso in seen_ids:
            suffix += 1
            iso = f"{original}{suffix}"
        seen_ids.add(iso)
        d = feature_to_path_d(ft["geometry"])
        if not d:
            continue
        name_pt = NAME_PT.get(original)
        attrs = [
            f'id="{escape(iso)}"',
            f'data-name="{escape(name)}"',
        ]
        if name_pt:
            attrs.append(f'data-name-pt="{escape(name_pt)}"')
        attrs.append(f'd="{d}"')
        paths_xml.append(f"<path {' '.join(attrs)}/>")
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" '
        'preserveAspectRatio="xMidYMid meet">\n'
        '<rect width="1000" height="500" fill="#0a0a0a"/>\n'
        '<g fill="#444" stroke="#222" stroke-width="0.5" '
        'stroke-linejoin="round" stroke-linecap="round">\n'
        + "\n".join(paths_xml)
        + "\n</g>\n</svg>\n"
    )
    with open(SVG_OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    return len(paths_xml)


def build_countries_json():
    """Use the 50m dataset for richer coverage if available, fall back to 110m."""
    src = GEO_50 if os.path.exists(GEO_50) else GEO_110
    with open(src) as f:
        gj = json.load(f)
    out = []
    seen = set()
    for ft in gj["features"]:
        props = ft["properties"]
        iso = pick_iso3(props)
        if not iso:
            continue
        if iso in seen:
            continue
        seen.add(iso)
        name = pick_name(props)
        centroid = bbox_centroid(ft["geometry"])
        out.append(
            {
                "iso3": iso,
                "name": name,
                "name_pt": NAME_PT.get(iso),
                "centroid": centroid,
            }
        )
    out.sort(key=lambda r: r["iso3"])
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return out


if __name__ == "__main__":
    n_paths = build_svg()
    countries = build_countries_json()
    translated = sum(1 for c in countries if c["name_pt"])
    print(f"SVG paths emitted: {n_paths}")
    print(f"countries.json entries: {len(countries)}")
    print(f"Translated names_pt: {translated}")
    print(f"SVG size: {os.path.getsize(SVG_OUT) / 1024:.1f} KB")
