#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import re
import os
import unicodedata

RSS_MADRID = "https://www.aemet.es/documentos_d/eltiempo/prediccion/avisos/rss/CAP_AFAC72_RSS.xml"
NS = {"cap": "urn:oasis:names:tc:emergency:cap:1.2"}
OUTPUT_DIR = "_posts"   # Carpeta típica de Jekyll

# ---------------------------------------------------------
# DESCARGA
# ---------------------------------------------------------
def descargar(url):
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read()
    except Exception as e:
        print(f"❌ Error al descargar {url}: {e}")
        return None

# ---------------------------------------------------------
# LECTURA RSS
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# CAP
# ---------------------------------------------------------
def obtener_info_es(root):
    infos = root.findall("cap:info", NS)
    for info in infos:
        lang = info.find("cap:language", NS)
        if lang is not None and lang.text and lang.text.lower().startswith("es"):
            return info
    return None

# ---------------------------------------------------------
# GENERAR MARKDOWN JEKYLL
# ---------------------------------------------------------
def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text

def crear_post_markdown(titulo, inicio, fin, contenido):
    fecha = inicio.split("T")[0]  # AAAA-MM-DD
    slug = slugify(titulo)
    filename = f"{fecha}-{slug}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(filepath):
        print(f"ℹ️ El aviso '{titulo}' ya existe ({filename}). No se genera archivo.")
        return

    # Convertir fechas CAP (UTC) a formato Jekyll (+0100)
    def convertir_fecha(dt_str):
        try:
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
        except:
            return dt_str

    fecha_inicio_fmt = convertir_fecha(inicio)
    fecha_fin_fmt = convertir_fecha(fin)

    yaml = f"""---
layout: post
title: "{titulo}"
date: {fecha_inicio_fmt}
author: AEMET
published: true
expires: {fecha_fin_fmt}
categories:
  - Alerta metereológica
---
"""

    # Contenido final del post
    body = (
        contenido
        + "\n\n<br><small><i>Aviso generado automáticamente.</i></small>\n"
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(yaml + "\n" + body)

    print(f"✅ Generado fichero de aviso: {filename}")

# ---------------------------------------------------------
# FORMATEO DEL AVISO
# ---------------------------------------------------------
def formatear_aviso(info_es):
    def get(tag):
        el = info_es.find(f"cap:{tag}", NS)
        return el.text.strip() if el is not None and el.text else ""

    evento = get("event")
    inicio = get("onset")
    fin = get("expires")
    titular = get("headline")
    descripcion = get("description")
    instrucciones = get("instruction")

    area = info_es.find("cap:area/cap:areaDesc", NS)
    area = area.text.strip() if area is not None else "Zona no especificada"

    # Ignorar avisos de la Sierra de Madrid
    if "Sierra de Madrid" in area:
        return None

    # Ignorar avisos expirados
    try:
        expires_dt = datetime.fromisoformat(fin.replace("Z", "+00:00"))
        if expires_dt <= datetime.now(timezone.utc):
            return None
    except Exception:
        pass

    parametros = {
        p.find("cap:valueName", NS).text.strip(): p.find("cap:value", NS).text.strip()
        for p in info_es.findall("cap:parameter", NS)
        if p.find("cap:valueName", NS) is not None and p.find("cap:value", NS) is not None
    }

    nivel = parametros.get("AEMET-Meteoalerta nivel", "No especificado")
    prob = parametros.get("AEMET-Meteoalerta probabilidad", None)

    explicacion_nivel = {
        "amarillo": "Fenómeno no habitual. Riesgo bajo, pero se recomienda precaución.",
        "naranja": "Riesgo importante. Fenómenos adversos con impacto notable.",
        "rojo": "Riesgo extremo. Fenómeno meteorológico excepcional. Evite actividades al aire libre."
    }.get(nivel.lower(), "")

    texto = f"""
============================================================

       ⚠️ AVISO AUTOMATIZADO – AEMET
       
============================================================

🔔 *Fenómeno previsto:* {evento}

🗺️ *Zona afectada:* {area}

🟨 *Nivel de aviso:* {nivel.capitalize()}

{f"📊 *Probabilidad estimada:* {prob}" if prob else ""}


📆 *Periodo de validez:*

   • Inicio → {inicio}
   
   • Fin    → {fin}

📝 *Tipo:* {titular}

📄 *Descripción:*

{descripcion}

ℹ️ *Nivel de riesgo:*

{explicacion_nivel}

📌 *Recomendaciones oficiales:*

{instrucciones}

============================================================

Tenga en cuenta que puede suponer afectaciones al transporte. Planifique en consecuencia.
""".strip()

    return texto, titular, inicio, fin

# ---------------------------------------------------------
# PROCESAR AVISO INDIVIDUAL
# ---------------------------------------------------------
def procesar_aviso(url):
    xml_data = descargar(url)
    if not xml_data:
        return False

    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"❌ Error parseando CAP: {e}")
        return False

    info_es = obtener_info_es(root)
    if info_es is None:
        return False

    resultado = formatear_aviso(info_es)
    if not resultado:
        return False

    contenido, titulo, inicio, fin = resultado

    crear_post_markdown(titulo, inicio, fin, contenido)
    return True

# ---------------------------------------------------------
# PRINCIPAL
# ---------------------------------------------------------
def main():
    enlaces = leer_rss_madrid()
    if not enlaces:
        print("Consulta realizada: no hay alertas.")
        return

    generados = 0
    for url in enlaces:
        if procesar_aviso(url):
            generados += 1

    if generados == 0:
        print("Consulta realizada: no hay alertas nuevas.")

if __name__ == "__main__":
    main()
