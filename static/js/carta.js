function cerrarInstrucciones() {
    var instructions = document.getElementById("intrucciones");
    instructions.style.display = "none";
}
document.getElementById("createSeccionForm").addEventListener("submit", function (event) {
    event.preventDefault();

    var form = document.getElementById("createSeccionForm");
    var formData = new FormData(form);

    if (formData.get("nombre_seccion") === "" || formData.get("nombre_seccion") === null) {
        mostrarMensajeTemporal("No se puede crear una sección sin nombre", 7);
        return;
    }

    // Iterar sobre los datos del formulario y mostrarlos por consola
    for (var entry of formData.entries()) {
        console.log("Campo:", entry[0]);
        console.log("Valor:", entry[1]);
    }

    fetch("/createSeccion", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error " + response.status + ": " + response.statusText);
        }
        window.location.reload();
    })
    .catch(error => {
        if (error.message.startsWith("Error 452")) {
            mostrarMensajeTemporal("No se puede crear una sección con el nombre repetido", 7); 
        } else {
            mostrarMensajeTemporal("No se puede añadir en este momento", 7); 

        }
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
    console.log("Estado:", estado);
    // Asignar valores actuales a los campos del formulario
    nombreInput.value = nombre;
    indiceInput.value = indice;
    if (estado == "Activa") {
        estado = true;
    } else {
        estado = false;
    }
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

    if (formData.get("nombre_seccion_editar") === "" || formData.get("nombre_seccion_editar") === null) {
        mostrarMensajeTemporal("No se puede crear una sección sin nombre", 7);
        return;
    }
    

    fetch("/editSeccion", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error " + response.status + ": " + response.statusText);
        }
        window.location.reload();
    })
    .catch(error => {
        if (error.message.startsWith("Error 452")) {
            mostrarMensajeTemporal("No se puede crear una sección con el nombre repetido", 7); 
        } else {
            mostrarMensajeTemporal("No se puede añadir en este momento", 7); 

        }
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








function mostrarMensajeTemporal(mensaje, segundos) {
    var burbleadvice = document.getElementById("burbleadvice");
    var descripmsg = document.getElementById("descripmsg");
    var count = document.getElementById("count");

    descripmsg.textContent = mensaje; 

    // Muestra el elemento burbleadvice
    burbleadvice.style.display = "flex";

    // Actualiza el contador
    count.textContent = segundos;

    var intervalo = setInterval(function() {
        segundos--;
        count.textContent = segundos;

        if (segundos <= 0) {
            clearInterval(intervalo); // Detiene el intervalo cuando el contador llega a cero
            burbleadvice.style.display = "none"; // Oculta el elemento burbleadvice
        }
    }, 1000); // Actualiza el contador cada segundo
}
