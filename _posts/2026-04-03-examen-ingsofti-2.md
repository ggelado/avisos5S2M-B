---
layout: post
title: Examen IngSoft I
date: 2026-04-03 00:00:00 +0200
author: Gonzalo
published: true
event_date: 2026-04-08 12:00:00 +0200
expires: 2026-04-08 14:00:00 +0200
categories:
  - Convocatorias de Examen
  - IngSoftI
excerpt: Examen 8 de abril IngSoft I
image: https://www.dlsiis.fi.upm.es/imagenes/lsiis.png
---

Recuerda que el próximo día 8 de abril a las 12:00 es el examen de Ingeniería del Software I. 

<ul>
<li><strong>Nerja</strong> (bloque IV): de <strong>Acitones Rich</strong> a <strong>Franco González</strong></li>
<li><strong>Del Monje</strong> (bloque IV): de <strong>Garabán Gil</strong> a <strong>Juaranz Dominguez</strong></li>
<li><strong>Los Verdes</strong> (bloque IV): de <strong>Labzae</strong> a <strong>Rodríguez Jimenez</strong></li>
<li><strong>Artá</strong> (bloque VI, planta baja): de <strong>Rojas Castaño</strong> a <strong>Valdés Briales</strong></li>
<li><strong>Altamira</strong> (bloque V): de <strong>Valera Díaz</strong> a <strong>Zhou</strong></li>
</ul>

<input type="text" id="apellido" placeholder="Escribe tu primer apellido" />
<p id="resultado"></p>

<script>
  // Datos de los grupos del miércoles 4 de marzo
  const aulas = [
    { aula: "Nerja (bloque IV)", rango: ["Acitones Rich", "Franco González"] },
    { aula: "Del Monje (bloque IV)", rango: ["Garabán Gil", "Juaranz Dominguez"] },
    { aula: "Los Verdes (bloque IV)", rango: ["Labzae", "Rodríguez Jimenez"] },
    { aula: "Artá (bloque VI, planta baja)", rango: ["Rojas Castaño", "Valdés Briales"] },
    { aula: "Altamira (bloque V)", rango: ["Valera Díaz", "Zhou"] }
  ];

  const resultado = document.getElementById("resultado");
  const input = document.getElementById("apellido");

  input.addEventListener("input", () => {
    const valor = input.value.trim().toLowerCase();

    if (!valor) {
      resultado.textContent = "";
      return;
    }

    // Buscar aula según el primer apellido
    let encontrado = null;
    for (const a of aulas) {
      const inicio = a.rango[0].toLowerCase();
      const fin = a.rango[1].toLowerCase();
      if (valor >= inicio && valor <= fin) {
        encontrado = a.aula;
        break;
      }
    }

    resultado.textContent = encontrado 
      ? `Tu aula es: ${encontrado}` 
      : "Sigue escribiendo";
  });
</script>
