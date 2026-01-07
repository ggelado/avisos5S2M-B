import os
import re
from datetime import datetime
import pytz  # Para manejar zonas horarias

# Carpeta donde están tus posts
POSTS_DIR = "_posts"

# Patrón para capturar la línea de 'published' y 'expires'
PUBLISHED_RE = re.compile(r'^published:\s*(true|false)', re.IGNORECASE)
EXPIRES_RE = re.compile(r'^expires:\s*(.+)$', re.IGNORECASE)

# Hora actual con zona UTC (podemos compararla con la de los posts)
DATE_FORMAT_FULL = "%Y-%m-%d %H:%M:%S %z"
DATE_FORMAT_NO_SECONDS = "%Y-%m-%d %H:%M %z"
now = datetime.now(pytz.UTC)

for filename in os.listdir(POSTS_DIR):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(POSTS_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    expires_line_idx = None
    published_line_idx = None
    expires_dt = None

    expires_needs_normalization = False
    published_changed = False

    for i, line in enumerate(lines):
        m_exp = EXPIRES_RE.match(line)
        if m_exp:
            expires_line_idx = i
            expires_str = m_exp.group(1).strip()

            try:
                expires_dt = datetime.strptime(expires_str, DATE_FORMAT_FULL)
            except ValueError:
                try:
                    expires_dt = datetime.strptime(expires_str, DATE_FORMAT_NO_SECONDS)
                    expires_needs_normalization = True
                except ValueError:
                    expires_dt = None

        elif PUBLISHED_RE.match(line):
            published_line_idx = i

    # Normalizar expires SOLO si faltaban segundos
    if expires_needs_normalization and expires_dt and expires_line_idx is not None:
        normalized = expires_dt.strftime(DATE_FORMAT_FULL)
        lines[expires_line_idx] = f"expires: {normalized}\n"

    # Evaluar published
    if expires_dt and published_line_idx is not None:
        # Comparar la fecha de expiración con la fecha actual
        if expires_dt < now:
            # Cambiar published a false si es true
            if PUBLISHED_RE.match(lines[published_line_idx]).group(1).lower() == "true":
                lines[published_line_idx] = "published: false\n"
                published_changed = True

    # Escribir SOLO si hubo cambios reales
    if expires_needs_normalization or published_changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"{filename} actualizado")

print("Fin comprobación caducidades")
