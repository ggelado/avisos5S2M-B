#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import json

# -----------------------------
# CONFIG
# -----------------------------
RSS_MADRID = "https://www.aemet.es/documentos_d/eltiempo/prediccion/avisos/rss/CAP_AFAC72_RSS.xml"
NS = {"cap": "urn:oasis:names:tc:emergency:cap:1.2"}
DATA_DIR = "_data"
ALERTS_FILE = f"{DATA_DIR}/alerts.json"

# -----------------------------
# DESCARGA
# -----------------------------
def descargar(url):
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read()
    except Exception as e:
        print(f"❌ Error al descargar {url}: {e}")
        return None

# -----------------------------
# LECTURA RSS
# -----------------------------
def leer_rss_madrid():
    xml_data = descargar(RSS_MADRID)
    if not xml_data:
        return []

    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"❌ Error parseando RSS: {e}")
        return []

    items = root.findall("./channel/item")
    enlaces = []
    for item in items:
        link = item.find("link")
        if link is not None and link.text.endswith(".xml"):
            enlaces.append(link.text.strip())
    return enlaces

# -----------------------------
# CAP
# -----------------------------
def obtener_info_es(root):
    infos = root.findall("cap:info", NS)
    for info in infos:
        lang = info.find("cap:language", NS)
        if lang is not None and lang.text and lang.text.lower().startswith("es"):
            return info
    return None

# -----------------------------
# FORMATEO Y FILTRO DE AVISO
# -----------------------------
def formatear_aviso(info_es):
    def get(tag):
        el = info_es.find(f"cap:{tag}", NS)
        return el.text.strip() if el is not None and el.text else ""

    inicio = get("onset")
    fin = get("expires")

    # Ignorar avisos expirados
    try:
        expires_dt = datetime.fromisoformat(fin.replace("Z", "+00:00"))
        if expires_dt <= datetime.now(timezone.utc):
            return None
    except Exception:
        return None

    return {
        "event": get("event")
    }

# -----------------------------
# ACTUALIZAR JSON
# -----------------------------
def actualizar_alertas_json(alertas):
    import os
    os.makedirs(DATA_DIR, exist_ok=True)

    # Deduplicar por evento
    alertas_unicas = []
    vistos = set()
    for alerta in alertas:
        ev = alerta["event"]
        if ev not in vistos:
            vistos.add(ev)
            alertas_unicas.append(alerta)

    with open(ALERTS_FILE, "w", encoding="utf-8") as f:
        json.dump(alertas_unicas, f, ensure_ascii=False, indent=2)

    print(f"🔄 Actualizado {ALERTS_FILE} con {len(alertas_unicas)} alerta(s)")

# -----------------------------
# PROCESAR CADA AVISO
# -----------------------------
def procesar_aviso(url):
    xml_data = descargar(url)
    if not xml_data:
        return None

    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"❌ Error parseando CAP: {e}")
        return None

    info_es = obtener_info_es(root)
    if info_es is None:
        return None

    resultado = formatear_aviso(info_es)
    if not resultado:
        return None

    return resultado

# -----------------------------
# MAIN
# -----------------------------
def main():
    enlaces = leer_rss_madrid()
    alertas = []

    if not enlaces:
        print("Consulta realizada: no hay alertas.")
        actualizar_alertas_json([])
        return

    for url in enlaces:
        aviso = procesar_aviso(url)
        if aviso:
            alertas.append(aviso)

    actualizar_alertas_json(alertas)

if __name__ == "__main__":
    main()
