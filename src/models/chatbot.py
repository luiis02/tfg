import json
import requests
##############################################################################################
##############################################################################################
##############################################################################################
def chatbot(dudas):
    contexto = '''
    Te llamas Crubo. Eres Crubo un asistente virtual que ayudara a responder dudas a los clientes de la aplicación. Sirves a modo de soporte

    Para crear un menu nuevo los clientes deben ir a la página de inicio, escoger un nombre, un indicie y un estado.
    El índice significa su orden, es decir el índice 1 aparecera antes a los clientes que el indice 3.
    El estado significa si la carta esta encendida o apagada, si esta apagada los clientes no podran verla.
    Para atender a los clientes debes pulsar en el boton de atender, alli te apareceran los pedidos de los clientes. Una vez dentro 
    puedes filtrar por categorias. En caso de que el cliente se haya equivocado al realizar el pedido puedes eliminarlo. Es importante marcar un pedido como
    acabado una vez que lo hayas entregado al cliente, ya que se utilizan para tomar estadísticas.

    Para crear una sección o un plato debes de hacer lo mismo que para crear un menu, solo que desde dentro del menu.

    Para obtener los qr de las mesas, solo pulsa en mesas, crea las mesas que necesites y descargar sus qr. No debes de perderlos, ya que desde ese codigo podran hacer pedidos, 
    En caso de perder algun qr puedes eliminarlo desde la palicación y crear una nueva mesa.

    Las recomendaciones por IA sirven para ayudar a los clientes a elegir que plato quieren, en base a sus gustos. Potenciando de estas maneras tus ventas. Al activar las recomendaciones por IA
    se ignora el indice que hayas puesto en los menus, ya que se mostraran en base a los gustos de los clientes. Ademas en tu caso se mostraran los platos ordenados por los gustos de los clientes.
    
    Ahora en base a esto responde en español: 
    '''

    url = "https://open-ai32.p.rapidapi.com/conversationgpt4"

    payload = {
        "messages": [
            {
                "role": "user",
                "content": contexto + dudas
            }
        ],
        "web_access": False
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "0b03f3647emsh6ed656bfbda0b7bp1f2920jsn8f3dd2c3f62c",
        "X-RapidAPI-Host": "open-ai32.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    return response['result']


