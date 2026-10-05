const crear = document.getElementById("crear-lista");
const campo = document.getElementById("tarea");
const tareas = document.getElementById("tareas");
const error = document.getElementById("error");
const anadir = document.getElementById("anadir");
function comprobarLimite() {
  const lleno = tareas.children.length >= 10;
  anadir.disabled = lleno;
  error.textContent = lleno ? "Máximo de 10 tareas. Elimina una para añadir otra." : "";
}
crear.addEventListener("submit", function (evento) {
  evento.preventDefault();
  const titulo = document.getElementById("titulo").value.trim();
  if (!titulo) return;
  document.getElementById("titulo-lista").textContent = titulo;
  crear.hidden = true;
  document.getElementById("lista").hidden = false;
  campo.focus();
});
document.getElementById("anadir-tarea").addEventListener("submit", function (evento) {
  evento.preventDefault();
  if (tareas.children.length >= 10 || !campo.value.trim()) return;
  const li = document.createElement("li");
  const texto = document.createElement("span");
  texto.textContent = campo.value.trim();
  const completar = document.createElement("button");
  completar.type = "button";
  completar.textContent = "Completar";
  completar.addEventListener("click", function () {
    const completada = texto.classList.toggle("completada");
    completar.textContent = completada ? "Pendiente" : "Completar";
  });
  const eliminar = document.createElement("button");
  eliminar.type = "button";
  eliminar.textContent = "Eliminar";
  eliminar.addEventListener("click", function () {
    if (confirm("¿Quieres eliminar esta tarea?")) {
      li.remove();
      comprobarLimite();
    }
  });
  li.append(texto, completar, eliminar);
  tareas.append(li);
  campo.value = "";
  comprobarLimite();
  campo.focus();
});
