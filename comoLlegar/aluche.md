<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<style>
/* Fix para los marcadores de Leaflet */
.markdown-body .leaflet-marker-icon,
.markdown-body .leaflet-marker-shadow {
    background-color: transparent !important;
}
</style>

<section class="container-lg my-4">

<div id="status" class="text-small color-fg-muted mb-2"></div>

<div class="Box">
    <div class="Box-body p-0">
      <ul id="arrivals" class="list-style-none m-0"></ul>
    </div>
  </div>
</section>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>


(() => {
  // --- Paradas de referencia por línea ---
  const LINE_STOPS = {
    "8__571___": "15782",
    "8__591___": "08380"
  };

  const SOURCES = [
    { url: "https://api.madridtransporte.com/stops/bus/15782/times", lines: ["571"] },
    { url: "https://api.madridtransporte.com/stops/bus/08380/times", lines: ["591"] }
  ];

  const arrivalsEl = document.getElementById("arrivals");
  const statusEl = document.getElementById("status");
  const maps = {};

  function minutesFromNow(ts) {
    return Math.max(0, Math.round((ts - Date.now()) / 60000));
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

  function uniqueSorted(arr) {
    return [...new Set(arr)].sort((a, b) => a - b);
  }

  // --- Cargar próximas llegadas ---
  async function loadArrivals() {
    const results = [];

    for (const source of SOURCES) {
      try {
        const res = await fetch(source.url);
        const data = await res.json();

        for (const arrival of data.arrives || []) {
          if (source.lines && !source.lines.includes(arrival.line)) continue;
          uniqueSorted(arrival.estimatedArrives || []).forEach(ts => {
            results.push({
              line: arrival.line,
              lineCode: arrival.lineCode,
              destination: arrival.destination,
              minutes: minutesFromNow(ts),
              isTram: false
            });
          });
        }
      } catch (e) {
        console.error("Error cargando", source.url, e);
      }
    }

    const sorted = results.sort((a, b) => a.minutes - b.minutes);


    const busArrivals = sorted.filter(a => !a.isTram);

    return [...busArrivals]
      .sort((a, b) => a.minutes - b.minutes);
  }

  // --- Ubicación de buses ---
  async function loadBusLocations(lineCode) {
    const stopCode = LINE_STOPS[lineCode];
    if (!stopCode) return [];

    const url = `https://api.madridtransporte.com/lines/bus/${lineCode}/locations/2?stopCode=${stopCode}`;
    try {
      const res = await fetch(url);
      const data = await res.json();
      return data.locations || [];
    } catch (e) {
      console.error("Error cargando ubicación", lineCode, e);
      return [];
    }
  }

  function createMap(container, locations) {
    const map = L.map(container).setView(
      [locations[0].coordinates.latitude, locations[0].coordinates.longitude],
      13
    );

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap"
    }).addTo(map);

    return map;
  }

  function renderBuses(map, markers, locations) {
    markers.forEach(m => m.remove());
    markers.length = 0;

    locations.forEach(bus => {
      const m = L.marker([bus.coordinates.latitude, bus.coordinates.longitude])
        .addTo(map)
        .bindPopup(`
          <strong>Bus ${bus.codVehicle}</strong><br>
          Servicio: ${bus.service || "—"}
        `);
      markers.push(m);
    });

    if (markers.length) {
      const group = L.featureGroup(markers);
      map.fitBounds(group.getBounds().pad(0.25));
    }
  }

  async function toggleMap(btn) {
    const lineCode = btn.dataset.linecode;
    const container = document.getElementById(`map-${lineCode}`);

    if (container.classList.contains("d-none")) {
      container.classList.remove("d-none");
      btn.textContent = "Ocultar mapa";

      if (!maps[lineCode]) {
        const locations = await loadBusLocations(lineCode);
        if (!locations.length) {
          container.innerHTML = "<div class='p-3 text-small'>No hay buses en ruta</div>";
          return;
        }

        const map = createMap(container, locations);
        const markers = [];
        renderBuses(map, markers, locations);

        maps[lineCode] = { map, markers };
      }
    } else {
      container.classList.add("d-none");
      btn.textContent = "Ver ubicación (beta)";
    }
  }

  function render(arrivals) {
    arrivalsEl.innerHTML = "";

    if (!arrivals.length) {
      arrivalsEl.innerHTML =
        "<li class='Box-row text-small color-fg-muted'>No hay servicios próximos</li>";
      return;
    }

    arrivals.forEach(a => {
      const li = document.createElement("li");
      li.className = "Box-row";

      li.innerHTML = `
        <div class="d-flex flex-justify-between flex-items-center">
          <div>
            <strong>${a.line}</strong>
            <span class="color-fg-muted">→ ${a.destination}</span>
          </div>
          <div class="text-right">
            <span class="Label Label--accent mr-2">${a.minutes} min</span>
            ${(a.isTram) ? "" :
              `<button class="btn btn-sm btn-outline" data-linecode="${a.lineCode}">
                Ver ubicación (beta)
              </button>`}
          </div>
        </div>
        ${(a.isTram) ? "" :
          `<div id="map-${a.lineCode}" class="d-none mt-2"
                style="height:300px;border-radius:6px;"></div>`}
      `;

      arrivalsEl.appendChild(li);
    });
  }

  arrivalsEl.addEventListener("click", e => {
    if (e.target.tagName === "BUTTON") toggleMap(e.target);
  });

  async function refresh() {
    statusEl.textContent = "Actualizando…";
    const arrivals = await loadArrivals();
    render(arrivals);
    statusEl.textContent =
      "Actualizado " + new Date().toLocaleTimeString() +
      ". Es la API del CRTM, puede fallar.";
  }

  refresh();
  setInterval(refresh, 60000);
})();
</script>
