import re
from pathlib import Path

# Mapeo Obsidian -> Clase CSS
mapping = {
    "note": "note",
    "info": "info",
    "tip": "tip",
    "todo": "tip",
    "warning": "warning",
    "caution": "warning",
    "danger": "danger",
    "bug": "danger",
    "quote": "quote",
}

# Regex callout multilinea
CALL_RE = re.compile(
    r"^> *\[\!(\w+)\] *([^\n]*)\n((^>.*\n?)*)",
    re.MULTILINE
)

# Limpia ">"
CLEAN_RE = re.compile(r"^> ?", re.MULTILINE)


def convert_callouts(text):

    def build_html(tipo, title, body):
        css = mapping.get(tipo, "info")

        # limpiar >
        body = CLEAN_RE.sub("", body)

        # dividir en párrafos
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]

        html = [f'<div class="notice {css}">']

        if title:
            html.append(f'  <h4>{title}</h4>')

        for p in paragraphs:
            html.append(f'  <p>{p}</p>')

        html.append('</div>\n')

        return "\n".join(html)

    def repl(match):
        tipo = match.group(1).lower()
        title = match.group(2).strip()
        body = match.group(3)

        return build_html(tipo, title, body)

    return CALL_RE.sub(repl, text)


def process_posts():
    posts = Path("_posts").glob("**/*")

    for file in posts:
        if file.suffix.lower() not in {".md", ".markdown"}:
            continue

        original = file.read_text(encoding="utf-8")
        converted = convert_callouts(original)

        if converted != original:
            file.write_text(converted, encoding="utf-8")
            print(f"Convertido: {file}")
        else:
            print(f"Sin cambios: {file}")


if __name__ == "__main__":
    process_posts()
    print("\nHecho.")
