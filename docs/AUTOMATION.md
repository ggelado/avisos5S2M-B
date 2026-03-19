# Guía de automatización

Este documento describe en detalle cómo funcionan los scripts de automatización del proyecto, cómo ejecutarlos y cómo mantenerlos.

---

## Instalación de dependencias

Todos los scripts dependen de las librerías definidas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

| Dependencia | Versión | Uso |
|---|---|---|
| `feedparser` | ≥ 6.0 | Parseo de feeds RSS/Atom (importer.py) |
| `python-frontmatter` | ≥ 1.1 | Lectura y escritura de front matter YAML |
| `PyYAML` | ≥ 6.0 | Parseo de YAML (validate_posts.py) |
| `pytz` | ≥ 2024.1 | Conversión de zonas horarias (Madrid → UTC) |

---

## Scripts

### `scripts/importer.py` — Importador RSS de la UPM

**Propósito:** Descarga el tablón de anuncios oficial de la ETSISI desde su feed RSS y genera posts Jekyll.

**Fuente:** `https://fi.upm.es/GestorTablon/rss2b.php`

**Ejecución:**

```bash
python scripts/importer.py
```

**Salida:** Ficheros `.md` en `_posts/` con el formato `YYYY-MM-DD-titulo-slugificado.md`.

**Comportamiento:**
- Parsea el feed RSS de la UPM
- Convierte cada entrada en un post Jekyll con front matter estándar
- Slugifica el título para el nombre del fichero
- No sobreescribe posts existentes con el mismo nombre

---

### `scripts/alertas.py` — Alertas meteorológicas AEMET

**Propósito:** Descarga y procesa las alertas meteorológicas activas de AEMET en formato CAP (Common Alerting Protocol).

**Fuente:** Feed RSS CAP de AEMET para la zona de Madrid.

**Ejecución:**

```bash
python scripts/alertas.py
```

**Salida:** `_data/alerts.json` con las alertas activas en formato:

```json
[
  {
    "event": "Viento",
    "severity": "Moderate",
    "expires": "2026-03-15T18:00:00+01:00",
    "description": "..."
  }
]
```

**Comportamiento:**
- Filtra alertas ya expiradas
- Deduplica por tipo de evento
- Genera `[]` si no hay alertas activas
- El componente `_includes/banner-aemet.html` consume este fichero en build time

---

### `scripts/caducidad.py` — Gestión de expiración de posts

**Propósito:** Gestiona el ciclo de vida de los posts: oculta los vencidos y genera el listado de próximos avisos para los widgets de la web.

**Ejecución:**

```bash
python scripts/caducidad.py
```

**Salidas:**
- Actualiza el campo `published: false` en los posts cuya fecha `expires` ya ha pasado
- Genera `_data/future_posts.json` con los avisos próximos (publicados pero aún no mostrados)

**Comportamiento:**
- Normaliza el formato de fechas en el front matter (`YYYY-MM-DD HH:MM:SS ±HHMM`)
- Gestiona correctamente el cambio de hora (zona Europe/Madrid)
- Los posts expirados se conservan en el repositorio como historial; solo se marca `published: false`

---

### `scripts/calfile.py` — Generador de calendario iCalendar

**Propósito:** Genera el fichero `assets/avisos.ics` a partir de todos los posts publicados, para permitir la suscripción al calendario.

**Ejecución:**

```bash
python scripts/calfile.py
```

**Salida:** `assets/avisos.ics` en formato RFC 5545 (iCalendar).

**Compatibilidad:**
- Google Calendar (via URL `webcal://` o importación)
- Apple Calendar
- Microsoft Outlook
- Cualquier cliente compatible con RFC 5545

**Comportamiento:**
- Lee todos los posts publicados en `_posts/`
- Crea un evento por post usando `date` como inicio y `expires` como fin (si existe)
- Aplica la codificación RFC 5545 correcta (plegado de líneas, escape de caracteres)
- Convierte fechas a UTC para máxima compatibilidad

---

### `scripts/validate_posts.py` — Validador de front matter (CI)

**Propósito:** Valida la coherencia y completitud del front matter YAML de los posts. Se usa en el pipeline CI de GitHub Actions.

**Ejecución:**

```bash
# Validar posts específicos
python scripts/validate_posts.py _posts/2026-03-15-mi-aviso.md

# Validar todos los posts
python scripts/validate_posts.py
```

**Salida:** Mensajes de error/advertencia en stdout. Exit code 1 si hay errores, 0 si todo es correcto.

**Validaciones que realiza:**
- Campos obligatorios presentes: `layout`, `title`, `date`, `author`, `published`
- Campos recomendados: `expires`
- Tipo correcto: `layout` debe ser `"post"`, `published` debe ser booleano
- Formato de nombre de fichero: `YYYY-MM-DD-slug.md`
- Coherencia de fechas: `expires` debe ser posterior a `date`

---

## Flujo de trabajo recomendado

Para mantener el sitio actualizado, se recomienda ejecutar los scripts en este orden:

```bash
# 1. Importar nuevos avisos de la UPM (si procede)
python scripts/importer.py

# 2. Actualizar alertas meteorológicas
python scripts/alertas.py

# 3. Marcar posts expirados y actualizar future_posts.json
python scripts/caducidad.py

# 4. Regenerar el calendario
python scripts/calfile.py

# 5. Hacer commit de los cambios generados
git add _posts/ _data/ assets/avisos.ics
git commit -m "chore: actualizar datos automáticos"
git push
```

El push a `main` disparará automáticamente el workflow de GitHub Actions que validará todos los posts.

---

## Ejecución automática

Actualmente los scripts se ejecutan manualmente o mediante procesos externos. Si se desea automatizar su ejecución periódica, se puede configurar un cron job o un workflow adicional de GitHub Actions con el evento `schedule`:

```yaml
on:
  schedule:
    - cron: '0 * * * *'   # Cada hora (alertas)
    - cron: '0 6 * * *'   # Cada día a las 6:00 (caducidad + calfile)
```
