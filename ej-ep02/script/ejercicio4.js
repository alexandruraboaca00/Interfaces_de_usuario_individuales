const busqueda = document.getElementById("busqueda");
const productos = document.querySelectorAll(".producto");
busqueda.addEventListener("input", function () {
  const filtro = busqueda.value.toLocaleLowerCase("es");
  productos.forEach(function (producto) {
    const titulo = producto.querySelector("h2").textContent.toLocaleLowerCase("es");
    producto.hidden = !titulo.includes(filtro);
  });
});
