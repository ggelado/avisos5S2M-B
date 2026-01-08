<section class="container-lg my-4">
  <div id="status" class="text-small color-fg-muted mb-2"></div>

  <div class="Box">
    <div class="Box-body p-0">
      <ul id="arrivals" class="list-style-none m-0"></ul>
    </div>
  </div>
</section>

<script>
// --- Lanzaderas (horario fijo, L-V) ---
const SHUTTLES = [
  {
    line: "LZ-BARR",
    destination: "El Barrial – CC Pozuelo → Campus de Montegancedo (SOLO DÍAS LECTIVOS)",
    times: ["08:15", "09:00", "09:45"]
  }
];

const arrivalsEl = document.getElementById("arrivals");
const statusEl = document.getElementById("status");

function isWeekday(date = new Date()) {
  const d = date.getDay();
  return d >= 1 && d <= 5; // L-V
}

function minutesUntilTodayTime(hhmm) {
  const [h, m] = hhmm.split(":").map(Number);
  const now = new Date();
  const t = new Date();
  t.setHours(h, m, 0, 0);
  return Math.round((t - now) / 60000);
}

function loadShuttles() {
  const results = [];

  if (!isWeekday()) return results;

  SHUTTLES.forEach(shuttle => {
    shuttle.times.forEach(time => {
      const minutes = minutesUntilTodayTime(time);
      if (minutes > 0 && minutes <= 90) {
        results.push({
          line: shuttle.line,
          destination: shuttle.destination,
          minutes
        });
      }
    });
  });

  return results.sort((a, b) => a.minutes - b.minutes);
}

function render(arrivals) {
  arrivalsEl.innerHTML = "";

  if (!arrivals.length) {
    arrivalsEl.innerHTML =
      "<li class='Box-row text-small color-fg-muted'>No hay lanzaderas en los próximos 90 minutos</li>";
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
        <span class="Label Label--accent">${a.minutes} min</span>
      </div>
    `;
    arrivalsEl.appendChild(li);
  });
}

function refresh() {
  statusEl.textContent = "Actualizando…";
  const arrivals = loadShuttles();
  render(arrivals);
  statusEl.textContent =
    "Actualizado " + new Date().toLocaleTimeString() + ". Horario programado.";
}

refresh();
setInterval(refresh, 60000);
</script>
