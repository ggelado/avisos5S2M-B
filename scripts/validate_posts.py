#!/usr/bin/env python3
"""Validador de metadatos YAML para avisos de _posts/.

Uso:
    python scripts/validate_posts.py                   # valida todos los posts
    python scripts/validate_posts.py _posts/file.md …  # valida archivos concretos

Códigos de salida:
    0  Todos los archivos son válidos.
    1  Al menos un archivo contiene errores de validación.
"""

import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

POSTS_DIR = Path("_posts")

# Campos obligatorios que deben aparecer en el front matter de todo aviso.
REQUIRED_FIELDS = ("layout", "title", "date", "author", "published")

# Campos que se recomienda incluir pero cuya ausencia sólo genera advertencia.
RECOMMENDED_FIELDS = ("expires",)

# Patrón esperado para el nombre del archivo Jekyll.
FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")

# Formatos de fecha aceptados en el front matter.
DATE_FORMATS = (
    "%Y-%m-%d %H:%M:%S %z",
    "%Y-%m-%d %H:%M %z",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_date(value) -> datetime | None:
    """Convierte un valor de front matter a ``datetime``.

    Acepta objetos ``datetime``/``date`` (producidos por PyYAML) y cadenas
    en los formatos habituales de Jekyll.

    Returns:
        Un objeto ``datetime`` o ``None`` si el valor no puede parsearse.
    """
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    raw = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def extract_frontmatter(filepath: Path) -> dict | None:
    """Lee y parsea el front matter YAML de un archivo Markdown.

    Returns:
        El front matter como diccionario, o ``None`` si no se encuentra o
        no puede parsearse.
    """
    content = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML inválido: {exc}") from exc


# ---------------------------------------------------------------------------
# Reglas de validación
# ---------------------------------------------------------------------------


def validate_file(filepath: Path) -> tuple[list[str], list[str]]:
    """Valida los metadatos de un único post.

    Returns:
        Una tupla ``(errors, warnings)`` con los mensajes encontrados.
    """
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Nombre de archivo
    if not FILENAME_RE.match(filepath.name):
        errors.append(
            f"El nombre de archivo no sigue el formato Jekyll "
            f"'YYYY-MM-DD-slug.md': {filepath.name!r}"
        )

    # 2. Front matter presente y parseable
    try:
        fm = extract_frontmatter(filepath)
    except ValueError as exc:
        errors.append(str(exc))
        return errors, warnings

    if fm is None:
        errors.append("No se encontró front matter YAML (falta el bloque '---').")
        return errors, warnings

    # 3. Campos obligatorios
    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"Campo obligatorio ausente: '{field}'.")
        elif fm[field] is None or (isinstance(fm[field], str) and not fm[field].strip()):
            errors.append(f"Campo obligatorio vacío: '{field}'.")

    # 4. Campos recomendados
    for field in RECOMMENDED_FIELDS:
        if field not in fm:
            warnings.append(f"Campo recomendado ausente: '{field}'.")

    # 5. layout debe ser "post"
    if fm.get("layout") not in (None, "post"):
        errors.append(
            f"El campo 'layout' debe ser 'post', se encontró: {fm['layout']!r}."
        )

    # 6. published debe ser booleano
    if "published" in fm and not isinstance(fm["published"], bool):
        errors.append(
            f"El campo 'published' debe ser true/false (booleano), "
            f"se encontró: {fm['published']!r}."
        )

    # 7. date debe ser una fecha válida
    dt_date = None
    if "date" in fm and fm["date"] is not None:
        dt_date = parse_date(fm["date"])
        if dt_date is None:
            errors.append(f"El campo 'date' no tiene un formato de fecha reconocido: {fm['date']!r}.")

    # 8. expires debe ser una fecha válida y >= date
    if "expires" in fm and fm["expires"] is not None:
        dt_expires = parse_date(fm["expires"])
        if dt_expires is None:
            errors.append(
                f"El campo 'expires' no tiene un formato de fecha reconocido: {fm['expires']!r}."
            )
        elif dt_date is not None:
            # Comparar sin zona horaria para evitar errores de offset-naive vs aware
            naive_exp = dt_expires.replace(tzinfo=None)
            naive_date = dt_date.replace(tzinfo=None)
            if naive_exp < naive_date:
                errors.append(
                    f"El campo 'expires' ({fm['expires']}) es anterior a 'date' ({fm['date']})."
                )

    # 9. event_date debe ser una fecha válida
    if "event_date" in fm and fm["event_date"] is not None:
        if parse_date(fm["event_date"]) is None:
            errors.append(
                f"El campo 'event_date' no tiene un formato de fecha reconocido: {fm['event_date']!r}."
            )

    # 10. categories y tags deben ser listas
    for field in ("categories", "tags"):
        value = fm.get(field)
        if value is not None and not isinstance(value, list):
            errors.append(
                f"El campo '{field}' debe ser una lista (se encontró {type(value).__name__})."
            )

    return errors, warnings


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Ejecuta la validación y devuelve el código de salida.

    Args:
        argv: Lista de rutas a validar. Si es ``None`` o está vacía se
              validan todos los archivos en ``_posts/``.

    Returns:
        ``0`` si no hay errores, ``1`` en caso contrario.
    """
    if argv:
        files = [Path(p) for p in argv]
    else:
        if not POSTS_DIR.is_dir():
            print(f"❌ No se encontró el directorio {POSTS_DIR}/", file=sys.stderr)
            return 1
        files = sorted(POSTS_DIR.glob("*.md"))

    if not files:
        print("ℹ️  No se encontraron archivos para validar.")
        return 0

    total_errors = 0
    total_warnings = 0

    for filepath in files:
        errs, warns = validate_file(filepath)
        total_errors += len(errs)
        total_warnings += len(warns)

        if errs or warns:
            print(f"\n📄 {filepath}")
            for msg in errs:
                print(f"  ❌ ERROR   {msg}")
            for msg in warns:
                print(f"  ⚠️  AVISO  {msg}")

    print()
    if total_errors == 0 and total_warnings == 0:
        print(f"✅ {len(files)} archivo(s) validado(s) sin problemas.")
    else:
        print(
            f"{'❌' if total_errors else '⚠️ '} "
            f"{len(files)} archivo(s) validado(s): "
            f"{total_errors} error(es), {total_warnings} advertencia(s)."
        )

    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
