import os
import yaml
from datetime import datetime, timezone

# Carpeta de posts y salida del ICS
POSTS_DIR = "_posts"
OUTPUT_DIR = "assets"
OUTPUT_FILE = "avisos.ics"
PERMALINK = "/avisos.ics"

DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S %z",
    "%Y-%m-%d %H:%M %z",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",  # ← faltaba este formato común en Jekyll
]

def read_frontmatter(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    parts = content.split("---")
    if len(parts) >= 3:
        try:
            return yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            print(f"Error leyendo YAML en {filepath}: {e}")
    return None

def parse_datetime(value):
    # Jekyll/PyYAML puede devolver ya un objeto date o datetime
    if isinstance(value, datetime):
        return value
    if hasattr(value, "timetuple"):  # date sin hora
        return datetime(value.year, value.month, value.day)
    dt_str = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"No se pudo parsear la fecha: {dt_str!r}")

def format_datetime(dt):
    """Devuelve la fecha en UTC formateada para iCal."""
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt.strftime("%Y%m%dT%H%M%S")

def escape_ical(text):
    """Escapa caracteres especiales según RFC 5545."""
    text = str(text)
    text = text.replace("\\", "\\\\")
    text = text.replace(";", "\\;")
    text = text.replace(",", "\\,")
    text = text.replace("\n", "\\n")
    return text

def fold_line(line):
    """Divide líneas largas según RFC 5545 (máx 75 octetos)."""
    result = []
    while len(line.encode("utf-8")) > 75:
        result.append(line[:75])
        line = " " + line[75:]
    result.append(line)
    return "\r\n".join(result)

os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

events = []

for filename in sorted(os.listdir(POSTS_DIR)):  # sorted para orden determinista
    if not filename.endswith(".md"):
        continue
    filepath = os.path.join(POSTS_DIR, filename)
    fm = read_frontmatter(filepath)
    if not fm:
        continue
    # Saltar posts no publicados (ausente también se considera no publicado)
    if not fm.get("published", False):
        continue

    title = escape_ical(fm.get("title", "Sin título"))
    description = escape_ical(fm.get("excerpt", ""))

    start_val = fm.get("event_date") or fm.get("date")
    if not start_val:
        print(f"Sin fecha en {filename}, omitido.")
        continue

    try:
        dt_start = parse_datetime(start_val)
    except ValueError as e:
        print(f"Error de fecha en {filename}: {e}")
        continue

    end_val = fm.get("expires")
    if end_val:
        try:
            dt_end = parse_datetime(end_val)
        except ValueError as e:
            print(f"Error en 'expires' de {filename}: {e}")
            dt_end = dt_start
    else:
        dt_end = dt_start

    # UID estable basado en el nombre del archivo, no en timestamp
    uid = f"{filename}@avisos.com"

    now_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VEVENT",
        fold_line(f"UID:{uid}"),
        fold_line(f"DTSTAMP:{now_utc}"),
        fold_line(f"DTSTART:{format_datetime(dt_start)}Z"),
        fold_line(f"DTEND:{format_datetime(dt_end)}Z"),
        fold_line(f"SUMMARY:{title}"),
        fold_line(f"DESCRIPTION:{description}"),
        "END:VEVENT",
    ]
    events.append("\r\n".join(lines))

with open(output_path, "w", encoding="utf-8", newline="") as f:
    f.write("---\n")
    f.write("layout: null\n")
    f.write(f"permalink: {PERMALINK}\n")
    f.write("---\n\n")
    # iCal usa CRLF según RFC 5545
    f.write("BEGIN:VCALENDAR\r\n")
    f.write("VERSION:2.0\r\n")
    f.write("PRODID:-//Avisos//ggelado//ES\r\n")
    f.write("CALSCALE:GREGORIAN\r\n")
    f.write("\r\n".join(events))
    f.write("\r\nEND:VCALENDAR\r\n")

print(f"Archivo iCal generado con {len(events)} evento(s): {output_path}")