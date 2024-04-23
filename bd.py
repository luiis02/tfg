from src.database.dbcontroller import DBController

# Crear una instancia de la clase DBController
bd = DBController()

# Conectar a la base de datos
bd.connect()

# Ejecutar una consulta
bd.execute_query("INSERT INTO sentence (sentence, uso, realimentacion) VALUES ('Hola', 0, 10)", "")
bd.execute_query("INSERT INTO sentence (sentence, uso, realimentacion) VALUES ('Hola que tal', 0, 10)", "")
bd.execute_query("INSERT INTO sentence (sentence, uso, realimentacion) VALUES ('Buenos dias', 0, 10)", "")
bd.execute_query("INSERT INTO sentence (sentence, uso, realimentacion) VALUES ('buenas tardes', 0, 10)", "")
bd.execute_query("INSERT INTO sentence (sentence, uso, realimentacion) VALUES ('buenas noches', 0, 10)", "")
bd.execute_query("INSERT INTO sentence (sentence, uso, realimentacion) VALUES ('hola como estas', 0, 10)", "")
bd.execute_query("INSERT INTO sentence (sentence, uso, realimentacion) VALUES ('hola que tal', 0, 10)", "")
bd.execute_query("INSERT INTO sentence (sentence, uso, realimentacion) VALUES ('saludos', 0, 10)", "")

# Desconectar de la base de datos
bd.disconnect()
