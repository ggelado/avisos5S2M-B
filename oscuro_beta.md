---
layout: default
title: Modo Oscuro Beta
sitemap: false
---

<style>
.beta-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 24px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.beta-header {
  text-align: center;
  margin-bottom: 32px;
}

.beta-header h1 {
  font-size: 2em;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.beta-badge {
  display: inline-block;
  background: rgba(139, 157, 255, 0.15);
  color: var(--link-color);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75em;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: 1px solid rgba(139, 157, 255, 0.3);
}

.beta-description {
  font-size: 1em;
  line-height: 1.7;
  color: var(--text-secondary);
  margin-bottom: 32px;
}

.beta-status {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 20px;
  margin-bottom: 24px;
  text-align: center;
}

.status-label {
  font-size: 0.85em;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 8px;
  font-weight: 600;
}

.status-value {
  font-size: 1.5em;
  font-weight: 700;
  margin-bottom: 4px;
}

.status-active {
  color: var(--accent-success);
}

.status-inactive {
  color: var(--text-muted);
}

.beta-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.beta-button {
  width: 100%;
  padding: 14px 24px;
  border-radius: var(--radius-md);
  font-size: 1em;
  font-weight: 600;
  font-family: var(--font-body);
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  box-shadow: var(--shadow-sm);
}

.beta-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-activate {
  background: linear-gradient(135deg, #5c7cfa 0%, #4c63d2 100%);
  color: #ffffff;
}

.btn-activate:hover {
  background: linear-gradient(135deg, #748dd6 0%, #3d4fb8 100%);
}

.btn-deactivate {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-deactivate:hover {
  background: var(--bg-secondary);
  border-color: var(--accent-danger);
  color: var(--accent-danger);
}

.beta-features {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

.beta-features h3 {
  font-size: 1.1em;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.beta-features ul {
  list-style: none;
  padding: 0;
}

.beta-features li {
  padding: 8px 0;
  padding-left: 28px;
  position: relative;
  color: var(--text-secondary);
  line-height: 1.6;
}

.beta-features li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: var(--accent-success);
  font-weight: bold;
  font-size: 1.1em;
}

.beta-note {
  margin-top: 24px;
  padding: 12px 16px;
  background: rgba(245, 158, 11, 0.1);
  border-left: 3px solid var(--accent-warning);
  border-radius: var(--radius-sm);
  font-size: 0.9em;
  color: var(--text-secondary);
}

.beta-note strong {
  color: var(--accent-warning);
}
</style>

<div class="beta-container">
  <div class="beta-header">
    <h1>🌙 Modo Oscuro</h1>
    <span class="beta-badge">Beta</span>
  </div>

  <div class="beta-description">
    <p>
      Bienvenido al programa beta del modo oscuro. Al activarlo, experimentarás una versión 
      completamente rediseñada del sitio con una paleta de colores oscura que es más cómoda 
      para tus ojos en entornos con poca luz.
    </p>
  </div>

  <div class="beta-status">
    <div class="status-label">Estado Actual</div>
    <div class="status-value" id="currentStatus">
      Cargando...
    </div>
  </div>

  <div class="beta-actions">
    <button id="activateBtn" class="beta-button btn-activate" onclick="activateBeta()">
      🌙 Activar Modo Oscuro Beta
    </button>
    <button id="deactivateBtn" class="beta-button btn-deactivate" onclick="deactivateBeta()" style="display: none;">
      ☀️ Desactivar Modo Oscuro
    </button>
  </div>

  <div class="beta-features">
    <h3>✨ Características</h3>
    <ul>
      <li>Paleta de colores oscura diseñada para reducir la fatiga visual</li>
      <li>Logos e iconos optimizados para modo oscuro</li>
      <li>Contraste mejorado para mejor legibilidad</li>
      <li>Animaciones y transiciones suaves</li>
      <li>Compatible con todos los widgets y funcionalidades</li>
    </ul>
  </div>

  <div class="beta-note">
    <strong>Nota:</strong> Esta es una versión beta. Si encuentras algún problema visual o de 
    usabilidad, por favor repórtalo. El modo oscuro se guarda en tu navegador y permanecerá 
    activo en futuras visitas.
  </div>
</div>

<script>
const DARK_MODE_KEY = 'darkModeBeta';

function isDarkModeActive() {
  return localStorage.getItem(DARK_MODE_KEY) === 'true';
}

function updateUI() {
  const isActive = isDarkModeActive();
  const statusEl = document.getElementById('currentStatus');
  const activateBtn = document.getElementById('activateBtn');
  const deactivateBtn = document.getElementById('deactivateBtn');

  if (isActive) {
    statusEl.textContent = '✓ Activado';
    statusEl.className = 'status-value status-active';
    activateBtn.style.display = 'none';
    deactivateBtn.style.display = 'block';
  } else {
    statusEl.textContent = '○ Inactivo';
    statusEl.className = 'status-value status-inactive';
    activateBtn.style.display = 'block';
    deactivateBtn.style.display = 'none';
  }
}

function activateBeta() {
  localStorage.setItem(DARK_MODE_KEY, 'true');
  
  // Mostrar mensaje de confirmación
  alert('🌙 Modo Oscuro activado!\n\nLa página se recargará para aplicar los cambios.');
  
  // Recargar la página
  window.location.reload();
}

function deactivateBeta() {
  if (confirm('¿Estás seguro que deseas desactivar el modo oscuro?')) {
    localStorage.removeItem(DARK_MODE_KEY);
    
    // Mostrar mensaje de confirmación
    alert('☀️ Modo Oscuro desactivado!\n\nLa página se recargará para aplicar los cambios.');
    
    // Recargar la página
    window.location.reload();
  }
}

// Actualizar UI al cargar
document.addEventListener('DOMContentLoaded', updateUI);
</script>
