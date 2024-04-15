from src.database.dbcontroller import DBController
import mysql.connector

bd = DBController()
bd.connect()

query = "SELECT * FROM users"
rows = bd.fetch_data(query)

bd.disconnect()
