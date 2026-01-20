---
layout: post
author: decanato
categories:
  - SAI
date: 2026-01-19T23:00:00
title: Listado de estudiantes con calificación de aptos en la prueba SAI
expires: 2026-01-21 23:59:00 +0100
excerpt: Publicado listado oficial de aptos
published: true
---
Han sido considerados aptos en la prueba SAI los siguientes alumnos en todo el Grado en Ingeniería Informática. Los alumnos de GII que no están aquí listados y comparecieron el pasado 11 de diciembre NO HAN SIDO CONSIDERADOS APTOS.

08122145 54979457 UB6707294 54348944 54965602 50358381 06023814 11899751 OL4160806 05953533 55026899 03536223 50375218 54268745 03179508 AH6428724 70084515 51123960 02742889 49422964 02563379 48282253 53954796 54298992 11867980 06645182 11852710 53657822 02566391 11867328 54713625 54023638 55312782 05954001 47226622 08006901 02597533 50775596 18547947 03169493 51803669 49156348 55202574 X9971399 53955000 03502979 02785734 04262489 ZJ6951484 50241764 53720706 54890793 49308045 77022150 61020751 X8535492 Y0540193 X6424303

<input type="text" id="alumno" placeholder="Introduce el número de alumno">
<button onclick="buscarAlumno()">Buscar</button>
<p id="resultado"></p>

(*Puedes inspeccionar el código fuente de la web con CRTL+U, no se guarda ningún dato*)

<script>
  // Lista de alumnos aptos
  const alumnosAptos = [
    "08122145","54979457","UB6707294","54348944","54965602","50358381",
    "06023814","11899751","OL4160806","05953533","55026899","03536223",
    "50375218","54268745","03179508","AH6428724","70084515","51123960",
    "02742889","49422964","02563379","48282253","53954796","54298992",
    "11867980","06645182","11852710","53657822","02566391","11867328",
    "54713625","54023638","55312782","05954001","47226622","08006901",
    "02597533","50775596","18547947","03169493","51803669","49156348",
    "55202574","X9971399","53955000","03502979","02785734","04262489",
    "ZJ6951484","50241764","53720706","54890793","49308045","77022150",
    "61020751","X8535492","Y0540193","X6424303"
  ];

  function buscarAlumno() {
    const input = document.getElementById('alumno').value.trim();
    const resultado = document.getElementById('resultado');

    if (alumnosAptos.includes(input)) {
      resultado.textContent = "APTO";
      resultado.style.color = "green";
    } else {
      resultado.textContent = "El alumno NO ESTÁ en la lista de aptos en GII";
      resultado.style.color = "red";
    }
  }
</script>
