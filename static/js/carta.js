function cerrarInstrucciones() {
    var instructions = document.getElementById("intrucciones");
    instructions.style.display = "none";
}
document.getElementById("createSeccionForm").addEventListener("submit", function (event) {
event.preventDefault();

var form = document.getElementById("createSeccionForm");
var formData = new FormData(form);

// Iterar sobre los datos del formulario y mostrarlos por consola
for (var entry of formData.entries()) {
    console.log("Campo:", entry[0]);
    console.log("Valor:", entry[1]);
}

fetch("/createSeccion", {
    method: "POST",
    body: formData
})
    .then(response => response.json())
    .then(data => {
        window.location.reload();
    })
    .catch(error => {
        console.error(error);
    });
});


var edita = ""
function editform(nombre, indice, estado) {
edita = nombre;
// Mostrar el formulario de edición
var edtiform = document.getElementById("editform");
edtiform.style.display = "flex"; // Cambiado a "block" para que sea visible

// Obtener referencia a los campos del formulario de edición
var nombreInput = document.getElementById("editNombreSeccion");
var indiceInput = document.getElementById("editIndice");
var estadoInput = document.getElementById("editEstado");

// Asignar valores actuales a los campos del formulario
nombreInput.value = nombre;
indiceInput.value = indice;
estadoInput.checked = estado; // estado debe ser un valor booleano
}
function cerrarFormulario() {
var edtiform = document.getElementById("editform");
edtiform.style.display = "none";
}
function enviarFormulario() {
var form = document.getElementById("editSeccionForm");
var formData = new FormData(form);
formData.append("edita", edita); // Agregar la variable "edita" al formulario

console.log("Formulario a enviar:", formData);
console.log(formData.get("nombre_seccion_editar"));
console.log(formData.get("indice_editar"));
console.log(formData.get("estado_editar"));

fetch("/editSeccion", {
    method: "POST",
    body: formData
})
    .then(response => response.json())
    .then(data => {
        window.location.reload();
    })
    .catch(error => {
        console.error(error);
    });
}


var eliminarButtons = document.getElementsByClassName("eliminar-btn");
for (var i = 0; i < eliminarButtons.length; i++) {
eliminarButtons[i].addEventListener("click", function () {
    var cartaId = this.getAttribute("data-seccion-id");
    var data = { cartaId: cartaId };

    console.log("Data being sent:", data); // Add this line to console log the data being sent

    fetch("/removeSeccion", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
        .catch(error => {
            console.error(error);
        });
});
}
