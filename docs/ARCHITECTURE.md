# Arquitectura del sistema

## Visión general

El sistema de avisos funciona como un sitio estático generado con **Jekyll** y publicado en **GitHub Pages**. Los datos dinámicos (alertas meteorológicas, estado del transporte, calendario) se generan mediante scripts Python que se ejecutan periódicamente fuera del proceso de build de Jekyll.

---

## Flujo de datos

```
Fuentes externas
    │
    ├── UPM RSS feed  ──────────────►  scripts/importer.py  ──►  _posts/*.md
    │
    ├── AEMET CAP RSS  ─────────────►  scripts/alertas.py   ──►  _data/alerts.json
    │
    └── CRTM Madrid API  ──────────►  (widget JS en tiempo real)
                                            │
                                            ▼
                                   _includes/logica_crtm.html

Posts publicados  ──────────────►  scripts/caducidad.py  ──►  _data/future_posts.json
Posts publicados  ──────────────►  scripts/calfile.py    ──►  assets/avisos.ics

Jekyll build  (lee _posts/, _data/, _includes/, _layouts/)
    │
    └──►  _site/  (HTML estático)  ──►  GitHub Pages
```

---

## Componentes principales

### Generación de sitio estático — Jekyll

| Directorio | Función |
|---|---|
| `_posts/` | Avisos en formato Markdown con front matter YAML |
| `_data/` | Datos estructurados consumidos por Jekyll (JSON/YAML) |
| `_includes/` | Componentes HTML reutilizables (widgets, banners, lógica JS) |
| `_layouts/` | Plantillas de página (`default.html`, `post.html`) |
| `assets/` | CSS, JS, iconos SVG, manifiesto PWA, service worker |
| `_config.yml` | Configuración global de Jekyll |

### Automatización Python — `scripts/`

| Script | Frecuencia recomendada | Descripción |
|---|---|---|
| `alertas.py` | Cada hora | Consulta el feed CAP de AEMET y actualiza `_data/alerts.json` |
| `caducidad.py` | Diaria | Marca como `published: false` los posts expirados; actualiza `_data/future_posts.json` |
| `calfile.py` | Tras cada push | Regenera `assets/avisos.ics` a partir de los posts publicados |
| `importer.py` | Manual / periódica | Importa avisos del RSS oficial de la UPM como nuevos posts |
| `validate_posts.py` | CI (GitHub Actions) | Valida el front matter YAML de los posts en PRs y pushes a `main` |

### Integración continua — GitHub Actions

El workflow `.github/workflows/validate-posts.yml`:

- Se ejecuta en Pull Requests que modifiquen `_posts/**` y en pushes a `main`
- Valida el front matter YAML de todos los posts afectados mediante `scripts/validate_posts.py`
- Comprueba campos obligatorios, tipos de datos y coherencia de fechas

---

## Modelo de datos — Post

Cada aviso es un fichero Markdown en `_posts/` con el siguiente front matter:

```yaml
---
layout: post           # obligatorio
title: "Texto"         # obligatorio
date: YYYY-MM-DD HH:MM:SS +HHMM   # obligatorio — fecha de publicación
author: Gonzalo        # obligatorio
published: true        # obligatorio — false para ocultar
expires: YYYY-MM-DD HH:MM:SS +HHMM  # recomendado — fecha de expiración
categories:            # opcional
  - Convocatorias de Examen
excerpt: "Resumen"     # opcional — aparece en el feed RSS
image: "https://..."   # opcional — imagen de cabecera
---

Contenido en Markdown...
```

El nombre del fichero sigue el formato `YYYY-MM-DD-slug-descriptivo.md`.

---

## PWA y service worker

El sitio es instalable como Progressive Web App:

- `assets/manifest.json` — metadatos de la app (nombre, iconos, colores)
- `assets/sw.js` — service worker con estrategia cache-first para recursos estáticos
- `assets/icons/` — iconos en 180, 192 y 512 px para iOS y Android

---

## Tema y estilos

El sitio usa `jekyll-theme-primer` como base y lo extiende con:

| Fichero | Propósito |
|---|---|
| `assets/css/custom.css` | Personalizaciones del tema (modo claro) |
| `assets/css/custom_dark.css` | Personalizaciones del tema (modo oscuro) |
| `assets/css/callouts.css` | Estilos para bloques callout |
| `assets/css/callouts_dark.css` | Estilos callout en modo oscuro |

El cambio de tema claro/oscuro se gestiona mediante JavaScript en `_includes/head-custom.html`.

---

## Iconos de estado del transporte

El directorio `assets/crtm/` contiene 48 iconos SVG para representar el estado operativo de las líneas de transporte de Madrid:

- Líneas: metro, EMT, cercanías, metro ligero, interurbanos, BEI
- Estados: verde (normal), amarillo (incidencia parcial), rojo (corte total)
- Variantes: modo claro y modo oscuro
