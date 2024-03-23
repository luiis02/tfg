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

vaciar()
userRoot()

