---
layout: post
title: Reconfiguración de Eduroam - Nuevos Parámetros de Seguridad
date: 2025-12-10 00:00:00 +0100
author: Iván
published: true
expires: 2025-12-16 23:00:01 +0100
categories:
  - Servicios UPM
excerpt: Información importante sobre la reconfiguración de Eduroam y los nuevos parámetros de seguridad que entrarán en vigor próximamente.
---
Buenas tardes a todos,
Os remitimos el correo enviado desde el Vicerrectorado.
Un saludo.

> Estimado estudiantado,
>
> El próximo martes 16 de diciembre se llevará a cabo una actualización importante en la infraestructura de la red Wifi de la Universidad que nos va a permitir mejorar la seguridad pero que podría afectar a la conexión de algunos dispositivos a la red eduroam. Concretamente el cambio se centra fundamentalmente en la gestión de los certificados.
>
> Si durante 2025 configuraste eduroam mediante alguna de las aplicaciones geteduroam o eduroam CAT no deberías experimentar ningún problema. Sin embargo, si la configuración la realizaste con anterioridad o no empleaste estas aplicaciones, es probable que el cambio afecte a alguno de tus dispositivos y no puedas conectarte a eduroam
>
> Para asegurar la continuidad del servicio, recomendamos reconfigurar eduroam antes de la fecha señalada utilizando alguna de las las herramientas indicadas:
>
>    geteduroam (https://www.eduroam.app/) para dispositivos Windows, iOS, Linux y Android
>    eduroam CAT (https://cat.eduroam.org/) para dispositivos macOS y Chrome OS
>
> Puedes consultar información adicional sobre el servicio Wi-Fi en https://www.upm.es/wifi.
>
> En caso de incidencias, te pedimos que contactes con el servicio informático de tu centro o que emplees la herramienta de soporte https://soporte.upm.es.
>
> Agradecemos tu colaboración y comprensión pero este cambio era necesario para mejorar la seguridad de nuestra red
> 
> Recibe un cordial saludo.
>
> Vicerrectorado para Universidad Digital

<!-- Modal de descarga de la app -->
<div id="download-app-modal" style="
    display:none;
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(2px);
    z-index: 9999;
">
  <div style="
        background:white;
        width: 80%;
        max-width: 350px;
        margin: 15% auto;
        padding: 20px;
        border-radius: 10px;
        text-align:center;
    ">

    <h4>Activa las notificaciones en tu navegador</h4>
    <p>Y podrás recibir avisos en cuanto se publiquen.</p>
    <p>La web puede tardar unos segundos en cargar.</p>

    <!-- Botón universal -->
    <a id="universal-link" href="https://notifierpushrss.onrender.com/"
       style="margin: 15px 0; background:#4A90E2; color:white; padding:10px; border-radius:5px; text-decoration:none; display:block;">
       Activar notificaciones
    </a>

    <button id="close-modal" style="padding:8px 20px; border:none; background:#ccc; border-radius:5px;">
      Cerrar
    </button>
  </div>
</div>

{% raw %}
<script>
// Evitar mostrar el modal más de una vez
const shown = localStorage.getItem("appModalShown");

if (!shown) {
    document.getElementById("download-app-modal").style.display = "block";
}

// Cerrar el modal
document.getElementById("close-modal").onclick = function () {
    localStorage.setItem("appModalShown", "true");
    document.getElementById("download-app-modal").style.display = "none";
};
</script>
{% endraw %}
