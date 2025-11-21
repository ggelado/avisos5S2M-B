import os
import re
from datetime import datetime
import pytz  # Para manejar zonas horarias

# Carpeta donde están tus posts
POSTS_DIR = "_posts"

# Patrón para capturar la línea de 'published' y 'expires'
PUBLISHED_RE = re.compile(r'^published:\s*(true|false)', re.IGNORECASE)
EXPIRES_RE = re.compile(r'^expires:\s*(.+)$', re.IGNORECASE)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %z"

# Hora actual con zona UTC (podemos compararla con la de los posts)
now = datetime.now(pytz.UTC)

for filename in os.listdir(POSTS_DIR):
    filepath = os.path.join(POSTS_DIR, filename)
    
    if not filename.endswith(".md"):
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    expires_line_idx = None
    published_line_idx = None
    expires_dt = None
    
    for i, line in enumerate(lines):
        if EXPIRES_RE.match(line):
            expires_line_idx = i
            expires_str = EXPIRES_RE.match(line).group(1).strip()
            expires_dt = datetime.strptime(expires_str, DATE_FORMAT)
        elif PUBLISHED_RE.match(line):
            published_line_idx = i
    
    if expires_dt and published_line_idx is not None:
        # Comparar la fecha de expiración con la fecha actual
        if expires_dt < now:
            # Cambiar published a false si es true
            if PUBLISHED_RE.match(lines[published_line_idx]).group(1).lower() == "true":
                lines[published_line_idx] = "published: false\n"
                with open(filepath, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                print(f"{filename} actualizado a published: false")

print("Fin comprobación caducidades")
