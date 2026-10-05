const texto = document.getElementById("texto");
const contador = document.getElementById("contador");
texto.addEventListener("input", function () {
  const restantes = 280 - texto.value.length;
  contador.textContent = "Quedan " + restantes + " caracteres.";
  contador.classList.toggle("error", restantes < 15);
});
