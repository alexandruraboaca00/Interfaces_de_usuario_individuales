const boton = document.getElementById("modo");
boton.addEventListener("click", function () {
  const oscuro = document.body.classList.toggle("oscuro");
  boton.textContent = oscuro ? "Cambiar a modo claro" : "Cambiar a modo oscuro";
  boton.setAttribute("aria-pressed", oscuro);
});
