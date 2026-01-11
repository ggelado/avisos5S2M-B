---
layout: post
title: Aulas exámenes de Enero
date: 2026-01-01 00:00:00 +0100
author: Gonzalo
published: true
expires: 2026-01-26 12:00:01 +0100
categories:
- Convocatorias de Examen
excerpt: Aulas de exámenes de enero
image: https://img.freepik.com/vector-gratis/texto-estilo-logotipo-estilo-papel-2026-vispera-ano-nuevo_1017-60883.jpg?semt=ais_hybrid&w=740&q=80
---

{% raw %}
<div id="buses-simplificado" style="
  position: sticky;
  top: 0;
  z-index: 1000;
  margin-top: 8px;
  padding: 8px;
  background: white;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 0.85em;
  text-align: center;
">
  Cargando próximos transportes…
</div>
<script>

// --- Lanzaderas (L-V) ---
const SHUTTLES = [
  {
    line: "LZ-CIU",
    times: ["10:00", "11:00", "12:00", "13:00", "14:00"]
  },
  {
    line: "LZ-BARR",
    times: ["08:35", "09:15", "10:00"]
  }
];

// --- Fuentes CRTM ---
const SOURCES = [
  { url: "https://api.madridtransporte.com/stops/bus/08771/times", lines: ["571", "573", "N905"] },
  { url: "https://api.madridtransporte.com/stops/bus/08411/times", lines: ["591"] },
  { url: "https://api.madridtransporte.com/stops/bus/17573/times", lines: ["865"] },
  { url: "https://api.madridtransporte.com/stops/tram/29/planned", isTram: true }
];

// --- Utilidades ---
function minutesFromNow(ts) {
  return Math.max(0, Math.round((ts - Date.now()) / 60000));
}

function uniqueSorted(arr) {
  return [...new Set(arr)].sort((a, b) => a - b);
}

function isWeekday(date = new Date()) {
  const d = date.getDay();
  return d >= 1 && d <= 5;
}

function minutesUntilTodayTime(hhmm) {
  const [h, m] = hhmm.split(":").map(Number);
  const now = new Date();
  const t = new Date();
  t.setHours(h, m, 0, 0);
  return Math.round((t - now) / 60000);
}

// --- Actualización principal ---
async function actualizarBusesSimplificados() {
  const contenedor = document.getElementById("buses-simplificado");
  if (!contenedor) return;

  try {
    const results = [];

    // --- CRTM ---
    for (const source of SOURCES) {
      try {
        const res = await fetch(source.url);
        const data = await res.json();

        // Metro Ligero
        if (source.isTram) {
          for (const a of data) {
            if (a.direction !== 2) continue;
            uniqueSorted(a.arrives || []).forEach(ts => {
              results.push({
                line: a.lineCode,
                minutes: minutesFromNow(ts)
              });
            });
          }
          continue;
        }

        // Buses
        for (const a of data.arrives || []) {
          if (source.lines && !source.lines.includes(a.line)) continue;
          uniqueSorted(a.estimatedArrives || []).forEach(ts => {
            results.push({
              line: a.line,
              minutes: minutesFromNow(ts)
            });
          });
        }
      } catch (_) {}
    }

    // --- Lanzaderas ---
    if (isWeekday()) {
      SHUTTLES.forEach(s => {
        s.times.forEach(t => {
          const min = minutesUntilTodayTime(t);
          if (min > 0 && min <= 60) {
            results.push({
              line: s.line,
              minutes: min
            });
          }
        });
      });
    }

    // --- Render ---
    const sorted = results.sort((a, b) => a.minutes - b.minutes).slice(0, 10);

    if (!sorted.length) {
      contenedor.textContent = "No hay servicios próximos";
      return;
    }

    contenedor.innerHTML = sorted
      .map(b => `<span><strong>${b.line}</strong>: <span class="bus-time">${b.minutes}'</span></span>`)
      .join(" · ");

  } catch (e) {
    contenedor.textContent = "API CRTM caída. Actualiza la web.";
  }
}

// --- Arranque ---
document.addEventListener("DOMContentLoaded", () => {
  actualizarBusesSimplificados();
  setInterval(actualizarBusesSimplificados, 60000);
});
</script>

