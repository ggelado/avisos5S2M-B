# Guía de contribución

Gracias por tu interés en contribuir a este proyecto.
La web está hecha por y para alumnos, así que cualquier mejora suma: contenido, correcciones, automatizaciones o UX.

## Cómo puedes contribuir

- **Reportar errores** — abre un [issue de tipo Bug](https://github.com/ggelado/avisos5S2M-B/issues/new?template=bug-report.md)
- **Proponer mejoras** — abre un [issue de tipo Mejora](https://github.com/ggelado/avisos5S2M-B/issues/new?template=feature-request.md)
- **Publicar un aviso** — usa la [plantilla de aviso](https://github.com/ggelado/avisos5S2M-B/issues/new?template=dar-de-alta-avisos.md) o abre directamente una Pull Request
- **Mejorar el código** — corrige textos, arregla enlaces rotos, mejora estilos o lógica de scripts

## Requisitos para entorno local

### Opción A — Docker (recomendado)

```bash
docker compose up
```

El sitio estará disponible en `http://localhost:4000/avisos5S2M-B` con recarga en vivo.

### Opción B — Jekyll local

```bash
bundle install
bundle exec jekyll serve --livereload
```

**Requisitos:** Ruby ≥ 3.0, Bundler, Jekyll 4.3

### Scripts Python

```bash
pip install -r requirements.txt
```

Consulta [`docs/AUTOMATION.md`](docs/AUTOMATION.md) para ver cómo ejecutar cada script.

## Flujo recomendado

1. Haz un [fork](https://github.com/ggelado/avisos5S2M-B/fork) del repositorio
2. Crea una rama con nombre descriptivo (`fix/enlace-roto`, `feat/nuevo-widget`, `post/aviso-examen-SD`)
3. Realiza cambios enfocados en un solo objetivo
4. Verifica que el sitio compila y que no has roto contenido existente
5. Abre una Pull Request con una descripción clara (la plantilla te guiará)

## Convenciones de contenido

### Posts (`_posts/`)

- Nombre de fichero: `YYYY-MM-DD-titulo-descriptivo.md`
- Campos obligatorios en el front matter: `layout`, `title`, `date`, `author`, `published`
- Campo recomendado: `expires` (fecha a partir de la cual el aviso se ocultará)
- Puedes usar la plantilla en `_templates/Avisos.md` como punto de partida

### Componentes HTML

- Los componentes reutilizables van en `_includes/`
- Las plantillas de página van en `_layouts/`
- Si modificas un componente, revisa su impacto en todas las páginas que lo usan

### Scripts Python

- Todos los scripts van en `scripts/`
- Consulta [`docs/AUTOMATION.md`](docs/AUTOMATION.md) para la descripción de cada uno

## Checklist para Pull Request

La plantilla de PR ya incluye este checklist. Antes de enviar, asegúrate de que:

- [ ] El cambio tiene objetivo claro y alcance limitado
- [ ] No incluye cambios no relacionados
- [ ] El sitio compila sin errores
- [ ] Si toca `_posts/`, el front matter pasa la validación del CI
- [ ] Si toca UI, incluye captura de pantalla o descripción del cambio visual
- [ ] Si toca lógica de scripts, describe el caso de uso y el comportamiento esperado
- [ ] Se referencian los issues relacionados (usa `Closes #N`)

## Seguridad

Si encuentras una vulnerabilidad, **no la publiques en abierto**.
Revisa el proceso de divulgación responsable en [SECURITY.md](SECURITY.md).

## Código de conducta

Este proyecto sigue el [Código de Conducta](CODE_OF_CONDUCT.md) basado en el Contributor Covenant.
Se espera un trato respetuoso, colaborativo y constructivo en todos los espacios del proyecto.

---

Si tienes sugerencias pero no quieres tocar código, no hay problema — compártelas a través de issues o los canales habituales del Equipo de Delegados.