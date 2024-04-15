
from src.database.dbcontroller import DBController
from datetime import datetime
##############################################################################################
##############################################################################################
##############################################################################################


def marcaPedido(estado, data):
    bd = DBController()
    bd.connect()
    
    if estado == 'fin':   
        result = bd.fetch_data("SELECT * FROM pedidos_activos WHERE id = %s", (data.get('id'),))
        bd.execute_query("DELETE FROM pedidos_activos WHERE id = %s", (data.get('id'),))
        
        count = bd.fetch_data("SELECT COUNT(*) FROM pedidos_historicos")  # Obtener el conteo directamente
        fecha_cierre_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        fecha_datetime = result[0][6]  # Assuming result[0][6] is a datetime.datetime object
        fecha_str = fecha_datetime.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
        fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")  # Parse string to datetime

        
        bd.execute_query(
            "INSERT INTO pedidos_historicos ( usuario, mesa, plato, cantidad, precio, fecha, fecha_cierre, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
            (result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], fecha_datetime, fecha_cierre_actual, result[0][7])
        )
    else:
        bd.execute_query("DELETE FROM pedidos_activos WHERE id = %s", (data.get('id'),))
    
    bd.disconnect()

def obtenpedidos(usuario):
    bd = DBController()
    bd.connect()
    resultados = bd.fetch_data("SELECT * FROM pedidos_activos WHERE usuario = %s ORDER BY fecha ASC", (usuario,))
    bd.disconnect()
    
    resultados_serializables = []

    for resultado in resultados:
        fecha_str = str(resultado[6])  
        fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")



        resultado_dict = {
            'id': resultado[0],
            'usuario': resultado[1],
            'mesa': resultado[2],
            'plato': resultado[3],
            'cantidad': resultado[4],
            'precio': resultado[5],
            'fecha': str(fecha_datetime),
            'categoria': resultado[7]
        }
        resultados_serializables.append(resultado_dict)

    
    bd.connect()
    categorias = bd.fetch_data("SELECT nombre FROM seccion WHERE usuario = %s AND STATUS = TRUE", (usuario,))
    bd.disconnect()
    categorias_carta = []
    for categoria in categorias:
        categorias_carta.append(categoria[0])
    return resultados_serializables, categorias_carta
    