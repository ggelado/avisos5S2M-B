---
layout: default
title: Inicio de servicio
date: 2025-11-16 19:26:00 +0100
author: Gonzalo
published: true
last_modified_at: 2026-02-22 14:38:00 +0100
---
De ahora en adelante se publicarán aquí las últimas novedades de interés, debido al exceso de publicaciones en el grupo.

También estarán disponibles como feed RSS, por lo que se pueden recibir los mensajes desde clientes como Thunderbird, apps móviles (como Feeder), bots de Telegram (p.ej. @FeedRiverBot, con el comando `/add https://ggelado.github.io/avisos5S2M-B/feed.xml`)...

**Se recomienda configurar las notificaciones push [desde aquí](https://notifierpushrss.onrender.com/).**

Los avisos cuentan con categorías XML, que puede utilizar para filtrar si su cliente RSS lo permite.

Si se utiliza el cliente Feeder, se recomienda configurar las notificaciones y una frecuencia de refresco suficientemente alta, se recomienda 15 minutos.

Recuerda que si un post se modifica, su cliente RSS podría no reflejar los cambios. Por ello se recomienda que aquellos avisos que puedan estar sujetos a cambios regulares (como pueden ser las convocatorias de examen) se revisen accediendo al enlace del aviso y/o Moodle de las asignaturas.

**INCLUSO HAY UN BOT DE DISCORD QUE PUEDES AGREGAR A TU SERVIDOR [PULSANDO AQUÍ](https://discord.com/oauth2/authorize?client_id=1464244457049424079&permissions=2048&integration_type=0&scope=bot)**

¿Todavía no te parece suficiente? Puedes incluso agregar los distintos avisos a tu calendario. Simplemente accede a tu proveedor de calendario (p.ej. google calendar), agregar calendario por url e indica `https://ggelado.github.io/avisos5S2M-B/avisos.ics`

[Agregar a Google Calendar](https://calendar.google.com/calendar/r?cid=webcal%3A%2F%2Fggelado.github.io%2Favisos5S2M-B%2Favisos.ics).
[Agregar a Apple Calendar](webcal://ggelado.github.io/avisos5S2M-B/avisos.ics). (no tengo dispositivos de apple, si no va el link me decís)

---

La web está creada por alumnos y para alumnos. Bastantes cosas están muy chapuceras, lo reconocemos, pero por ello el código es público y está abierto a Pull Requests, por lo que animamos a todo el mundo a contribuir con lo que pueda, desde diseño gráfico (de ahí los logos tan cutres, era un requisito de Google para poder configurarla como web-app) hasta la lógica de negocio.

[Contribuir](https://github.com/ggelado/avisos5S2M-B/fork)

Y si encuentras alguna vulnerabilidad de seguridad, por favor, indícanoslo a través de la pestaña [Security](https://github.com/ggelado/avisos5S2M-B/security/advisories/new) del repositorio o por los medios cifrados de contacto [disponibles aquí](https://ggelado.github.io/avisos5S2M-B/SECURITY). Por favor, insistimos en utilizar estos medios y no cualquier otro cuando se traten de vulnerabilidades o problemas de seguridad.

---

# ¿Cómo funciona? (POST EN REDACCIÓN)

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';

  document.querySelectorAll('pre code.language-mermaid').forEach(el => {
    // Decodifica entidades HTML (&gt; -> >, etc.)
    const txt = document.createElement('textarea');
    txt.innerHTML = el.innerHTML;
    const decoded = txt.value;

    const div = document.createElement('div');
    div.className = 'mermaid';
    div.textContent = decoded;
    el.closest('pre').replaceWith(div);
  });

  mermaid.initialize({ startOnLoad: true });
</script>

```mermaid
sequenceDiagram
    actor Alumno
    actor Admin
    participant Scraper as Scrapers (fuentes externas)
    participant Servidor
    participant GitHub as GitHub Repo
    participant Jekyll as Jekyll Planificador
    participant Feed as feed.xml
    participant Worker as Worker RSS
    participant DB as MySQL DB
    participant Push as Web Push
    participant Discord
    actor Suscriptor

    rect rgb(220, 235, 255)
        Note over Alumno,Suscriptor: 1. PROPUESTA
        Alumno->>Servidor: Envía aviso via formulario
        Servidor->>Servidor: Valida datos y rate limit
        Servidor->>GitHub: Abre Pull Request
        Admin->>Servidor: Publica aviso directamente
        Servidor->>GitHub: Push directo a main
        Scraper->>Servidor: Fuente externa detecta aviso
        Servidor->>GitHub: Abre Pull Request
    end

    rect rgb(220, 255, 220)
        Note over Alumno,Suscriptor: 2. APROBACIÓN
        Admin->>GitHub: Revisa y aprueba PR
        Note right of Admin: Admin no necesita aprobación
        alt PR aprobada
            GitHub->>GitHub: Merge a main
        else PR rechazada
            GitHub-->>Alumno: Notificación de rechazo
        end
    end

    rect rgb(255, 255, 210)
        Note over Alumno,Suscriptor: 3. PLANIFICACIÓN (Jekyll)
        GitHub->>Jekyll: Trigger rebuild tras merge
        Note over Jekyll: Además, rebuild periódico programado<br/>para publicar avisos con fecha futura<br/>cuando llegue su momento
        loop periódicamente
            Jekyll->>Jekyll: Comprueba fecha de cada aviso
            alt Fecha del aviso alcanzada
                Jekyll->>Feed: Publica aviso en feed.xml
            else Fecha futura
                Jekyll->>Jekyll: Aviso en espera
            end
        end
    end

    rect rgb(255, 235, 210)
        Note over Alumno,Suscriptor: 4. PUBLICACIÓN
        Feed->>Feed: Aviso disponible en GitHub Pages y RSS
    end

    rect rgb(245, 220, 255)
        Note over Alumno,Suscriptor: 5. NOTIFICACIÓN
        loop cada 2 minutos
            Worker->>Feed: Lee feed.xml
            Worker->>DB: Comprueba items ya vistos
            alt Aviso nuevo
                Worker->>DB: Marca como visto
                Worker->>DB: Obtiene suscripciones
                Worker->>Push: Envía notificación push
                Push-->>Suscriptor: Notificación en navegador
                Worker->>Discord: Envía mensaje con embed
            else Ya visto
                Worker->>Worker: Omite
            end
        end
    end

    rect rgb(210, 245, 245)
        Note over Alumno,Suscriptor: ALTA DE SUSCRIPTORES
        Suscriptor->>Servidor: Solicita suscripción push
        Servidor->>DB: Guarda suscripción
        Servidor->>Push: Envía confirmación
        Push-->>Suscriptor: Suscripción confirmada
    end
```
