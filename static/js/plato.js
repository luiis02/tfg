
function incrementCounter(idd, idd2, categ) {
    var contador = document.getElementById(idd);
    var valorActual = parseInt(contador.innerText);
    valorActual++;
    contador.innerText = valorActual;
    getCount(idd2, valorActual, categ);
}

// Función para decrementar el contador
function decrementCounter(idd, idd2, categ) {
    var contador = document.getElementById(idd);
    var valorActual = parseInt(contador.innerText);
    if (valorActual > 0) {
        valorActual--;
        contador.innerText = valorActual;
    }
    getCount(idd2, valorActual, categ);
}

function getCount(idd2, idd3, categ) {
    var nombre = document.getElementById(idd2);
    var precio = nombre.querySelector("#namepre");
    var precioTexto = precio.innerText;
    var precioNumero = parseFloat(precioTexto.match(/[\d\.]+/)[0]);
    var valorCookie = obtenerCookie(idd2);


    if (valorCookie != null) {
        eliminarCookie(idd2);
        crearCookie(idd2, { cantidad: idd3, precio: precioNumero, categoria: categ });
    } else {
        crearCookie(idd2, { cantidad: idd3, precio: precioNumero, categoria: categ  });
    }

    var todasLasCookies = obtenerTodasLasCookies();
    console.log(todasLasCookies);
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




var todasLasCookies = obtenerTodasLasCookies();


var suma = 0;
for (var nombreCookie in todasLasCookies) {
    var valorCookie = todasLasCookies[nombreCookie];
    if (valorCookie != 0 && nombreCookie != "total" && valorCookie.cantidad != 0) {
        var nombre = document.getElementById(nombreCookie);
        var cant = document.getElementById("cant" + nombreCookie);
        if (cant == null) {
            continue;
        }
        cant.innerText = valorCookie.cantidad;
        if (nombre == null) {
            continue;
        }
        var precio = nombre.querySelector("#namepre");
        var precioTexto = precio.innerText;
        var precioNumero = parseFloat(precioTexto.match(/[\d\.]+/)[0]);
        suma += precioNumero * valorCookie.cantidad;
    }
}





var suma = 0;
for (var nombreCookie in todasLasCookies) {
    var valorCookie = todasLasCookies[nombreCookie];
    if (valorCookie != 0 && nombreCookie != "total" && valorCookie.cantidad != 0) {
        var nombre = document.getElementById(nombreCookie);
        var cant = document.getElementById("cant" + nombreCookie);
        if (cant != null) {
            
            cant.innerText = valorCookie.cantidad;
            if (nombre != null) {
                var precio = nombre.querySelector("#namepre");
            var precioTexto = precio.innerText;
            var precioNumero = parseFloat(precioTexto.match(/[\d\.]+/)[0]);
            suma += precioNumero * valorCookie.cantidad;   
            }

        }
        
    }
}




