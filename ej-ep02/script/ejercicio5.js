const formulario = document.getElementById("registro");
const mensajes = document.getElementById("mensajes");
formulario.addEventListener("reset", function () {
  mensajes.replaceChildren();
});
formulario.addEventListener("submit", function (evento) {
  evento.preventDefault();
  const nombre = document.getElementById("nombre");
  const email = document.getElementById("email");
  const contrasena = document.getElementById("contrasena");
  const confirmacion = document.getElementById("confirmacion");
  const errores = [];
  if (nombre.value.trim().length < 4)
    errores.push([nombre, "Nombre: escribe al menos 4 caracteres."]);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value))
    errores.push([email, "Correo: escribe una dirección válida, como nombre@ejemplo.com."]);
  if (contrasena.value.length < 8 || !/[0-9]/.test(contrasena.value) || !/[A-Z]/.test(contrasena.value))
    errores.push([contrasena, "Contraseña: incluye al menos 8 caracteres, un número y una mayúscula."]);
  if (!confirmacion.value || confirmacion.value !== contrasena.value)
    errores.push([confirmacion, "Confirmación: repite exactamente la contraseña."]);
  mensajes.replaceChildren();
  if (errores.length) {
    const lista = document.createElement("ul");
    lista.className = "error";
    errores.forEach(function (error) {
      const li = document.createElement("li");
      li.textContent = error[1];
      lista.append(li);
    });
    mensajes.append(lista);
    errores[0][0].focus();
  } else {
    formulario.reset();
    mensajes.textContent = "Registro completado correctamente.";
    mensajes.className = "exito";
  }
});
