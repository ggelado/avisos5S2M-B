---
layout: default
title: Contribuir
permalink: /contributing/
---

# Guia de contribucion

Gracias por tu interes en contribuir a este proyecto.
La web esta hecha por y para alumnos, asi que cualquier mejora suma: contenido, correcciones, automatizaciones o UX.

## Como puedes contribuir

- Reportar errores o proponer mejoras desde Issues o Security.
- Corregir textos, enlaces rotos o estilos visuales.
- Mejorar la logica de scripts Python y automatizaciones.
- Proponer o actualizar avisos en el formato del sitio.

## Requisitos para entorno local

Puedes trabajar de dos formas:

- Con Docker (recomendado para entorno consistente).
- Con Ruby/Jekyll de forma local usando el `Gemfile` del repo.

## Flujo recomendado

1. Haz un fork del repositorio.
2. Crea una rama con un nombre claro (`fix/enlace-roto`, `feat/nuevo-widget`, etc.).
3. Haz cambios pequenos y enfocados en un solo objetivo.
4. Verifica que el sitio compila y que no has roto contenido existente.
5. Abre un Pull Request con una descripcion clara.

## Convenciones de contenido

- Los avisos van en `_posts/`.
- Usa nombres de archivo con formato `YYYY-MM-DD-titulo-del-aviso.md`.
- Mantiene front matter coherente.
- Si cambias componentes reutilizables, revisa su impacto en `_includes/` y `_layouts/`.

## Checklist para Pull Request

Antes de abrir PR, revisa esto:

- El cambio tiene objetivo claro y alcance limitado.
- No incluye cambios no relacionados.
- Si toca UI, incluye captura o breve explicacion visual.
- Si toca logica, explica el caso de uso y el comportamiento esperado.
- Referencia Issues relacionadas, si aplica.

## Seguridad

Si encuentras una vulnerabilidad, no la publiques en abierto.
Revisa el proceso en [SECURITY.md](SECURITY.md).

## Codigo de conducta

No hay un codigo de conducta formal en este repo.
Aun asi, se espera trato respetuoso, colaborativo y constructivo en Issues y PRs.

Y si simplemente tienes sugerencias, pero no quieres tocar código, no pasa nada. Haznoslas llegar a través de issues o mediante los canales habituales del Equipo de Delegados.