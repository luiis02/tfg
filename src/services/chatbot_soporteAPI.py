from flask import jsonify, request, session, url_for
from flask import request
from src.models.chatbot import chatbot
##############################################################################################
##############################################################################################
##############################################################################################
from flask import Blueprint, request, jsonify
chatbot_routes = Blueprint("soporte_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################

@chatbot_routes.route('/getRespuestaAPI', methods=['POST'])
def getRespuestaAPI():
    datos = request.json
    dudas = datos.get('dudas')
    respuesta = chatbot(dudas)
    return jsonify({'mensaje': respuesta})



