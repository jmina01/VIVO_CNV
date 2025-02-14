const cloud = document.getElementById("cloud");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span");
const palanca = document.querySelector(".switch");
const circulo = document.querySelector(".circulo");
const menu = document.querySelector(".menu");
const main = document.querySelector("main");

/**
 * Al cargar la página, restaurar el estado de la barra lateral
 * (mini-barra-lateral, max-barra-lateral) desde localStorage, si existe.
 */
document.addEventListener("DOMContentLoaded", () => {
  // Leer flags guardados en localStorage (pueden ser "true" o "false")
  const isMini = localStorage.getItem("sidebarIsMini") === "true";
  const isMax = localStorage.getItem("sidebarIsMax") === "true";

  // Restaurar estado "mini" (barra chica en escritorio)
  if (isMini) {
    barraLateral.classList.add("mini-barra-lateral");
    main.classList.add("min-main");
    spans.forEach((span) => {
      span.classList.add("oculto");
    });
  }

  // Restaurar estado "max" (barra abierta/cerrada en móvil)
  if (isMax) {
    barraLateral.classList.add("max-barra-lateral");
    // Ajustar iconos de menú
    menu.children[0].style.display = "none";  // menu-outline
    menu.children[1].style.display = "block"; // close-outline
  }
});

/**
 * Evento al presionar el botón de menú (el circulito de la esquina):
 * toggle de la clase "max-barra-lateral" para móvil.
 */
menu.addEventListener("click", () => {
  barraLateral.classList.toggle("max-barra-lateral");

  // Actualiza icono de menú
  if (barraLateral.classList.contains("max-barra-lateral")) {
    menu.children[0].style.display = "none";   // Ocultar "menu-outline"
    menu.children[1].style.display = "block";  // Mostrar "close-outline"
  } else {
    menu.children[0].style.display = "block";
    menu.children[1].style.display = "none";
  }

  // Si la pantalla es muy pequeña, forzamos modo mini-barra
  if (window.innerWidth <= 320) {
    barraLateral.classList.add("mini-barra-lateral");
    main.classList.add("min-main");
    spans.forEach((span) => {
      span.classList.add("oculto");
    });
    // Guardar en localStorage
    localStorage.setItem("sidebarIsMini", "true");
  } else {
    // En pantallas grandes, no forzamos el mini
    localStorage.setItem("sidebarIsMini", barraLateral.classList.contains("mini-barra-lateral"));
  }

  // Guardar en localStorage si la barra está "max" (para móvil)
  localStorage.setItem("sidebarIsMax", barraLateral.classList.contains("max-barra-lateral"));
});

/**
 * Evento al presionar el ícono "cloud" (que minimiza la barra en escritorio).
 */
cloud.addEventListener("click", () => {
  barraLateral.classList.toggle("mini-barra-lateral");
  main.classList.toggle("min-main");
  spans.forEach((span) => {
    span.classList.toggle("oculto");
  });
  // Guardar en localStorage si está mini
  localStorage.setItem("sidebarIsMini", barraLateral.classList.contains("mini-barra-lateral"));
});

/**
 * Evento para el modo oscuro (tema) - Se mantiene igual, 
 * y si quisieras conservarlo, podrías guardar en localStorage
 * de manera similar.
 */
palanca.addEventListener("click", () => {
  let body = document.body;
  body.classList.toggle("dark-mode");
  body.classList.toggle("bb");
  circulo.classList.toggle("prendido");

  // (Opcional) Si quieres guardar el modo oscuro también:
  // localStorage.setItem("darkMode", body.classList.contains("dark-mode"));
});
