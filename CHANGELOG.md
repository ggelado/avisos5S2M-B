# Historial de cambios

Todos los cambios notables de este proyecto se documentan aquí.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Sin publicar]

### Añadido
- Directorio `docs/` con documentación técnica: `ARCHITECTURE.md` y `AUTOMATION.md`
- `CODE_OF_CONDUCT.md` — Código de conducta del proyecto
- `CONTRIBUTING.md` — Guía de contribución (renombrado desde `contributing.md`)
- `.github/PULL_REQUEST_TEMPLATE.md` — Plantilla estándar para Pull Requests
- Plantillas de issue adicionales: reporte de error y solicitud de mejora
- Todos los scripts Python consolidados bajo `scripts/`

### Cambiado
- `README.md` completamente reescrito: badges de estado, tabla de contenidos, arquitectura, estructura de directorios y guía rápida de desarrollo
- `contributing.md` renombrado a `CONTRIBUTING.md` (convención estándar de GitHub)
- Scripts `alertas.py`, `caducidad.py`, `calfile.py` e `importer.py` movidos de la raíz del repositorio a `scripts/`

---

## [2026-03-05]

### Añadido
- Enunciado práctica SOS publicado como aviso
- Integración con CRTM: widget de estado de líneas de transporte en tiempo real

### Cambiado
- Mejoras de rendimiento en `_includes/logica_crtm.html`

---

## [2026-02-22]

### Cambiado
- Actualización de `_includes/banner-aemet.html` con soporte para alertas de nivel rojo
- Mejoras de accesibilidad en los iconos SVG del transporte

---

## [2025-12-19]

### Añadido
- Soporte para notificaciones push mediante `notifierpushrss.onrender.com`
- Service worker (`assets/sw.js`) con caché offline básica

---

## [2025-12-08]

### Añadido
- Convocatoria de examen Cisco CCNA publicada
- Widget de próximos buses (`_includes/proximos_buses.html`)

---

## [2025-11-16]

### Añadido
- Inicio del servicio de avisos
- Sitio Jekyll publicado en GitHub Pages
- Feed RSS mediante `jekyll-feed`
- Integración iCalendar con `scripts/calfile.py`
- Scripts de automatización: `alertas.py`, `caducidad.py`, `importer.py`
- Bot de Discord integrado
- PWA: manifiesto y service worker básico
- Workflow de GitHub Actions para validación de posts (`validate-posts.yml`)
- Guías de navegación al campus en `comoLlegar/`
- Iconos SVG de estado del transporte CRTM en `assets/crtm/`