{% endraw %}


Feliz año.

Y como regalo de año nuevo, la lista de aulas de los exámenes:

<embed 
    src="https://fi.upm.es/docs/estudios/grado/901_aulas_evaluacion_enero_26.pdf" 
    type="application/pdf" 
    width="100%" 
    height="400px" />

A través del Moodle de las diferentes asignaturas se publicarán las convocatorias de los exámenes. Para evitar colapsar a avisos, no enviaré un aviso por cada convocatoria, sino que editaré este mismo aviso. Tu lector RSS podría no reflejar estas actualizaciones, por lo que se recomienda la consulta [de este aviso en su versión web](#).

Si dispones de suscripción activa a las [notificaciones push](https://notifierpushrss.onrender.com/), se enviarán notificaciones y recordatorios ante eventos relevantes, p.ej. las aulas momentos antes de un examen importante y obligatorio.

No curso todas las optativas, así que si quieres colaborar publicando las convocatorias de los distintos exámenes, puedes hacerlo [desde aquí](https://github.com/ggelado/avisos5S2M-B/edit/main/_posts/2026-01-01-examenesEnero.md).

<p style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 8px; border: 1px solid #ffeeba; font-weight: bold; font-size: 1.1em;">
<span style="text-decoration: underline;">AVISO:</span> 
  La información aquí mostrada es con carácter informativo, y podría estar desactualizada. LA ÚNICA INFORMACIÓN OFICIAL ES LA PUBLICADA MEDIANTE LOS CANALES DE COMUNICACIÓN DE LAS DISTINTAS ASIGNATURAS.
</p>

# Inteligencia Artificial

- Viernes 9 de enero a las 15:00. Presencial. En papel.
- Contenidos:
  - Todos los alumnos: temas 4 y 5. Necesaria una calificación de al menos 0.5 sobre 3.
  - Adicionalmente, temas 1 y 2 para aquellos que no hayan alcanzado la calificación de 0.5 puntos sobre 3 en el examen de evaluación progresiva.
  - Opcionalmente, temas 1 y 2 para aquellos con una calificación igual o superior a 0.5 puntos pero que no hayan alcanzado 1.5 puntos sobre 3 en el examen de evaluación progresiva. Prevalece la calificación de este examen sobre la calificación anterior, debiendo el alumno alcanzar la calificación de 0.5 puntos sobre 3 para poder aprobar la asignatura en esta convocatoria. 
- **Aulas: distribución por apellidos.** 
  - DE: ACITORES HASTA: FERRER. Aula 3102-3103.
  - DE: FIGUEROA HASTA: LLAMAS. Aula 3104.
  - DE: LOPEZ HASTA: ZHUANG. Aula 3001 exámenes.
1. Antes de comenzar el reparto de los ejercicios, únicamente puede haber en la mesa una calculadora, un bolígrafo azul o negro y un documento de identificación personal.
2. Se podrá utilizar una calculadora del tipo permitido en las pruebas de evaluación de acceso a la Universidad en la Comunidad de Madrid ([https://evau.info/lista-calculadoras-evau-madrid/](https://evau.info/lista-calculadoras-evau-madrid/)). En especial, que no transmita datos, que no sea programable, que no tenga pantalla gráfica y que no almacene datos alfanuméricos.
3. Si durante el desarrollo de la prueba de evaluación fuera necesario el uso de material adicional (una hoja en blanco, un bolígrafo adicional, etc.), deberá solicitarse al profesor encargado del aula.
4. Los bolsos, abrigos, mochilas, carpetas, apuntes, estuches, dispositivos electrónicos, etc. deberán estar fuera de la mesa (incluida la cajonera).
5. Los dispositivos electrónicos tales como teléfonos móviles, tabletas, relojes, inteligentes, lápices digitales, auriculares o cualquier instrumento de naturaleza análoga deberán permanecer apagados durante el desarrollo de la prueba.

<div style="background-color: yellow; color: red; font-size: 24px; font-weight: bold; padding: 15px; border: 2px solid red; text-align: center;">
    RECUERDA QUE NO ESTÁ PERMITIDA CUALQUIER CALCULADORA. Algunos ejemplos de <u>CALCULADORAS NO PERMITIDAS</u>.
</div>

<div style="display:flex; flex-wrap:wrap; width:100%;">

<div style="position:relative; width:50%; overflow:hidden;">
    <img src="https://m.media-amazon.com/images/I/71mTdxjO9cL._AC_SL1500_.jpg" style="width:100%; display:block;">
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(45deg); transform-origin:center;"></div>
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(-45deg); transform-origin:center;"></div>
  </div>

<div style="position:relative; width:50%; overflow:hidden;">
    <img src="https://m.media-amazon.com/images/I/514Kel0a1xL._AC_SL1000_.jpg" style="width:100%; display:block;">
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(45deg); transform-origin:center;"></div>
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(-45deg); transform-origin:center;"></div>
  </div>

<div style="position:relative; width:50%; overflow:hidden;">
    <img src="https://m.media-amazon.com/images/I/71PcaRiFl6L._AC_SL1500_.jpg" style="width:100%; display:block;">
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(45deg); transform-origin:center;"></div>
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(-45deg); transform-origin:center;"></div>
  </div>

<div style="position:relative; width:50%; overflow:hidden;">
    <img src="https://m.media-amazon.com/images/I/61v44oHp1cL._AC_SL1500_.jpg" style="width:100%; display:block;">
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(45deg); transform-origin:center;"></div>
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(-45deg); transform-origin:center;"></div>
  </div>

<div style="position:relative; width:50%; overflow:hidden;">
    <img src="https://m.media-amazon.com/images/I/71ryiGtcr5L._AC_SL1500_.jpg" style="width:100%; display:block;">
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(45deg); transform-origin:center;"></div>
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(-45deg); transform-origin:center;"></div>
  </div>

<div style="position:relative; width:50%; overflow:hidden;">
    <img src="https://m.media-amazon.com/images/I/61EZKZc1R8L._AC_SL1001_.jpg" style="width:100%; display:block;">
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(45deg); transform-origin:center;"></div>
    <div style="position:absolute; top:50%; left:-30%; width:160%; height:6px; background:red; transform:rotate(-45deg); transform-origin:center;"></div>
  </div>

</div>
<div style="
    background-color: #ff0000; 
    color: #ffffff; 
    font-size: 32px; 
    font-weight: bolder; 
    padding: 25px; 
    border: 4px solid #ffff00; 
    text-align: center; 
    text-transform: uppercase; 
    box-shadow: 0 0 20px #ffff00;
    animation: blink 1s step-start 0s infinite;
">
    ESTOS SON EJEMPLOS DE CALCULADORAS <u>NO PERMITIDAS</u>
</div>

# Sistemas Operativos

13 de enero. Más info [https://laurel.datsi.fi.upm.es/~ssoo/RepartoAulas/SO/](https://laurel.datsi.fi.upm.es/~ssoo/RepartoAulas/SO/).

<table border="1">
<tbody><tr><th>Instrucciones para los Estudiantes</th></tr>
<tr><td><ul>
	<li>No se permite el uso del móvil. Deberá mantenerlo apagado y fuera de la vista/acceso.</li>
	<li>Deberá poner visible sobre la mesa <b>documentación acreditativa de su identidad</b>.</li>
	<li>Deberá identificarse en la cabecera de cada hoja: Nombre, Apellidos, DNI y número de hoja sobre hojas en total.</li>
	<li>Deberá identificarse en los Tests. Su DNI y la CLAVE de examen son fundamentales para poder corregir.</li>
	<li>Si necesita justificante solicíteselo al profesor durante la prueba.</li>
	<li>Para el Examen Final podrá utilizar como material de consulta solamente los resúmenes manuscritos de los temas para los que en el pasado haya ganado el visado (y no lo haya perdido por comportamiento fraudulento).</li>
</ul></td></tr>
</tbody></table>

## Examen final de semestre

16 horas

<iframe frameborder="0" width="100%" height="500px" src="https://laurel.datsi.fi.upm.es/~ssoo/RepartoAulas/SO/aula-alumno-EFS.cgi" scrolling="auto" border="0" valign="top" target="_blank" name="listado" id="listadoEFS">
<A href="aula-alumno.cgi"           >Listado de alumnos</A>
</iframe>


## Examen del minishell

15 horas

<table border="1" id="asignacion">
<tbody><tr><th>Asignación de asiento por alumno para la Pr3</th></tr>
<tr><td>

	Sólo podrán accecer a la Pr3 aquellos alumnos <b>con un 1 en la columna DrchPr3</b>
	de la lista <a href="https://laurel.datsi.fi.upm.es/~ssoo/consultaBD.cgi?Asig=ssooX&amp;Curs=2025A&amp;Conv=Jul&amp;Tipo=prac">
	Calificación Prácticas Diseño y Análisis a Julio 2025 </a>.<br>

	Siéntese en el asiento que le corresponde según el <a href="#listado">listado de alumnos</a> adjunto.<br>
	<font color="red"><b>
	Si NO aparece en esta lista entonces NO tiene asiento asignado y por lo tanto NO podría acceder a la prueba.<br>
	Vuelva a consultar su asiento asignado antes de la prueba pues podría haber cambios de última hora.
	</b></font><br>
</td></tr>
</tbody></table>

<iframe frameborder="0" width="100%" height="500px" src="https://laurel.datsi.fi.upm.es/~ssoo/RepartoAulas/SO/aula-alumno.cgi" scrolling="auto" border="0" valign="top" target="_blank" name="listado" id="listado">
<A href="aula-alumno.cgi"           >Listado de alumnos</A>
</iframe>



# Tecnologías de Red Cisco CCNA

GII 105000087 Tecnologías de Red Cisco: CCNA 7º 10:00 Salas El Monje y Los Verdes

# Fundamentos de Videojuegos

GII 105001044 Fundamentos de Videojuegos 5º 15:00 Bloque 3 aula 3204

# Building Up Comunication Skills

GII 105000046 Building up Communications Skills 5º 15:00 Bloque 5 aula 5002

# Español para Extranjeros

105001046 Español para Extranjeros 7º 10:00 Bloque 6 aula 6001

# NOTIFICACIONES PUSH

RECUERDA ACTIVAR LAS NOTIFICACIONES PUSH [DESDE AQUÍ](https://notifierpushrss.onrender.com/), PARA PODER RECIBIR LO ANTES POSIBLE CUALQUIER NOVEDAD O INFORMACIÓN IMPORTANTE. LLEGAN INSTANTÁNEAMENTE DESDE QUE SE ENVÍAN.

SE INTENTAN ENVIAR POCOS AVISOS PARA EVITAR SATURAR, PERO SIEMPRE PUEDES DARLOS DE BAJA.

Ya no se encuentran en estado beta.
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
document.addEventListener("DOMContentLoaded", function() {
  // Selecciona todos los h1
  const allH1 = document.querySelectorAll("h1");

  // Ignora el primero y aplica a todos los demás
  allH1.forEach((h1, index) => {
    if (index === 0 || index === allH1.length - 1) return; // Saltar el primer y último h1

    // Crea un contenedor para todo el contenido hasta el siguiente h1
    let container = document.createElement("div");
    container.style.display = "none";
    container.style.marginLeft = "20px";

    // Mueve todo lo que esté después del h1 hasta el siguiente h1 dentro del container
    let next = h1.nextElementSibling;
    while (next && next.tagName !== "H1") {
      let temp = next.nextElementSibling;
      container.appendChild(next);
      next = temp;
    }

    h1.insertAdjacentElement("afterend", container);

    // Agrega símbolo de flecha
    h1.textContent = "► " + h1.textContent;

    // Evento click para mostrar/ocultar
    h1.style.cursor = "pointer";
    h1.addEventListener("click", () => {
      if (container.style.display === "none") {
        container.style.display = "block";
        h1.textContent = "▼ " + h1.textContent.replace(/^►\s*/, "");
      } else {
        container.style.display = "none";
        h1.textContent = "► " + h1.textContent.replace(/^▼\s*/, "");
      }
    });
  });
});
</script>
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
