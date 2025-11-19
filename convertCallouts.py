import re
from pathlib import Path

# Mapeo Obsidian -> Include Jekyll
include_map = {
    "note": "note",
    "info": "note",
    "tip": "tip",
    "todo": "tip",
    "warning": "warning",
    "caution": "warning",
    "danger": "important",
    "bug": "important",
    "quote": "note",
}

CALL_RE = re.compile(
    r"^> *\[\!(\w+)\] *([^\n]*)\n((^>.*\n?)*)",
    re.MULTILINE
)

CLEAN_RE = re.compile(r"^> ?", re.MULTILINE)


def convert_callouts(text):

    def build_html(tipo, title, body):
        include = include_map.get(tipo, "note")

        # limpiar >
        body = CLEAN_RE.sub("", body).strip()

        # Juntamos todo en un único bloque
        full_content = body if not title else f"**{title}**\n\n{body}"

        # Escape para comillas dobles
        full_content = full_content.replace('"', '&quot;')

        return f'{{% include {include}.html content="{full_content}" %}}\n'

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
