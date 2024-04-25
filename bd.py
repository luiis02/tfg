from src.database.dbcontroller import DBController

# Crear una instancia de la clase DBController
bd = DBController()

# Conectar a la base de datos
bd.connect()

# Ejecutar una consulta
bd.execute_query("INSERT INTO tag (sentence, uso, realimentacion) VALUES ('1', 1, 10)", "")

# Desconectar de la base de datos
bd.disconnect()
