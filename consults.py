from src.database.dbcontroller import DBController


def vaciar():
    a = DBController()
    a.connect()
    a.execute_query("DELETE FROM usuario_sin_confirmar;")
    a.execute_query("DELETE FROM usuario;")
    a.execute_query("DELETE FROM cartas;")
    a.connection.commit()
    a.disconnect()


vaciar()

