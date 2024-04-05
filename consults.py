from src.database.dbcontroller import DBController

def vaciar():
    a = DBController()
    a.connect()
    a.execute_query("DELETE FROM usuario_sin_confirmar;")
    a.execute_query("DELETE FROM usuario;")
#    a.execute_query("DELETE FROM cartas;")
    a.connection.commit()
    a.disconnect()

def userRoot():
    a = DBController()
    a.connect()
    root = "root".encode('utf-8')
    a.execute_query("INSERT INTO usuario (nombre, apellido, establecimiento, provincia, email, passwd, usuario, telefono) VALUES ('root', 'root', 'root', 'root', 'root', ?, 'root', 'root')", (root,))
    a.connection.commit()
    a.disconnect()

bd = DBController()
bd.connect()
#a = bd.fetch_data("SELECT COUNT(*) FROM platos WHERE carta = ? AND usuario = ? AND seccion = ?;", ('prueba', 'root', 'estas'))
#print(a[0][0])
bd.execute_query("DROP TABLE IF EXISTS pedidos_activos;")
bd.execute_query(" CREATE TABLE pedidos_activos (id INT AUTO_INCREMENT PRIMARY KEY, usuario VARCHAR(50), mesa INT, plato VARCHAR(50), cantidad INT, precio FLOAT, fecha DATE, estado INT);")
bd.execute_query(" CREATE TABLE pedidos_historicos (id INT AUTO_INCREMENT PRIMARY KEY, usuario VARCHAR(50), mesa INT, plato VARCHAR(50), cantidad INT, precio FLOAT, fecha DATE, fecha_cierre DATE);")
bd.connection.commit()
bd.disconnect()

