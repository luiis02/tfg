import qrcode
from src.database.dbcontroller import DBController

def crear_qr(numero, establecimiento, mesa, identificador):
    # URL base para el pedido
    url_base = "http://127.0.0.1:5000/pedido"

    # Parámetros del pedido
    parametros = {
        "ref": establecimiento,
        "mes": mesa,
        "num": identificador
    }

    bd = DBController()
    result = bd.fetch_data("SELECT * FROM mesas WHERE id = ? AND establecimiento =?", (identificador,establecimiento))
    n_mesas = result[0][0]
    
    #### en la tabla mesas habra: id, establecimiento, numero_mesa, img_qr
    for i in range(numero):
        num_mesa = n_mesas + 1 + i
        url_pedido = url_base + "&" + str(establecimiento) + "&" + str(num_mesa) + "&" + str(identificador)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url_pedido)
        qr.make(fit=True)
        imagen_qr = qr.make_image(fill_color="black", back_color="white")
        bd.insert_data("INSERT INTO mesas (id_establecimiento, establecimiento, numero_mesa, img_qr) VALUES (?, ?, ?, ?)", (identificador,establecimiento, num_mesa, imagen_qr))






