        // Obtener todos los elementos con la clase "changeunicjs"
        var elementos = document.querySelectorAll('.changeunicjs');

        // Iterar sobre cada elemento
        elementos.forEach(function (elemento) {
            // Verificar si el texto del elemento es "Activo"
            if (elemento.textContent.trim() === 'Activa') {
                // Cambiar el ID del elemento a "unic"
                elemento.setAttribute('id', 'acti');
            } else {
                // Cambiar el ID del elemento a "unic"
                elemento.setAttribute('id', 'inac');
            }
        });
var edita = ""
function editform(nombre, indice, estado) {
    edita = nombre;
    // Mostrar el formulario de edición
    var edtiform = document.getElementById("editform");
    edtiform.style.display = "block"; // Cambiado a "block" para que sea visible

    // Obtener referencia a los campos del formulario de edición
    var nombreInput = document.getElementById("editNombreCarta");
    var indiceInput = document.getElementById("editIndice");
    var estadoInput = document.getElementById("editEstado");

    // Asignar valores actuales a los campos del formulario
    nombreInput.value = nombre;
    indiceInput.value = indice;
    estadoInput.checked = estado; // estado debe ser un valor booleano
}

function enviarFormulario() {
    var form = document.getElementById("editCartaForm");
    var formData = new FormData(form);
    formData.append("edita", edita); // Agregar la variable "edita" al formulario

    console.log("Formulario a enviar:", formData);
    fetch("/editCarta", {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Hubo un error al enviar el formulario.");
            }
            window.location.reload();
            return response.json();
        })
        .then(data => {
            window.location.reload();
        })
        .catch(error => {
            console.error("Error al enviar el formulario:", error);
        });
}

var eliminarButtons = document.getElementsByClassName("eliminar-btn");
for (var i = 0; i < eliminarButtons.length; i++) {
    eliminarButtons[i].addEventListener("click", function () {
        var cartaId = this.getAttribute("data-carta-id");
        var data = { cartaId: cartaId };

        console.log("Data being sent:", data); // Add this line to console log the data being sent

        fetch("/removeCarta", {
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


document.getElementById("createCartaForm").addEventListener("submit", function (event) {
    event.preventDefault();

    var form = document.getElementById("createCartaForm");
    var formData = new FormData(form);

    // Iterar sobre los datos del formulario y mostrarlos por consola
    for (var entry of formData.entries()) {
        console.log("Campo:", entry[0]);
        console.log("Valor:", entry[1]);
    }

    fetch("/createCarta", {
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