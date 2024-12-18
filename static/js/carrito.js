if (document.referrer == document.location.href) {
    document.getElementById("bredcrenl").href = "/carta";
} else {
    document.getElementById("bredcrenl").href = document.referrer;

}
// Función para agregar la clase "shaking" a la imagen del carrito
function shakeCartImage() {
    var imgCarrito = document.getElementById('imgcarrito');
    imgCarrito.classList.add('shaking');

    // Después de 0.5 segundos, remover la clase "shaking"
    setTimeout(function () {
        imgCarrito.classList.remove('shaking');
    }, 500);
}

// Variable para rastrear la actividad del usuario
var timer;

// Función para reiniciar el temporizador cuando hay actividad del usuario
function resetTimer() {
    clearTimeout(timer);
    timer = setTimeout(shakeCartImage, 5000); // Agita la imagen después de 5 segundos sin actividad
}

// Agregar escuchadores de eventos para rastrear la actividad del usuario
document.addEventListener('mousemove', resetTimer);
document.addEventListener('keypress', resetTimer);


resetTimer();



function crearCookie(nombre, valor) {
    var fecha = new Date();
    fecha.setTime(fecha.getTime() + (20 * 60 * 1000));
    var expira = "expires=" + fecha.toUTCString();
    document.cookie = nombre + "=" + encodeURIComponent(JSON.stringify(valor)) + ";" + expira + ";path=/";
}


function obtenerCookie(nombre) {
    var nombreCookie = nombre + "=";
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        while (cookie.charAt(0) == ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(nombreCookie) == 0) {
            return cookie.substring(nombreCookie.length, cookie.length);
        }
    }
    return null;
}

function eliminarCookie(nombre) {
    crearCookie(nombre, "", -1);
}

function obtenerTodasLasCookies() {
    var cookies = document.cookie.split(';');
    var cookiesObj = {};
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        var partes = cookie.split('=');
        var nombre = partes[0];
        var valor = partes.slice(1).join('='); // Para manejar valores que contienen '='
        try {
            // Intentar decodificar y analizar el valor como JSON
            cookiesObj[nombre] = JSON.parse(decodeURIComponent(valor));
        } catch (error) {
            // Si hay un error, el valor no es JSON, por lo que lo guardamos como está
            cookiesObj[nombre] = decodeURIComponent(valor);
        }
    }
    return cookiesObj;
}



function sumafinal() {
    generaCarrito();
    var todasLasCookies = obtenerTodasLasCookies();


    var suma = 0;
    for (var nombreCookie in todasLasCookies) {
        var valorCookie = todasLasCookies[nombreCookie];
        suma += valorCookie.precio * valorCookie.cantidad;
    }
    if (isNaN(suma)) {
        document.getElementById("preciotot").innerText = "(0.00€)";
        return;
    }
    var textoaniadir = "(" + suma.toFixed(2) + "€)";
    document.getElementById("preciotot").innerText = textoaniadir;
}


function generaCarrito() {
    var todasLasCookies = obtenerTodasLasCookies();
    console.log(todasLasCookies);
    var strtext = ''; // Initialize an empty string to store the HTML
    for (var nombreCookie in todasLasCookies) {
        var valorCookie = todasLasCookies[nombreCookie]['cantidad'];
        var precioCookie = todasLasCookies[nombreCookie]['precio'];
        if (valorCookie != 0 && nombreCookie != "total" && nombreCookie.trim() != "") {
            strtext += `
        <div class="platos" id="${nombreCookie}">
            <div class="subseccion1">
                <div id="namepla">
                    <b>${nombreCookie}</b>
                </div>
                <div id="namepre">
                    ${precioCookie} €
                </div>

                <div class="contadortotal">
                    <button class="elimina" id="elimina_${nombreCookie}"
                        onclick="decrementCounter('cant_${nombreCookie}', '${nombreCookie}')">-</button>

                    <b id="cant_${nombreCookie}">${valorCookie}</b>
                    <button class="aniade" id="aniade_${nombreCookie}"
                        onclick="incrementCounter('cant_${nombreCookie}', '${nombreCookie}')">+</button>
                </div>
            </div>
            <hr class="separapla">
        </div>
        `;
        }

    }
    // After the loop, set the HTML of .menu to the generated string
    document.querySelector(".menu").innerHTML = strtext;
}
// Función para incrementar el contador
function incrementCounter(idd, idd2) {
    // Obtener el elemento del contador
    var contador = document.getElementById(idd);
    // Obtener el valor actual del contador y convertirlo a un número
    var valorActual = parseInt(contador.innerText);
    // Incrementar el valor del contador
    valorActual++;
    // Actualizar el valor mostrado en el contador
    contador.innerText = valorActual;
    getCount(idd2, valorActual);
}

