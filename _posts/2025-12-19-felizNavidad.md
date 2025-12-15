---
layout: post
title: Inicio del periodo vacacional
date: 2025-12-19 19:00:00 +0100
author: Delegados
published: true
expires: 2025-12-21 23:59:59 +0100
categories:
  - Aviso de festivos
excerpt: Concluye la docencia. Felices fiestas.
---
Desde el Equipo de Delegados os deseamos felices fiestas, y os recordamos que ha concluido el 1er periodo de docencia. A la vuelta serán los exámenes, según el siguiente listado:

<embed 
    src="https://fi.upm.es/docs/estudios/grado/901_aulas_evaluacion_enero_26.pdf" 
    type="application/pdf" 
    width="100%" 
    height="400px" />

Recordad consultar regularmente el Moodle de las distintas asignaturas, para poder consultar las distintas convocatorias de exámenes.

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
