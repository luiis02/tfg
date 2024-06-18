from flask import Blueprint, redirect, url_for, session, request, jsonify
from src.models.plato import obtenerNombrePlatos
chatbot_routes = Blueprint("chatbot_routes", __name__)
import requests
import json

api_key = 'sk-proj-32XqN4cv9rGWph5rRYmwT3BlbkFJ78jZpRO3kuMEM0BCi8JY'

@chatbot_routes.route('/describeIA', methods=['POST'])
def generaDescripcion():
    data = request.get_json()
    producto = data.get('producto')
    codigo_postal = data.get('codigo_postal')
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    print(producto, codigo_postal)
    data = {
        'model': 'gpt-3.5-turbo-16k-0613',  
        'messages': [
            {'role': 'system', 'content': 'Eres el dueño de un local exitoso, escribe una descripción persuasiva y llamativa, de no más de 25 palabras, que incite a la compra en el sector hostelero. El formato de entrada del usuario es {"producto": value_1, "codigo_postal": value_2}. Ajusta el nivel de formalidad y detalles de la descripción según el código postal proporcionado, no se debe hacer referencia directa al código postal en la descripción, se deben hacer referencias culturales y / o de ubicación Adapta la descripción para que sea entendible para todos los públicos y asegúrate de que resulte atractiva. La descripción debe ser clara, concisa y atractiva.'},
            {'role': 'user', 'content': f'{{"producto": "{producto}", "codigo_postal": "{codigo_postal}"}}'}
        ],
        'max_tokens': 150
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        descripcion = response_data['choices'][0]['message']['content']
        return jsonify({'descripcion': descripcion})
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

@chatbot_routes.route('/soporteIA', methods=['POST'])
def generaChat():
    data = request.get_json()
    msg = data.get('msg')
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': 'gpt-3.5-turbo-16k-0613',  
        'messages': [
            {'role': 'system', 'content': 'Te llamas SEPY, eres un chatbot creado para ayudar al soporte y a resolver dudas en una página web llamada APUNTAJEFE.  Te daré un manual de uso y debes responder a los usuarios segun lo que indique el manual de uso, primero lee el manual lentamente y luego responde paso a paso. Si no aparece la respues en el manual de uso NO RESPONDAS, di que no tienes aun conocimiento. Manual de uso:Bienvenido a apuntajefe, la mejor plataforma para la gestión de locales de hostelería. Para crear una carta, primero debes iniciar sesión, tras esto debes rellenar el formulario en la página principal, el índice indica el orden de aparición para los clientes, en caso de que dos elementos tengan el mismo índice se ordenara por orden alfabético. La casilla de actividad indica si el cliente podrá acceder o no. Para crear una sección, debes primero pulsar en la carta a la que quieras añadir una sección y allí te saldrá un formulario con el mismo formato que para crear una carta. Para crear un plato, debes acceder a la sección pertinente, tras acceder te aparece un formulario muy parecido a los anteriores pero ahora te pedirá una descripción y un precio. Si dejas vacía la descripción aparecerá un "(none)" pero el cliente no visualizara nada. Para crear mesas tan solo debes ir a al menú y pulsar en mesas y escribir el número de mesas a añadir, si ya tienes 8 mesas y creas 10 más tendrás 18.   Al lado de cada mesa podras observar un qr y un botón de descargar, pulsa sobre el y se descargara el qr. A través de ese qr el cliente accederá a la mesa. Si pierdes algún qr es muy importante que borres la mesa perdida, ya que en caso de ser escaneado se podría acceder y hacer pedidos.Aun no es posible actualizar los valores del usuario, no obstante cuando se permita se enviara un correo a todos los usuarios.'},
            {'role': 'user', 'content': msg}
        ],
        'max_tokens': 150
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        respuesta = response_data['choices'][0]['message']['content']
        return jsonify({'respuesta': respuesta})
        
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None



@chatbot_routes.route('/pedidosIA', methods=['POST'])
def buscaPlatos():
    if request.cookies.get('usuarioIA') is None or request.cookies.get('mesaIA') is None:
        return url_for("/login")

    platos = obtenerNombrePlatos(request.cookies.get('usuarioIA'))
    platos = json.loads(platos)
    lista_platos = ", ".join([f"{plato['nombre']} - {plato['precio']} - {plato['seccion']}" for plato in platos["platos"]])
    msg = request.args.get('msg')  
    promt = "Te voy a pasar una lista de platos devuélveme en el formato pedido que quiere el usuario dada la frase. Sin texto adicional ni explicaciones solo el formato de salida. IMPORTANTE SI NO APARECE UN PLATO EN LA LISTA NO LO AÑADAS Lista de platos: "+ lista_platos + " Frase del usuario: " + msg + " Formato: {[{plato: 'plato1', precio: '1', categoeria: 'categoria1',cantidad: '1',},...]}"
    url = 'https://api.openai.com/v1/chat/completions'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': 'gpt-3.5-turbo-16k-0613',  
        'messages': [
            {'role': 'system', 'content': promt},
        ],
        'max_tokens': 350
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        contenido = response_data['choices'][0]['message']['content']

        try:
            platos = json.loads(contenido)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            platos = []

        for plato in platos:
            nombre_plato = plato['plato']
            precio = plato['precio']
            cantidad = plato['cantidad']

        # Ahora hacemos el POST a la dirección especificada
        try:
            url = 'http://192.168.0.2:8000/generaPedidoIA'
            response_post = requests.post(url, json={'respuesta': platos, 'nombre': request.cookies.get('usuarioIA'), 'mesa': request.cookies.get('mesaIA')  })
            if response_post.status_code == 200:
                return jsonify(response_post.json())  
            else:
                print(f"Error en el POST: {response_post.status_code}")
                return jsonify({'error': 'Hubo un problema al hacer el POST'})
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud POST: {e}")
            return jsonify({'error': 'Excepción en la solicitud POST'})

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return jsonify({'error': 'Hubo un problema al hacer la solicitud'})


    