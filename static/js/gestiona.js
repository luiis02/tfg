
function enviarEstado(idPedido, estado) {
    const datos = {
        id: idPedido,
        estado: estado
    };

    fetch('/gestion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    })
        .then(response => {
            window.location.reload();
        })
        .catch(error => {
            window.location.reload();
        });
}

function filtrado() {
    guardarEstadoCheckbox(event.target);
    var checkboxes = document.querySelectorAll('.valueCategoría');
    var selectedCategories = [];

    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            selectedCategories.push(checkbox.value);
        }
    });
    var categorias = document.querySelectorAll('.cat-filtadro');
    if(selectedCategories.length > 0) {
    categorias.forEach(function (categoria) {
        var categoryFound = false;
        for (var i = 0; i < selectedCategories.length; i++) {
            if (categoria.textContent === selectedCategories[i]) {
                categoria.parentElement.style.display = 'table-row';
                categoryFound = true;
                break;
            }
        }
        if (!categoryFound) {
            categoria.parentElement.style.display = 'none';
        }
    });
    
}

}


function recargarPagina() {
    var segundosRestantes = 30; // Inicializa el contador en 30 segundos
    var contadorElemento = document.getElementById('contadoractualizacion');

    console.log('Recargando página en ' + segundosRestantes + ' segundos');
    function actualizarContador() {
        if (segundosRestantes % 2 == 0) {
            contadorElemento.textContent = '⏳ Actualizando pedidos en ' + segundosRestantes + ' segundos';
        } else {
            contadorElemento.textContent = '⌛ Actualizando pedidos en ' + segundosRestantes + ' segundos';
        }

        segundosRestantes--;
        if (segundosRestantes < 0) {
            location.reload();
        } else {
            setTimeout(actualizarContador, 1000);
        }
    }

    actualizarContador();
}


window.onload = function() {
    cargarEstadoCheckbox();
    recargarPagina();
    filtrado(); 
};

// Función para guardar el estado de la casilla de verificación en localStorage
function guardarEstadoCheckbox(checkbox) {
localStorage.setItem(checkbox.value, checkbox.checked);
var estadoGuardado = localStorage.getItem(checkbox.value);
}

// Función para cargar el estado de las casillas de verificación desde localStorage
function cargarEstadoCheckbox() {
var checkboxes = document.querySelectorAll('.valueCategoría');
checkboxes.forEach(function(checkbox) {
    var estadoGuardado = localStorage.getItem(checkbox.value);
    if (estadoGuardado !== null) {
        checkbox.checked = (estadoGuardado === "true"); 
    }
});
}

