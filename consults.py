from src.database.dbcontroller import DBController
from datetime import datetime

bd = DBController()
bd.connect()

strin = "2024-04-07 01:56:44"
datetime_obj = datetime.strptime(strin, "%Y-%m-%d %H:%M:%S")
fecha_cierre_actual = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
print(fecha_cierre_actual)

#res = bd.fetch_data("SELECT * FROM p WHERE fecha > ?", (fecha_cierre_actual,))
#bd.execute_query("INSERT INTO relaciones VALUES ('valoración', 'precio', 3)")
bd.execute_query("UPDATE usuario SET establecimiento = 'Kabit' WHERE usuario = 'Kabit'")
bd.disconnect()