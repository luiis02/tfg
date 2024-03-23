from flask import jsonify,request
from src.mail.send_email import sendEmail
from flask import request

##############################################################################################
##############################################################################################
##############################################################################################

##############################################################################################
##############################################################################################
##############################################################################################
from flask import Blueprint
mail_routes = Blueprint("mail_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################
@mail_routes.route('/mail', methods=['POST'])
def mail():
    cookies = request.cookies
    print(cookies)
    if cookies.get('auth') != 'True':
        return jsonify({"error": "No autorizado"})
    else:
        data = request.get_json()
        asunto = data.get('asunto')
        msg = data.get('msg')
        destinatario = data.get('destinatario')
        clave = data.get('clave')
        sendEmail(asunto, msg, destinatario)
        return jsonify({"message": "Correo enviado correctamente"})