// Función para decrementar el contador
function decrementCounter(idd, idd2) {
    // Obtener el elemento del contador
    var contador = document.getElementById(idd);
    // Obtener el valor actual del contador y convertirlo a un número
    var valorActual = parseInt(contador.innerText);
    // Verificar si el valor actual es mayor que cero para evitar números negativos
    if (valorActual > 0) {
        // Decrementar el valor del contador
        valorActual--;
        // Actualizar el valor mostrado en el contador
        contador.innerText = valorActual;
    }
    getCount(idd2, valorActual);
}

function getCount(idd2, idd3) {
    var nombre = document.getElementById(idd2);
    var precio = nombre.querySelector("#namepre");
    var precioTexto = precio.innerText;
    var precioNumero = parseFloat(precioTexto.match(/[\d\.]+/)[0]);
    var valorCookie = obtenerCookie(idd2);

    if (valorCookie != null) {
        // Si la cookie existe, eliminarla y crear una nueva con el nuevo valor
        eliminarCookie(idd2);
        crearCookie(idd2, { cantidad: idd3, precio: precioNumero });

    } else {
        // Si la cookie no existe, crear una nueva
        crearCookie(idd2, { cantidad: idd3, precio: precioNumero });
    }

    var todasLasCookies = obtenerTodasLasCookies();
    var suma = 0;
    for (var nombreCookie in todasLasCookies) {
        var valorCookie = todasLasCookies[nombreCookie];
        if (valorCookie != 0 && nombreCookie != "total") {
            var nombre = document.getElementById(nombreCookie);
            if (nombre == null) {
                continue;
            }
            var precio = nombre.querySelector("#namepre");
            var precioTexto = precio.innerText;
            var precioNumero = parseFloat(precioTexto.match(/[\d\.]+/)[0]);
            suma += precioNumero * valorCookie;
        }
    }
    var textoaniadir = "(" + suma.toFixed(2) + "€)";
    document.getElementById("preciotot").innerText = textoaniadir;
    sumafinal();
}

generaCarrito();
sumafinal()


function enviarPedido(event ) {
    event.preventDefault(); 
    var todasLasCookies = obtenerTodasLasCookies();
    var pedido = [];
    for (var nombreCookie in todasLasCookies) {
        var valorCookie = todasLasCookies[nombreCookie];
        if (valorCookie != 0 && nombreCookie != "total" && nombreCookie.trim() != "") {
            var nombre = document.getElementById(nombreCookie);
            if (nombre == null) {
                continue;
            }
            pedido.push({ nombre: nombreCookie, cantidad: valorCookie.cantidad, precio: valorCookie.precio, categoria: valorCookie.categoria});

        }
    }
    if (pedido.length == 0) {
        alert("No hay platos en el pedido");
        return;
    } else {
        var jsonPedido = JSON.stringify(pedido);
        console.log(jsonPedido);
        for (var nombreCookie in todasLasCookies) {
            eliminarCookie(nombreCookie);
            crearCookie(nombreCookie, { cantidad: 0, precio: 0, categoria: ""})
        }
        
        fetch('/pedido', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonPedido
        })
        .then(response => {
            console.log(response);
            window.location.href = "/pedidoFin";
        })
        .catch(error => {
            console.error('Error:', error);
            window.location.href = "/pedidoFin";

        });
    }
}