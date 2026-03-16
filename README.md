# 📢 Avisos 5S/6F 2M-B

[![Validar Posts](https://github.com/ggelado/avisos5S2M-B/actions/workflows/validate-posts.yml/badge.svg)](https://github.com/ggelado/avisos5S2M-B/actions/workflows/validate-posts.yml)
[![Licencia BSD-3-Clause](https://img.shields.io/badge/licencia-BSD%203--Clause-blue.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-activo-brightgreen?logo=github)](https://ggelado.github.io/avisos5S2M-B)
[![Jekyll](https://img.shields.io/badge/Jekyll-4.3-CC0000?logo=jekyll&logoColor=white)](https://jekyllrb.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)

Sistema centralizado de avisos académicos para el grupo **5S/6F 2M-B** de la ETSISI — Universidad Politécnica de Madrid.

Agrega exámenes, avisos de clase, cortes de transporte y alertas meteorológicas desde un único punto, accesible a través de múltiples canales de notificación.

[Ver sitio](https://ggelado.github.io/avisos5S2M-B) · [Feed RSS](https://ggelado.github.io/avisos5S2M-B/feed.xml) · [Calendario iCal](https://ggelado.github.io/avisos5S2M-B/avisos.ics) · [Bot de Discord](https://discord.com/oauth2/authorize?client_id=1464244457049424079&permissions=2048&integration_type=0&scope=bot) · [Reportar error](https://github.com/ggelado/avisos5S2M-B/issues/new/choose)

---

## Tabla de contenidos

- [Características](#características)
- [Canales de distribución](#canales-de-distribución)
- [Arquitectura](#arquitectura)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Scripts de automatización](#scripts-de-automatización)
- [Desarrollo local](#desarrollo-local)
- [Contribuir](#contribuir)
- [Seguridad](#seguridad)
- [Licencia](#licencia)

---

## Características

- **Avisos académicos** — exámenes, cambios de clase, notas, plazos y eventos del grupo
- **Alertas en tiempo real** — avisos meteorológicos de AEMET e incidencias de transporte de CRTM Madrid
- **Multi-canal** — RSS, iCalendar, bot de Discord, notificaciones push y bots de Telegram
- **PWA** — instalable como app en móvil, con soporte offline mediante service worker
- **Modo oscuro** — tema claro/oscuro adaptado automáticamente
- **Validación automática** — CI/CD con GitHub Actions que valida el front matter de cada post
- **Generación de calendario** — fichero `.ics` compatible con Google Calendar, Apple Calendar y Outlook

---

## Canales de distribución

| Canal | Enlace / Instrucciones |
|---|---|
| Web | [ggelado.github.io/avisos5S2M-B](https://ggelado.github.io/avisos5S2M-B) |
| Feed RSS | [`/feed.xml`](https://ggelado.github.io/avisos5S2M-B/feed.xml) — compatible con Thunderbird, Feeder, etc. |
| iCalendar | [`/avisos.ics`](https://ggelado.github.io/avisos5S2M-B/avisos.ics) · [Añadir a Google Calendar](https://calendar.google.com/calendar/r?cid=webcal%3A%2F%2Fggelado.github.io%2Favisos5S2M-B%2Favisos.ics) · [Añadir a Apple Calendar](webcal://ggelado.github.io/avisos5S2M-B/avisos.ics) |
| Bot de Discord | [Invitar al servidor](https://discord.com/oauth2/authorize?client_id=1464244457049424079&permissions=2048&integration_type=0&scope=bot) |
| Notificaciones push | Configurar en [notifierpushrss.onrender.com](https://notifierpushrss.onrender.com/) |
| Bots de Telegram | p.ej. `@FeedRiverBot` con `/add https://ggelado.github.io/avisos5S2M-B/feed.xml` |

> Si un aviso es modificado tras publicarse, algunos clientes RSS podrían no reflejar los cambios. Se recomienda revisar el enlace original del aviso o el Moodle de la asignatura.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                      Fuentes de datos                        │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────────────┐ │
│  │ UPM RSS  │   │ AEMET (CAP)  │   │  CRTM Madrid API     │ │
│  └────┬─────┘   └──────┬───────┘   └──────────┬───────────┘ │
└───────┼────────────────┼──────────────────────┼─────────────┘
        │                │                      │
        ▼                ▼                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Scripts Python (scripts/)                  │
│  importer.py    alertas.py    caducidad.py    calfile.py    │
└──────────────────────────────┬──────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
  _posts/*.md          _data/alerts.json        assets/avisos.ics
        │                      │
        └──────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │   Jekyll (GitHub Pages) │
        │  ┌────────┐ ┌────────┐ │
        │  │_layouts│ │_includes│ │
        │  └────────┘ └────────┘ │
        └────────────┬────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Web PWA       feed.xml   sitemap.xml
```

---

## Estructura del proyecto

```
avisos5S2M-B/
├── _config.yml               # Configuración de Jekyll
├── _data/                    # Datos estructurados (JSON/YAML)
│   ├── alerts.json           # Alertas activas (AEMET/CRTM)
│   ├── authors.yml           # Metadatos de autores
│   └── future_posts.json     # Avisos próximos (generado)
├── _includes/                # Componentes HTML reutilizables
│   ├── avisos.html           # Feed principal de avisos
│   ├── banner-aemet.html     # Banner de alertas meteorológicas
│   ├── proximos_buses.html   # Widget de próximos buses
│   ├── widget_aemet.html     # Widget del tiempo
│   └── ...                   # Otros 14 componentes
├── _layouts/                 # Plantillas de página
│   ├── default.html          # Layout principal
│   └── post.html             # Layout de aviso individual
├── _posts/                   # Avisos publicados (Markdown)
│   └── YYYY-MM-DD-slug.md
├── _templates/               # Plantillas para nuevos avisos
├── assets/                   # Recursos estáticos
│   ├── css/                  # Estilos (claro y oscuro)
│   ├── crtm/                 # Iconos SVG de estado del transporte
│   ├── icons/                # Iconos de la PWA
│   ├── manifest.json         # Manifiesto de la PWA
│   └── sw.js                 # Service worker
├── comoLlegar/               # Guías de navegación al campus
├── docs/                     # Documentación técnica
│   ├── ARCHITECTURE.md       # Descripción de la arquitectura
│   └── AUTOMATION.md         # Guía de scripts de automatización
├── scripts/                  # Scripts Python de automatización
│   ├── alertas.py            # Descarga alertas de AEMET
│   ├── caducidad.py          # Gestiona la expiración de posts
│   ├── calfile.py            # Genera el calendario .ics
│   ├── importer.py           # Importa posts desde RSS de la UPM
│   └── validate_posts.py     # Valida metadatos de posts (CI)
├── .github/
│   ├── ISSUE_TEMPLATE/       # Plantillas de issues
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── validate-posts.yml
├── CHANGELOG.md              # Historial de cambios
├── CODE_OF_CONDUCT.md        # Código de conducta
├── CONTRIBUTING.md           # Guía de contribución
├── Dockerfile                # Entorno de desarrollo Docker
├── docker-compose.yml        # Orquestación Docker
├── LICENSE                   # Licencia BSD 3-Clause
└── README.md                 # Este fichero
```

---

## Scripts de automatización

Todos los scripts se encuentran en el directorio `scripts/`.

| Script | Descripción | Salida |
|---|---|---|
| `importer.py` | Importa posts desde el tablón RSS de la UPM | `_posts/*.md` |
| `alertas.py` | Descarga alertas activas de AEMET (formato CAP) | `_data/alerts.json` |
| `caducidad.py` | Marca como expirados los posts vencidos; genera listado de próximos avisos | `_data/future_posts.json` |
| `calfile.py` | Genera el fichero iCalendar a partir de los posts publicados | `assets/avisos.ics` |
| `validate_posts.py` | Valida el front matter YAML de los posts (usado en CI) | salida estándar |

Para instalar las dependencias Python:

```bash
pip install -r requirements.txt
```

---

## Desarrollo local

### Opción A — Docker (recomendado)

```bash
docker compose up
```

El sitio estará disponible en `http://localhost:4000/avisos5S2M-B` con recarga en vivo.

### Opción B — Jekyll local

```bash
# Instalar dependencias Ruby
bundle install

# Servir el sitio en local
bundle exec jekyll serve --livereload
```

**Requisitos:** Ruby ≥ 3.0, Bundler, Jekyll 4.3

---

## Contribuir

Las contribuciones son bienvenidas. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para conocer el flujo de trabajo recomendado, las convenciones de contenido y el checklist para Pull Requests.

En resumen:

1. Haz un [fork](https://github.com/ggelado/avisos5S2M-B/fork) del repositorio
2. Crea una rama descriptiva (`fix/enlace-roto`, `feat/nuevo-widget`)
3. Realiza cambios enfocados y verifica que el sitio compila
4. Abre una Pull Request con descripción clara

Para publicar un nuevo aviso también puedes usar la [plantilla de issue](https://github.com/ggelado/avisos5S2M-B/issues/new/choose).

---

## Seguridad

Si descubres una vulnerabilidad de seguridad, **no la publiques en abierto**. Consulta [SECURITY.md](SECURITY.md) para conocer el proceso de divulgación responsable y los medios de contacto cifrado disponibles.

---

## Licencia

Distribuido bajo la licencia **BSD 3-Clause**. Consulta el fichero [LICENSE](LICENSE) para más detalles.

---

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" contentStyleType="text/css" data-diagram-type="SEQUENCE" height="1544px" preserveAspectRatio="none" style="width:1812px;height:1544px;background:#FFFFFF;" version="1.1" viewBox="0 0 1812 1544" width="1812px" zoomAndPan="magnify"><defs/><g><rect fill="none" height="103.2031" style="stroke:#000000;stroke-width:1.5;" width="705.4878" x="10" y="451.7578"/><rect fill="none" height="103.2031" style="stroke:#000000;stroke-width:1.5;" width="329.4243" x="744.8667" y="748.7578"/><rect fill="none" height="219.7344" style="stroke:#000000;stroke-width:1.5;" width="598.5908" x="1197.3276" y="1067.7578"/><g class="participant-lifeline" data-entity-uid="part1" data-qualified-name="Alumno" id="part1-lifeline"><g><title>Alumno</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="45.708" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="49" x2="49" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part2" data-qualified-name="Admin" id="part2-lifeline"><g><title>Admin</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="110.8481" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="114.416" x2="114.416" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part3" data-qualified-name="Scraper" id="part3-lifeline"><g><title>Scrapers</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="218.061" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="221.2803" x2="221.2803" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part4" data-qualified-name="Servidor" id="part4-lifeline"><g><title>Servidor</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="433.3984" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="437.0791" x2="437.0791" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part5" data-qualified-name="GitHub" id="part5-lifeline"><g><title>GitHub</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="602.9668" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="606.7095" x2="606.7095" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part6" data-qualified-name="Jekyll" id="part6-lifeline"><g><title>Jekyll</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="798.855" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="801.8667" x2="801.8667" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part7" data-qualified-name="Feed" id="part7-lifeline"><g><title>feed.xml</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="1022.6387" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="1025.9863" x2="1025.9863" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part8" data-qualified-name="Worker" id="part8-lifeline"><g><title>Worker RSS</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="1251.6235" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="1255.3276" x2="1255.3276" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part9" data-qualified-name="DB" id="part9-lifeline"><g><title>MySQL DB</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="1453.4722" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="1457.0195" x2="1457.0195" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part10" data-qualified-name="Push" id="part10-lifeline"><g><title>Web Push</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="1548.5625" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="1551.9248" x2="1551.9248" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part11" data-qualified-name="Discord" id="part11-lifeline"><g><title>Discord</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="1633.6348" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="1637.2002" x2="1637.2002" y1="81.2969" y2="1464.1563"/></g></g><g class="participant-lifeline" data-entity-uid="part12" data-qualified-name="Suscriptor" id="part12-lifeline"><g><title>Suscriptor</title><rect fill="#000000" fill-opacity="0.00000" height="1382.8594" width="8" x="1743.3716" y="81.2969"/><line style="stroke:#181818;stroke-width:0.5;stroke-dasharray:5,5;" x1="1746.8247" x2="1746.8247" y1="81.2969" y2="1464.1563"/></g></g><g class="participant participant-head" data-entity-uid="part1" data-qualified-name="Alumno" id="part1-head"><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="53.416" x="20" y="77.9951">Alumno</text><ellipse cx="49.708" cy="13.5" fill="#E2E2F0" rx="8" ry="8" style="stroke:#181818;stroke-width:0.5;"/><path d="M49.708,21.5 L49.708,48.5 M36.708,29.5 L62.708,29.5 M49.708,48.5 L36.708,63.5 M49.708,48.5 L62.708,63.5" fill="none" style="stroke:#181818;stroke-width:0.5;"/></g><g class="participant participant-tail" data-entity-uid="part1" data-qualified-name="Alumno" id="part1-tail"><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="53.416" x="20" y="1476.1514">Alumno</text><ellipse cx="49.708" cy="1487.9531" fill="#E2E2F0" rx="8" ry="8" style="stroke:#181818;stroke-width:0.5;"/><path d="M49.708,1495.9531 L49.708,1522.9531 M36.708,1503.9531 L62.708,1503.9531 M49.708,1522.9531 L36.708,1537.9531 M49.708,1522.9531 L62.708,1537.9531" fill="none" style="stroke:#181818;stroke-width:0.5;"/></g><g class="participant participant-head" data-entity-uid="part2" data-qualified-name="Admin" id="part2-head"><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="44.8643" x="89.416" y="77.9951">Admin</text><ellipse cx="114.8481" cy="13.5" fill="#E2E2F0" rx="8" ry="8" style="stroke:#181818;stroke-width:0.5;"/><path d="M114.8481,21.5 L114.8481,48.5 M101.8481,29.5 L127.8481,29.5 M114.8481,48.5 L101.8481,63.5 M114.8481,48.5 L127.8481,63.5" fill="none" style="stroke:#181818;stroke-width:0.5;"/></g><g class="participant participant-tail" data-entity-uid="part2" data-qualified-name="Admin" id="part2-tail"><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="44.8643" x="89.416" y="1476.1514">Admin</text><ellipse cx="114.8481" cy="1487.9531" fill="#E2E2F0" rx="8" ry="8" style="stroke:#181818;stroke-width:0.5;"/><path d="M114.8481,1495.9531 L114.8481,1522.9531 M101.8481,1503.9531 L127.8481,1503.9531 M114.8481,1522.9531 L101.8481,1537.9531 M114.8481,1522.9531 L127.8481,1537.9531" fill="none" style="stroke:#181818;stroke-width:0.5;"/></g><g class="participant participant-head" data-entity-uid="part3" data-qualified-name="Scraper" id="part3-head"><rect fill="#E2E2F0" height="46.5938" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="143.5615" x="150.2803" y="33.7031"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="61.4688" x="191.3267" y="53.6982">Scrapers</text><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="129.5615" x="157.2803" y="69.9951">(fuentes externas)</text></g><g class="participant participant-tail" data-entity-uid="part3" data-qualified-name="Scraper" id="part3-tail"><rect fill="#E2E2F0" height="46.5938" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="143.5615" x="150.2803" y="1463.1563"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="61.4688" x="191.3267" y="1483.1514">Scrapers</text><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="129.5615" x="157.2803" y="1499.4482">(fuentes externas)</text></g><g class="participant participant-head" data-entity-uid="part4" data-qualified-name="Servidor" id="part4-head"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="72.6387" x="401.0791" y="50"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="58.6387" x="408.0791" y="69.9951">Servidor</text></g><g class="participant participant-tail" data-entity-uid="part4" data-qualified-name="Servidor" id="part4-tail"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="72.6387" x="401.0791" y="1463.1563"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="58.6387" x="408.0791" y="1483.1514">Servidor</text></g><g class="participant participant-head" data-entity-uid="part5" data-qualified-name="GitHub" id="part5-head"><rect fill="#E2E2F0" height="46.5938" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="62.5146" x="575.7095" y="33.7031"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="48.5146" x="582.7095" y="53.6982">GitHub</text><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="35.793" x="589.0703" y="69.9951">Repo</text></g><g class="participant participant-tail" data-entity-uid="part5" data-qualified-name="GitHub" id="part5-tail"><rect fill="#E2E2F0" height="46.5938" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="62.5146" x="575.7095" y="1463.1563"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="48.5146" x="582.7095" y="1483.1514">GitHub</text><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="35.793" x="589.0703" y="1499.4482">Repo</text></g><g class="participant participant-head" data-entity-uid="part6" data-qualified-name="Jekyll" id="part6-head"><rect fill="#E2E2F0" height="46.5938" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="95.9766" x="754.8667" y="33.7031"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="36.9141" x="784.3979" y="53.6982">Jekyll</text><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="81.9766" x="761.8667" y="69.9951">Planificador</text></g><g class="participant participant-tail" data-entity-uid="part6" data-qualified-name="Jekyll" id="part6-tail"><rect fill="#E2E2F0" height="46.5938" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="95.9766" x="754.8667" y="1463.1563"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="36.9141" x="784.3979" y="1483.1514">Jekyll</text><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="81.9766" x="761.8667" y="1499.4482">Planificador</text></g><g class="participant participant-head" data-entity-uid="part7" data-qualified-name="Feed" id="part7-head"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="75.3047" x="988.9863" y="50"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="61.3047" x="995.9863" y="69.9951">feed.xml</text></g><g class="participant participant-tail" data-entity-uid="part7" data-qualified-name="Feed" id="part7-tail"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="75.3047" x="988.9863" y="1463.1563"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="61.3047" x="995.9863" y="1483.1514">feed.xml</text></g><g class="participant participant-head" data-entity-uid="part8" data-qualified-name="Worker" id="part8-head"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="96.5918" x="1207.3276" y="50"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="82.5918" x="1214.3276" y="69.9951">Worker RSS</text></g><g class="participant participant-tail" data-entity-uid="part8" data-qualified-name="Worker" id="part8-tail"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="96.5918" x="1207.3276" y="1463.1563"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="82.5918" x="1214.3276" y="1483.1514">Worker RSS</text></g><g class="participant participant-head" data-entity-uid="part9" data-qualified-name="DB" id="part9-head"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="86.9053" x="1414.0195" y="50"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="72.9053" x="1421.0195" y="69.9951">MySQL DB</text></g><g class="participant participant-tail" data-entity-uid="part9" data-qualified-name="DB" id="part9-tail"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="86.9053" x="1414.0195" y="1463.1563"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="72.9053" x="1421.0195" y="1483.1514">MySQL DB</text></g><g class="participant participant-head" data-entity-uid="part10" data-qualified-name="Push" id="part10-head"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="83.2754" x="1510.9248" y="50"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="69.2754" x="1517.9248" y="69.9951">Web Push</text></g><g class="participant participant-tail" data-entity-uid="part10" data-qualified-name="Push" id="part10-tail"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="83.2754" x="1510.9248" y="1463.1563"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="69.2754" x="1517.9248" y="1483.1514">Web Push</text></g><g class="participant participant-head" data-entity-uid="part11" data-qualified-name="Discord" id="part11-head"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="66.8691" x="1604.2002" y="50"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="52.8691" x="1611.2002" y="69.9951">Discord</text></g><g class="participant participant-tail" data-entity-uid="part11" data-qualified-name="Discord" id="part11-tail"><rect fill="#E2E2F0" height="30.2969" rx="2.5" ry="2.5" style="stroke:#181818;stroke-width:0.5;" width="66.8691" x="1604.2002" y="1463.1563"/><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="52.8691" x="1611.2002" y="1483.1514">Discord</text></g><g class="participant participant-head" data-entity-uid="part12" data-qualified-name="Suscriptor" id="part12-head"><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="71.0938" x="1708.8247" y="77.9951">Suscriptor</text><ellipse cx="1747.3716" cy="13.5" fill="#E2E2F0" rx="8" ry="8" style="stroke:#181818;stroke-width:0.5;"/><path d="M1747.3716,21.5 L1747.3716,48.5 M1734.3716,29.5 L1760.3716,29.5 M1747.3716,48.5 L1734.3716,63.5 M1747.3716,48.5 L1760.3716,63.5" fill="none" style="stroke:#181818;stroke-width:0.5;"/></g><g class="participant participant-tail" data-entity-uid="part12" data-qualified-name="Suscriptor" id="part12-tail"><text fill="#000000" font-family="sans-serif" font-size="14" lengthAdjust="spacing" textLength="71.0938" x="1708.8247" y="1476.1514">Suscriptor</text><ellipse cx="1747.3716" cy="1487.9531" fill="#E2E2F0" rx="8" ry="8" style="stroke:#181818;stroke-width:0.5;"/><path d="M1747.3716,1495.9531 L1747.3716,1522.9531 M1734.3716,1503.9531 L1760.3716,1503.9531 M1747.3716,1522.9531 L1734.3716,1537.9531 M1747.3716,1522.9531 L1760.3716,1537.9531" fill="none" style="stroke:#181818;stroke-width:0.5;"/></g><rect fill="#EEEEEE" height="3" style="stroke:#EEEEEE;stroke-width:1;" width="1805.9185" x="0" y="111.8633"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="111.8633" y2="111.8633"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="114.8633" y2="114.8633"/><rect fill="#EEEEEE" height="23.1328" style="stroke:#000000;stroke-width:2;" width="124.8809" x="840.5188" y="101.2969"/><text fill="#000000" font-family="sans-serif" font-size="13" font-weight="bold" lengthAdjust="spacing" textLength="106.355" x="846.5188" y="117.3638">1. PROPUESTA</text><g class="message" data-entity-1="part1" data-entity-2="part4" id="msg1"><polygon fill="#181818" points="425.3984,151.5625,435.3984,155.5625,425.3984,159.5625,429.3984,155.5625" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="49.708" x2="431.3984" y1="155.5625" y2="155.5625"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="168.6572" x="159.2246" y="150.4966">Envía aviso via formulario</text></g><g class="message" data-entity-1="part4" data-entity-2="part4" id="msg2"><line style="stroke:#181818;stroke-width:1;" x1="437.3984" x2="479.3984" y1="184.6953" y2="184.6953"/><line style="stroke:#181818;stroke-width:1;" x1="479.3984" x2="479.3984" y1="184.6953" y2="197.6953"/><line style="stroke:#181818;stroke-width:1;" x1="438.3984" x2="479.3984" y1="197.6953" y2="197.6953"/><polygon fill="#181818" points="448.3984,193.6953,438.3984,197.6953,448.3984,201.6953,444.3984,197.6953" style="stroke:#181818;stroke-width:1;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="155.5684" x="444.3984" y="179.6294">Valida datos y rate limit</text></g><g class="message" data-entity-1="part4" data-entity-2="part5" id="msg3"><polygon fill="#181818" points="594.9668,222.8281,604.9668,226.8281,594.9668,230.8281,598.9668,226.8281" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="437.3984" x2="600.9668" y1="226.8281" y2="226.8281"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="115.4448" x="464.4602" y="221.7622">Abre Pull Request</text></g><g class="message" data-entity-1="part2" data-entity-2="part4" id="msg4"><polygon fill="#181818" points="425.3984,251.9609,435.3984,255.9609,425.3984,259.9609,429.3984,255.9609" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="114.8481" x2="431.3984" y1="255.9609" y2="255.9609"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="176.3442" x="187.9512" y="250.895">Publica aviso directamente</text></g><g class="message" data-entity-1="part4" data-entity-2="part5" id="msg5"><polygon fill="#181818" points="594.9668,281.0938,604.9668,285.0938,594.9668,289.0938,598.9668,285.0938" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="437.3984" x2="600.9668" y1="285.0938" y2="285.0938"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="129.3398" x="457.5127" y="280.0278">Push directo a main</text></g><g class="message" data-entity-1="part3" data-entity-2="part4" id="msg6"><polygon fill="#181818" points="425.3984,310.2266,435.3984,314.2266,425.3984,318.2266,429.3984,314.2266" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="222.061" x2="431.3984" y1="314.2266" y2="314.2266"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="191.3374" x="234.061" y="309.1606">Fuente externa detecta aviso</text></g><g class="message" data-entity-1="part4" data-entity-2="part5" id="msg7"><polygon fill="#181818" points="594.9668,339.3594,604.9668,343.3594,594.9668,347.3594,598.9668,343.3594" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="437.3984" x2="600.9668" y1="343.3594" y2="343.3594"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="115.4448" x="464.4602" y="338.2935">Abre Pull Request</text></g><rect fill="#EEEEEE" height="3" style="stroke:#EEEEEE;stroke-width:1;" width="1805.9185" x="0" y="371.9258"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="371.9258" y2="371.9258"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="374.9258" y2="374.9258"/><rect fill="#EEEEEE" height="23.1328" style="stroke:#000000;stroke-width:2;" width="133.9644" x="835.9771" y="361.3594"/><text fill="#000000" font-family="sans-serif" font-size="13" font-weight="bold" lengthAdjust="spacing" textLength="115.4385" x="841.9771" y="377.4263">2. APROBACIÓN</text><g class="message" data-entity-1="part2" data-entity-2="part5" id="msg8"><polygon fill="#181818" points="594.9668,422.1914,604.9668,426.1914,594.9668,430.1914,598.9668,426.1914" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="114.8481" x2="600.9668" y1="426.1914" y2="426.1914"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="134.0562" x="293.8794" y="421.1255">Revisa y aprueba PR</text></g><path d="M611,399.4922 L611,439.4922 L763,439.4922 L763,409.4922 L753,399.4922 L611,399.4922" fill="#FEFFDD" style="stroke:#181818;stroke-width:0.5;"/><path d="M753,399.4922 L753,409.4922 L763,409.4922 L753,399.4922" fill="#FEFFDD" style="stroke:#181818;stroke-width:0.5;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="61.9849" x="617" y="416.5591">Admin no</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="131.6504" x="617" y="431.6919">necesita aprobación</text><path d="M10,451.7578 L74.4429,451.7578 L74.4429,458.8906 L64.4429,468.8906 L10,468.8906 L10,451.7578" fill="#EEEEEE" style="stroke:#000000;stroke-width:1.5;"/><rect fill="none" height="103.2031" style="stroke:#000000;stroke-width:1.5;" width="705.4878" x="10" y="451.7578"/><text fill="#000000" font-family="sans-serif" font-size="13" font-weight="bold" lengthAdjust="spacing" textLength="19.4429" x="25" y="464.8247">alt</text><text fill="#000000" font-family="sans-serif" font-size="11" font-weight="bold" lengthAdjust="spacing" textLength="89.2891" x="89.4429" y="463.9683">[PR aprobada]</text><g class="message" data-entity-1="part5" data-entity-2="part5" id="msg10"><line style="stroke:#181818;stroke-width:1;" x1="606.9668" x2="648.9668" y1="490.0234" y2="490.0234"/><line style="stroke:#181818;stroke-width:1;" x1="648.9668" x2="648.9668" y1="490.0234" y2="503.0234"/><line style="stroke:#181818;stroke-width:1;" x1="607.9668" x2="648.9668" y1="503.0234" y2="503.0234"/><polygon fill="#181818" points="617.9668,499.0234,607.9668,503.0234,617.9668,507.0234,613.9668,503.0234" style="stroke:#181818;stroke-width:1;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="89.521" x="613.9668" y="484.9575">Merge a main</text></g><line style="stroke:#000000;stroke-width:1;stroke-dasharray:2,2;" x1="10" x2="715.4878" y1="512.0234" y2="512.0234"/><text fill="#000000" font-family="sans-serif" font-size="11" font-weight="bold" lengthAdjust="spacing" textLength="94.1982" x="15" y="522.2339">[PR rechazada]</text><g class="message" data-entity-1="part5" data-entity-2="part1" id="msg11"><polygon fill="#181818" points="60.708,542.9609,50.708,546.9609,60.708,550.9609,56.708,546.9609" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;stroke-dasharray:2,2;" x1="54.708" x2="605.9668" y1="546.9609" y2="546.9609"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="152.6294" x="252.0227" y="541.895">Notificación de rechazo</text></g><rect fill="#EEEEEE" height="3" style="stroke:#EEEEEE;stroke-width:1;" width="1805.9185" x="0" y="582.5273"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="582.5273" y2="582.5273"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="585.5273" y2="585.5273"/><rect fill="#EEEEEE" height="23.1328" style="stroke:#000000;stroke-width:2;" width="206.3467" x="799.7859" y="571.9609"/><text fill="#000000" font-family="sans-serif" font-size="13" font-weight="bold" lengthAdjust="spacing" textLength="187.8208" x="805.7859" y="588.0278">3. PLANIFICACIÓN (Jekyll)</text><g class="message" data-entity-1="part5" data-entity-2="part6" id="msg12"><polygon fill="#181818" points="790.855,622.2266,800.855,626.2266,790.855,630.2266,794.855,626.2266" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="606.9668" x2="796.855" y1="626.2266" y2="626.2266"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="171.8882" x="618.9668" y="621.1606">Trigger rebuild tras merge</text></g><path d="M665,639.2266 L665,694.2266 L940,694.2266 L940,649.2266 L930,639.2266 L665,639.2266" fill="#FEFFDD" style="stroke:#181818;stroke-width:0.5;"/><path d="M930,639.2266 L930,649.2266 L940,649.2266 L930,639.2266" fill="#FEFFDD" style="stroke:#181818;stroke-width:0.5;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="254.4585" x="671" y="656.2935">Además, rebuild periódico programado</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="242.1187" x="671" y="671.4263">para publicar avisos con fecha futura</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="177.4868" x="671" y="686.5591">cuando llegue su momento</text><g class="message" data-entity-1="part6" data-entity-2="part6" id="msg13"><line style="stroke:#181818;stroke-width:1;" x1="802.855" x2="844.855" y1="720.7578" y2="720.7578"/><line style="stroke:#181818;stroke-width:1;" x1="844.855" x2="844.855" y1="720.7578" y2="733.7578"/><line style="stroke:#181818;stroke-width:1;" x1="803.855" x2="844.855" y1="733.7578" y2="733.7578"/><polygon fill="#181818" points="813.855,729.7578,803.855,733.7578,813.855,737.7578,809.855,733.7578" style="stroke:#181818;stroke-width:1;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="209.7837" x="809.855" y="715.6919">Comprueba fecha de cada aviso</text></g><path d="M744.8667,748.7578 L809.3096,748.7578 L809.3096,755.8906 L799.3096,765.8906 L744.8667,765.8906 L744.8667,748.7578" fill="#EEEEEE" style="stroke:#000000;stroke-width:1.5;"/><rect fill="none" height="103.2031" style="stroke:#000000;stroke-width:1.5;" width="329.4243" x="744.8667" y="748.7578"/><text fill="#000000" font-family="sans-serif" font-size="13" font-weight="bold" lengthAdjust="spacing" textLength="19.4429" x="759.8667" y="761.8247">alt</text><text fill="#000000" font-family="sans-serif" font-size="11" font-weight="bold" lengthAdjust="spacing" textLength="171.9556" x="824.3096" y="760.9683">[Fecha del aviso alcanzada]</text><g class="message" data-entity-1="part6" data-entity-2="part7" id="msg14"><polygon fill="#181818" points="1014.6387,783.0234,1024.6387,787.0234,1014.6387,791.0234,1018.6387,787.0234" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="802.855" x2="1020.6387" y1="787.0234" y2="787.0234"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="166.2261" x="831.6338" y="781.9575">Publica aviso en feed.xml</text></g><line style="stroke:#000000;stroke-width:1;stroke-dasharray:2,2;" x1="744.8667" x2="1074.291" y1="796.0234" y2="796.0234"/><text fill="#000000" font-family="sans-serif" font-size="11" font-weight="bold" lengthAdjust="spacing" textLength="89.187" x="749.8667" y="806.2339">[Fecha futura]</text><g class="message" data-entity-1="part6" data-entity-2="part6" id="msg15"><line style="stroke:#181818;stroke-width:1;" x1="802.855" x2="844.855" y1="830.9609" y2="830.9609"/><line style="stroke:#181818;stroke-width:1;" x1="844.855" x2="844.855" y1="830.9609" y2="843.9609"/><line style="stroke:#181818;stroke-width:1;" x1="803.855" x2="844.855" y1="843.9609" y2="843.9609"/><polygon fill="#181818" points="813.855,839.9609,803.855,843.9609,813.855,847.9609,809.855,843.9609" style="stroke:#181818;stroke-width:1;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="103.7588" x="809.855" y="825.895">Aviso en espera</text></g><rect fill="#EEEEEE" height="3" style="stroke:#EEEEEE;stroke-width:1;" width="1805.9185" x="0" y="879.5273"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="879.5273" y2="879.5273"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="882.5273" y2="882.5273"/><rect fill="#EEEEEE" height="23.1328" style="stroke:#000000;stroke-width:2;" width="136.0591" x="834.9297" y="868.9609"/><text fill="#000000" font-family="sans-serif" font-size="13" font-weight="bold" lengthAdjust="spacing" textLength="117.5332" x="840.9297" y="885.0278">4. PUBLICACIÓN</text><g class="message" data-entity-1="part7" data-entity-2="part7" id="msg16"><line style="stroke:#181818;stroke-width:1;" x1="1026.6387" x2="1068.6387" y1="938.3594" y2="938.3594"/><line style="stroke:#181818;stroke-width:1;" x1="1068.6387" x2="1068.6387" y1="938.3594" y2="951.3594"/><line style="stroke:#181818;stroke-width:1;" x1="1027.6387" x2="1068.6387" y1="951.3594" y2="951.3594"/><polygon fill="#181818" points="1037.6387,947.3594,1027.6387,951.3594,1037.6387,955.3594,1033.6387,951.3594" style="stroke:#181818;stroke-width:1;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="105.6123" x="1055.7698" y="918.1606">Aviso disponible</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="149.8745" x="1033.6387" y="933.2935">en GitHub Pages y RSS</text></g><rect fill="#EEEEEE" height="3" style="stroke:#EEEEEE;stroke-width:1;" width="1805.9185" x="0" y="979.9258"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="979.9258" y2="979.9258"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="982.9258" y2="982.9258"/><rect fill="#EEEEEE" height="23.1328" style="stroke:#000000;stroke-width:2;" width="142.2988" x="831.8098" y="969.3594"/><text fill="#000000" font-family="sans-serif" font-size="13" font-weight="bold" lengthAdjust="spacing" textLength="123.7729" x="837.8098" y="985.4263">5. NOTIFICACIÓN</text><g class="message" data-entity-1="part7" data-entity-2="part8" id="msg17"><polygon fill="#181818" points="1243.6235,1019.625,1253.6235,1023.625,1243.6235,1027.625,1247.6235,1023.625" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="1026.6387" x2="1249.6235" y1="1023.625" y2="1023.625"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="204.9849" x="1038.6387" y="1018.5591">Webhook: feed.xml actualizado</text></g><g class="message" data-entity-1="part8" data-entity-2="part9" id="msg18"><polygon fill="#181818" points="1445.4722,1048.7578,1455.4722,1052.7578,1445.4722,1056.7578,1449.4722,1052.7578" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="1255.6235" x2="1451.4722" y1="1052.7578" y2="1052.7578"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="177.8486" x="1267.6235" y="1047.6919">Comprueba items ya vistos</text></g><path d="M1197.3276,1067.7578 L1261.7705,1067.7578 L1261.7705,1074.8906 L1251.7705,1084.8906 L1197.3276,1084.8906 L1197.3276,1067.7578" fill="#EEEEEE" style="stroke:#000000;stroke-width:1.5;"/><rect fill="none" height="219.7344" style="stroke:#000000;stroke-width:1.5;" width="598.5908" x="1197.3276" y="1067.7578"/><text fill="#000000" font-family="sans-serif" font-size="13" font-weight="bold" lengthAdjust="spacing" textLength="19.4429" x="1212.3276" y="1080.8247">alt</text><text fill="#000000" font-family="sans-serif" font-size="11" font-weight="bold" lengthAdjust="spacing" textLength="85.293" x="1276.7705" y="1079.9683">[Aviso nuevo]</text><g class="message" data-entity-1="part8" data-entity-2="part9" id="msg19"><polygon fill="#181818" points="1445.4722,1102.0234,1455.4722,1106.0234,1445.4722,1110.0234,1449.4722,1106.0234" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="1255.6235" x2="1451.4722" y1="1106.0234" y2="1106.0234"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="114.7529" x="1299.1714" y="1100.9575">Marca como visto</text></g><g class="message" data-entity-1="part8" data-entity-2="part9" id="msg20"><polygon fill="#181818" points="1445.4722,1131.1563,1455.4722,1135.1563,1445.4722,1139.1563,1449.4722,1135.1563" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="1255.6235" x2="1451.4722" y1="1135.1563" y2="1135.1563"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="143.4253" x="1284.8352" y="1130.0903">Obtiene suscripciones</text></g><g class="message" data-entity-1="part8" data-entity-2="part10" id="msg21"><polygon fill="#181818" points="1540.5625,1160.2891,1550.5625,1164.2891,1540.5625,1168.2891,1544.5625,1164.2891" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="1255.6235" x2="1546.5625" y1="1164.2891" y2="1164.2891"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="150.6489" x="1328.7686" y="1159.2231">Envía notificación push</text></g><g class="message" data-entity-1="part10" data-entity-2="part12" id="msg22"><polygon fill="#181818" points="1735.3716,1189.4219,1745.3716,1193.4219,1735.3716,1197.4219,1739.3716,1193.4219" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;stroke-dasharray:2,2;" x1="1552.5625" x2="1741.3716" y1="1193.4219" y2="1193.4219"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="170.8091" x="1564.5625" y="1188.356">Notificación en navegador</text></g><g class="message" data-entity-1="part8" data-entity-2="part11" id="msg23"><polygon fill="#181818" points="1625.6348,1218.5547,1635.6348,1222.5547,1625.6348,1226.5547,1629.6348,1222.5547" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="1255.6235" x2="1631.6348" y1="1222.5547" y2="1222.5547"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="171.8755" x="1360.6914" y="1217.4888">Envía mensaje con embed</text></g><line style="stroke:#000000;stroke-width:1;stroke-dasharray:2,2;" x1="1197.3276" x2="1795.9185" y1="1231.5547" y2="1231.5547"/><text fill="#000000" font-family="sans-serif" font-size="11" font-weight="bold" lengthAdjust="spacing" textLength="59.5762" x="1202.3276" y="1241.7651">[Ya visto]</text><g class="message" data-entity-1="part8" data-entity-2="part8" id="msg24"><line style="stroke:#181818;stroke-width:1;" x1="1255.6235" x2="1297.6235" y1="1266.4922" y2="1266.4922"/><line style="stroke:#181818;stroke-width:1;" x1="1297.6235" x2="1297.6235" y1="1266.4922" y2="1279.4922"/><line style="stroke:#181818;stroke-width:1;" x1="1256.6235" x2="1297.6235" y1="1279.4922" y2="1279.4922"/><polygon fill="#181818" points="1266.6235,1275.4922,1256.6235,1279.4922,1266.6235,1283.4922,1262.6235,1279.4922" style="stroke:#181818;stroke-width:1;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="39.603" x="1262.6235" y="1261.4263">Omite</text></g><rect fill="#EEEEEE" height="3" style="stroke:#EEEEEE;stroke-width:1;" width="1805.9185" x="0" y="1315.0586"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="1315.0586" y2="1315.0586"/><line style="stroke:#000000;stroke-width:1;" x1="0" x2="1805.9185" y1="1318.0586" y2="1318.0586"/><rect fill="#EEEEEE" height="23.1328" style="stroke:#000000;stroke-width:2;" width="165.9248" x="819.9968" y="1304.4922"/><text fill="#000000" font-family="sans-serif" font-size="13" font-weight="bold" lengthAdjust="spacing" textLength="147.3989" x="825.9968" y="1320.5591">Alta de suscriptores</text><g class="message" data-entity-1="part12" data-entity-2="part4" id="msg25"><polygon fill="#181818" points="448.3984,1354.7578,438.3984,1358.7578,448.3984,1362.7578,444.3984,1358.7578" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="442.3984" x2="1746.3716" y1="1358.7578" y2="1358.7578"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="160.1133" x="1012.3284" y="1353.6919">Solicita suscripción push</text></g><g class="message" data-entity-1="part4" data-entity-2="part9" id="msg26"><polygon fill="#181818" points="1445.4722,1383.8906,1455.4722,1387.8906,1445.4722,1391.8906,1449.4722,1387.8906" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="437.3984" x2="1451.4722" y1="1387.8906" y2="1387.8906"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="125.0679" x="884.9014" y="1382.8247">Guarda suscripción</text></g><g class="message" data-entity-1="part4" data-entity-2="part10" id="msg27"><polygon fill="#181818" points="1540.5625,1413.0234,1550.5625,1417.0234,1540.5625,1421.0234,1544.5625,1417.0234" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;" x1="437.3984" x2="1546.5625" y1="1417.0234" y2="1417.0234"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="124.3125" x="932.8242" y="1411.9575">Envía confirmación</text></g><g class="message" data-entity-1="part10" data-entity-2="part12" id="msg28"><polygon fill="#181818" points="1735.3716,1442.1563,1745.3716,1446.1563,1735.3716,1450.1563,1739.3716,1446.1563" style="stroke:#181818;stroke-width:1;"/><line style="stroke:#181818;stroke-width:1;stroke-dasharray:2,2;" x1="1552.5625" x2="1741.3716" y1="1446.1563" y2="1446.1563"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacing" textLength="152.4263" x="1573.7539" y="1441.0903">Suscripción confirmada</text></g><?plantuml-src ZLLBRkD64Dtp50MlPe34G7uR0mv0sQE90tyqaYT106-AP8dgkDdDz4SPppLoWXmWgpc2BpRL7r5gsOliIFQhttlLZ_PHg14D3c3fBq-gfHko5dkgfUWLjAGScShkKHlizDz2zR16QQd2rca39xNqWz8dW1RIutJG3KAbx-6fuYnEj694vU1arHeSoTW7zMRjGoKBz8dhARHlOqm674MHsOfEcuJ8BoNalN2_-EP1BMbCJQKF9UXNUdoIya4j92gn5YtkSgQ34hmcwau_3J82vlnI7l-kpICPMAvM4P1UIyZDq-h3DLpE8k1oTXHF3IoytSJ3y50UNmhRQjEbqFIy8tZbRMl4w7PyJAzLTNuEtvt2Odct-FXkTL_3-NcLn85lVvw8WpDufxRF_o7WLbWDMu6mrcRm4etGrGGhGtv3AJg43fssy0G67O4KWt15G6ATuNLZYCUI4fPXowohuZOS9LtuHh8CkP5E66eT3c4lNiyQUCem3GW3ydxbZJdAF8_RjLikwCY5rAdG_-quqFdzATJCvwo-k7h-vpOIkfjZYbmIPqKc1KVZgK4Me5AQgnlHRrm5wI80Nn40HIrP4JePZMwm5SzVL4MgWn1GeNGSdCywP7mkSbZkXanFk-c9hsG8OKes-BcCuQ2i_XdSQXStFXPaEdA03hNZe3_mtbpNjrVpguiywvjqAzw6eVTjf8-SyPwdwvbtGuqNiWDdU1c7q5iQNc_vC5-iG04Dp__QRoOuIyQjTABLmDFsx3Hy6naOJ0V6j1ScwMMXrGhMeM5OU-TD6BBrg3eDKbBl2Qo7GOV5qNioSwU7FL_e8KkKiZ4FR0AxjGZip_DtcNSIPOigyxfF6EpWnVfIw35vHf9bNdRyIZ_rBf0iyu6J63-o61zdrvCKh40ikIzTvnjZHwr48-b1SPQiqeBDFDnHzgQOxQTJkBsxFr3s85ssiJDWFzfe_NWspG1iDvul_UUWIuPnmEMiu54u6hWMiejOTeR8OUfDUTe6GOz2Rz0mOwqUT0fvYRXhd20LD8t6rWgjo1QmQ0EJYwbYjSTWfP0WuGRixV75BM3656wf3x-1ierakFiIl5aM_wIuXpGq_2-80l-1hymmCNh7vaYJfBLqST_ir0zhn48Sz5Sws4hpRWMdc7YOnZlqhqZPUu-cAv45g2ICfrWBCsJpUPsfrM7HNK27Nm40?></g></svg>
```puml
@startuml
skinparam sequenceMessageAlign center
skinparam shadowing false
actor "Alumno" as Alumno
actor "Admin" as Admin
participant "Scrapers\n(fuentes externas)" as Scraper
participant "Servidor" as Servidor
participant "GitHub\nRepo" as GitHub
participant "Jekyll\nPlanificador" as Jekyll
participant "feed.xml" as Feed
participant "Worker RSS" as Worker
participant "MySQL DB" as DB
participant "Web Push" as Push
participant "Discord" as Discord
actor "Suscriptor" as Suscriptor

== 1. PROPUESTA ==
Alumno -> Servidor : Envía aviso via formulario
Servidor -> Servidor : Valida datos y rate limit
Servidor -> GitHub : Abre Pull Request
Admin -> Servidor : Publica aviso directamente
Servidor -> GitHub : Push directo a main
Scraper -> Servidor : Fuente externa detecta aviso
Servidor -> GitHub : Abre Pull Request

== 2. APROBACIÓN ==
Admin -> GitHub : Revisa y aprueba PR
note right
  Admin no
  necesita aprobación
end note
alt PR aprobada
  GitHub -> GitHub : Merge a main
else PR rechazada
  GitHub --> Alumno : Notificación de rechazo
end

== 3. PLANIFICACIÓN (Jekyll) ==
GitHub -> Jekyll : Trigger rebuild tras merge
note over Jekyll
  Además, rebuild periódico programado
  para publicar avisos con fecha futura
  cuando llegue su momento
end note
Jekyll -> Jekyll : Comprueba fecha de cada aviso
alt Fecha del aviso alcanzada
  Jekyll -> Feed : Publica aviso en feed.xml
else Fecha futura
  Jekyll -> Jekyll : Aviso en espera
end

== 4. PUBLICACIÓN ==
Feed -> Feed : Aviso disponible\nen GitHub Pages y RSS

== 5. NOTIFICACIÓN ==
Feed -> Worker : Webhook: feed.xml actualizado
Worker -> DB : Comprueba items ya vistos
alt Aviso nuevo
  Worker -> DB : Marca como visto
  Worker -> DB : Obtiene suscripciones
  Worker -> Push : Envía notificación push
  Push --> Suscriptor : Notificación en navegador
  Worker -> Discord : Envía mensaje con embed
else Ya visto
  Worker -> Worker : Omite
end

== Alta de suscriptores ==
Suscriptor -> Servidor : Solicita suscripción push
Servidor -> DB : Guarda suscripción
Servidor -> Push : Envía confirmación
Push --> Suscriptor : Suscripción confirmada
@enduml
```
