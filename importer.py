import feedparser
import frontmatter
from datetime import datetime
import os
import re
import unicodedata

def slugify(text):
    # Quitar saltos de línea y espacios extra
    text = text.replace("\n", " ").replace("\r", " ").strip()

    # Quitar acentos
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    # Minúsculas
    text = text.lower()

    # Reemplazar cualquier cosa que no sea letra, número o guion
    text = re.sub(r"[^a-z0-9\-]+", "-", text)

    # Quitar guiones duplicados
    text = re.sub(r"-+", "-", text).strip("-")

    return text


RSS_URL = "https://fi.upm.es/GestorTablon/rss2b.php?idioma=castellano&tipogt=1,3"
OUTPUT_DIR = "jekyll_posts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

feed = feedparser.parse(RSS_URL)

for entry in feed.entries:
    # Metadata para Jekyll
    metadata = {
        "title": entry.title,
        "date": datetime(*entry.published_parsed[:6]).isoformat(),
        "layout": "post",
        "categories": [tag.term for tag in entry.tags] if 'tags' in entry else [],
        "author": entry.author if 'author' in entry else "Desconocido"  # <- aquí se añade el autor
    }

    # Contenido del post
    content = entry.summary  # o entry.content[0].value si existe contenido completo

    # Convertir a Markdown con frontmatter
    md = frontmatter.dumps(frontmatter.Post(content, **metadata))

    # Crear nombre de archivo tipo Jekyll: YYYY-MM-DD-titulo.md
    slug = slugify(entry.title)
    date_str = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Guardar archivo Markdown
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Guardado: {filepath}")
