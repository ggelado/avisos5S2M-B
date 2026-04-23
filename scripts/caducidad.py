import json
import os
import re
from datetime import datetime

import pytz  # Para manejar zonas horarias
import yaml

# Carpeta donde están tus posts
POSTS_DIR = "_posts"
DATA_DIR = "_data"

# Patrón para capturar la línea de 'published' y 'expires'
PUBLISHED_RE = re.compile(r'^published:\s*(true|false)', re.IGNORECASE)
EXPIRES_RE = re.compile(r'^expires:\s*(.+)$', re.IGNORECASE)

# Hora actual con zona UTC (podemos compararla con la de los posts)
DATE_FORMAT_FULL = "%Y-%m-%d %H:%M:%S %z"
DATE_FORMAT_NO_SECONDS = "%Y-%m-%d %H:%M %z"
now = datetime.now(pytz.UTC)

# Lista para almacenar posts futuros
future_posts = []

for filename in os.listdir(POSTS_DIR):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(POSTS_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Parsear frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm_match:
        continue
    
    fm_text = fm_match.group(1)
    
    try:
        fm = yaml.safe_load(fm_text)
    except:
        continue
    
    lines = content.split('\n')

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
        lines[expires_line_idx] = f"expires: {normalized}"

    # Evaluar published
    if expires_dt and published_line_idx is not None:
        # Comparar la fecha de expiración con la fecha actual
        if expires_dt < now:
            # Cambiar published a false si es true
            if PUBLISHED_RE.match(lines[published_line_idx]).group(1).lower() == "true":
                lines[published_line_idx] = "published: false"
                published_changed = True

    # Escribir SOLO si hubo cambios reales
    if expires_needs_normalization or published_changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))
        print(f"{filename} actualizado")

    # Detectar posts futuros
    if 'date' in fm:
        post_date = fm['date']
        if isinstance(post_date, str):
            try:
                post_date = datetime.strptime(post_date, DATE_FORMAT_FULL)
            except ValueError:
                try:
                    post_date = datetime.strptime(post_date, DATE_FORMAT_NO_SECONDS)
                except ValueError:
                    continue
        
        # Si es naive (sin zona horaria), asumir zona de Madrid
        if post_date.tzinfo is None:
            madrid_tz = pytz.timezone('Europe/Madrid')
            post_date = madrid_tz.localize(post_date)
        
        if post_date > now:
            expires_str = fm.get('expires', '')
            future_posts.append({
                'title': fm.get('title', 'Untitled'),
                'date': post_date.isoformat(),
                'excerpt': fm.get('excerpt', ''),
                'expires': expires_str,
            })

# Guardar future_posts en JSON
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Ordenar future_posts por fecha cronológicamente
future_posts.sort(key=lambda x: x['date'])

with open(os.path.join(DATA_DIR, 'future_posts.json'), 'w', encoding='utf-8') as f:
    json.dump(future_posts, f, ensure_ascii=False, indent=2)

print("Fin comprobación caducidades")
print(f"Posts futuros: {len(future_posts)}")

