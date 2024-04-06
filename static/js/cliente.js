    // Función para agregar la clase "shaking" a la imagen del carrito
    function shakeCartImage() {
        var imgCarrito = document.getElementById('imgcarrito');
        imgCarrito.classList.add('shaking');

        // Después de 0.5 segundos, remover la clase "shaking"
        setTimeout(function() {
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



        function sumafinal(){
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
sumafinal(   )