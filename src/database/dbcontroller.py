import mysql.connector

class DBController:
    def __init__(self):
        self.db_host = "localhost"
        self.db_user = "tfg"
        self.db_password = "tfg"
        self.db_name = "tfg"
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            self.cursor = self.connection.cursor()
            print("Conexión exitosa a la base de datos")
        except mysql.connector.Error as error:
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
            return 1
        except mysql.connector.Error as error:
            print("Error al ejecutar la consulta:", error)
            return 0

    def fetch_data(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            print("Datos obtenidos exitosamente")
            return rows
        except mysql.connector.Error as error:
            print("Error al obtener los datos:", error)
            return []

