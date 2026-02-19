---
permalink: /poblados
title: Atascos Av. Poblados
sitemap: false
---
<section>
  <p>Última actualización: <span id="ultima-actualizacion">Cargando…</span></p>
  <p>Constan posibles retenciones / atascos en: (datos obtenidos del Ayto de Madrid)</p>
  <ul id="lista-atascos">
    <li>Cargando información (puede tardar varios minutos)…</li>
  </ul>
</section>

<script>
async function cargarAtascosPoblados() {
  const ul = document.getElementById('lista-atascos');
  const updateEl = document.getElementById('ultima-actualizacion');

  try {
    const res = await fetch('https://notifierpushrss.onrender.com/api/poblados');
    if (!res.ok) throw new Error(`HTTP status ${res.status}`);
    const data = await res.json();

    // Mostrar timestamp
    updateEl.textContent = data.ultimaActualizacion || 'Desconocida';

    // Si no hay atascos
    if (!data.hayAtascos || !data.atascos || data.atascos.length === 0) {
      ul.innerHTML = '<li>No hay datos registrados.</li>';
      return;
    }

    // Listar atascos
    ul.innerHTML = '';
    data.atascos.forEach(atasco => {
      const li = document.createElement('li');
      li.textContent = `${atasco.descripcion}`
      ul.appendChild(li);
    });

  } catch (err) {
    console.error('Error cargando atascos:', err);
    ul.innerHTML = '<li>No se pudo cargar la información.</li>';
    updateEl.textContent = 'Error';
  }
}

// Ejecutar al cargar la página y refrescar cada 2 minutos
document.addEventListener('DOMContentLoaded', () => {
  cargarAtascosPoblados();
  setInterval(cargarAtascosPoblados, 120000);
});
</script>
