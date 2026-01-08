# Principales Orígenes:

- [Intercambiador de Aluche](/avisos5S2M-B/comoLlegar/aluche.html)
- [Colonia Jardín](/avisos5S2M-B/comoLlegar/colonia.html)
- [Moncloa (y Ciudad Universitaria)](/avisos5S2M-B/comoLlegar/moncloa-ciu.html)
- [Campamento](/avisos5S2M-B/comoLlegar/campamento.html)
- [Lanzadera El Barrial](/avisos5S2M-B/comoLlegar/barrial.html)
- [Príncipe Pío (temporalmente no disponible)](/avisos5S2M-B/comoLlegar/principePio.html)

<div id="estado-crtm" style="text-align:center;">
  Cargando estado del servicio…
</div>

<script>
async function cargarEstadoCRTM() {
  const contenedor = document.getElementById("estado-crtm");
  if (!contenedor) return;

  const urlCRTM =
    "https://crtm.es/comunicacion/actualidad-del-servicio/avisos/informacion-actualizada?lang=es";

  const proxyURL =
    "https://corsproxy.io/?url=" + encodeURIComponent(urlCRTM);

  try {
    const response = await fetch(proxyURL);
    const html = await response.text();

    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");

    const selector =
      "#colCentro > div > div.brdGris2 > div.cont > div:nth-child(2)";

    const divCRTM = doc.querySelector(selector);

    if (!divCRTM) {
      contenedor.innerText = "No se pudo obtener el estado del servicio";
      return;
    }

    // Clonamos para no mover nodos del documento remoto
    const clon = divCRTM.cloneNode(true);

    // Corregir rutas relativas de imágenes
    clon.querySelectorAll("img").forEach(img => {
      const src = img.getAttribute("src");
      if (src && src.trim().startsWith("/")) {
        img.src = "https://crtm.es" + src.trim();
      }
    });

    // Corregir rutas relativas de enlaces
    clon.querySelectorAll("a").forEach(a => {
      let href = a.getAttribute("href");
      if (!href) return;

      href = href.trim(); // elimina espacios y saltos de línea

      if (href.startsWith("/")) {
        a.href = "https://crtm.es" + href;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
      }
    });

    // Limpiar y agregar el contenido
    contenedor.innerHTML = "";
    contenedor.appendChild(clon);

  } catch (err) {
    console.error("Error CRTM:", err);
    contenedor.innerText = "Consulta al CRTM fallida. Recarga la web y vuelve a intentarlo,";
  }
}

// Cargar al iniciar
document.addEventListener("DOMContentLoaded", cargarEstadoCRTM);

// Auto-refresh cada 5 minutos
setInterval(cargarEstadoCRTM, 5 * 60 * 1000);
</script>