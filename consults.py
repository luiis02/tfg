from src.database.dbcontroller import DBController

a = DBController()
a.connect()

a.execute_query("INSERT INTO cartas (nombre, usuario, indice, status) VALUES ('Nombre de la carta', 'root', 1, true);")
a.connection.commit()

# Desconectar de la base de datos
a.disconnect()

