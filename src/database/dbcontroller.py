import sqlite3

class DBController:
    def __init__(self):
        self.db_name = "tfg.db"
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print("Conexión exitosa a la base de datos")
        except sqlite3.Error as error:
            print("Error al conectar a la base de datos:", error)

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Desconexión exitosa de la base de datos")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            print("Consulta ejecutada exitosamente")
        except sqlite3.DatabaseError as error:
            print("Error al ejecutar la consulta:", error)

    def fetch_data(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            print("Datos obtenidos exitosamente")
            return rows
        except sqlite3.DatabaseError as error:
            print("Error al obtener los datos:", error)
            return []
