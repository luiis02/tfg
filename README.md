
# Documentación
## register()
### Ruta
    /register
### Metodos: 
* Get 
* Post
### Función: 
    Front-End
### Parametros:
* Sin parametros
### Descripción: 
    1. Recibe el formulario del registro
    2. Envia datos del formulario a ser procesados en CreateUser
    3. Recibe respuesta de CreateUser y redirige al usuario en función del estado de CreateUser

## login()
### Ruta:
    /login
### Metodos:
* Get
* Post
### Función:
    Front-End
### Parametros:
* Sin parametros
### Descripción:
    1. Recibe el formulario del login
    2. Envia datos del formulario a ser procesados en LoginUser
    3. Recibe respuesta de LoginUser y redirige al usuario en función del estado de LoginUser

## confirm()
### Ruta:
    /confirm/<username>
### Metodos:
* Get
* Post
### Función:
    Front-end
### Parametros:
* Sin parametros
### Descripción:
    1. Recibe el formulario de confirmación
    2. Envia datos del formulario a ser procesados en ConfirmUser
    3. Recibe respuesta de ConfirmUser y redirige al usuario en función del estado de ConfirmUser

## cierresesion()
### Ruta:
    /cierresesion
### Metodos:
    Sin métodos
### Función:
    Back-End
    Front-End
### Parametros:
* Sin parametros
### Descripción:
    1. Elimina la variable sesión del usuario logeado
    2. Redirige a /login





## Funcion
### Ruta:
### Metodos:
### Función:
### Parametros:
### Descripción:
