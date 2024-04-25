from src.database.dbcontroller import DBController

# Crear una instancia de la clase DBController
bd = DBController()

# Conectar a la base de datos
bd.connect()

# Ejecutar una consulta
bd.execute_query("INSERT INTO intents (tag, Tipo, Texto, indice_apoyo) VALUES ('pedir', 1,%s,2)", ("Pedido anotado",))
bd.execute_query("INSERT INTO intents (tag, Tipo, Texto, indice_apoyo) VALUES ('pedir', 1,%s,2)", ("Pedido recibido",))
bd.execute_query("INSERT INTO intents (tag, Tipo, Texto, indice_apoyo) VALUES ('pedir', 1,%s,2)", ("Recibido en cocina",))






# Desconectar de la base de datos
bd.disconnect()
