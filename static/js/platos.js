function cerrarInstrucciones() {
    var instructions = document.getElementById("intrucciones");
    instructions.style.display = "none";
}
function cerrarFormulario() {
    var edtiform = document.getElementById("editform");
    edtiform.style.display = "none";
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

    if (formData.get("nombre_seccion") === "" || formData.get("nombre_seccion") === null) {
        mostrarMensajeTemporal("No se puede crear un plato sin nombre", 7);
        return;
    }
    if (formData.get("precio") === "") formData.set("precio", 0);
    fetch("/createPlato", {
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
            mostrarMensajeTemporal("No se puede crear un plato con el nombre repetido", 7); 
        } else {
            mostrarMensajeTemporal("No se puede añadir en este momento", 7); 

        }
    });
});

var edita = ""
function editform(nombre, descripcion, precio, indice, estado) {
    edita = nombre;
    // Mostrar el formulario de edición
    var edtiform = document.getElementById("editform");
    edtiform.style.display = "flex"; // Cambiado a "block" para que sea visible

    // Obtener referencia a los campos del formulario de edición
    var nombreInput = document.getElementById("editNombreSeccion");
    var indiceInput = document.getElementById("editIndice");
    var estadoInput = document.getElementById("editEstado");
    var precioInput = document.getElementById("editPrecio");
    var descripcionInput = document.getElementById("editSeccion");
    var estadoInput = document.getElementById("editEstado");

    // Asignar valores actuales a los campos del formulario
    nombreInput.value = nombre;
    indiceInput.value = indice;
    estadoInput.checked = estado; // estado debe ser un valor booleano
    precioInput.value = precio;
    descripcionInput.value = descripcion;
    estadoInput.checked = estado; // estado debe ser un valor booleano
}

function enviarFormulario() {
    var form = document.getElementById("editSeccionForm");
    var formData = new FormData(form);

    // Set the value of estado to an empty string if it is empty
    if (formData.get("estado_editar") === "") {
        formData.set("estado_editar", "");
    }
    formData.append("edita", edita); // Agregar la variable "edita" al formulario

    console.log("Formulario a enviar:", formData);
    console.log(formData.get("nombre_seccion_editar"));
    console.log(formData.get("indice_editar"));
    console.log(formData.get("estado_editar"));
    if (formData.get("nombre_seccion_editar") === "" || formData.get("nombre_seccion_editar") === null) {
        mostrarMensajeTemporal("No se puede crear una sección sin nombre", 7);
        return;
    }
    if (formData.get("precio_editar") === "") formData.set("precio_editar", 0);

    fetch("/editPlato", {
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

        fetch("/removePlato", {
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
    if (elemento.textContent.trim() === 'Activo') {
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
