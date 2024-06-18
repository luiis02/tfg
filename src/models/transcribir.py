import re
import requests

def transcribe():
    api_key = 'sk-proj-32XqN4cv9rGWph5rRYmwT3BlbkFJ78jZpRO3kuMEM0BCi8JY'
    url = 'https://api.openai.com/v1/audio/transcriptions'
    audio_file_path = 'audio_received.wav'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    files = {
        'file': ('audio.mp3', open(audio_file_path, 'rb'), 'audio/mp3'),
    }
    data = {
        'model': 'whisper-1',
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 200:
        transcription = response.json()
        return transcription['text']
    else:
        print(f"Error al transcribir el audio. Código de estado: {response.status_code}")
        print(response.text)

def encuentrapatron(msg):
    patron = r'robot(.*)'
    resultado = re.search(patron, msg)

    if resultado:
        texto_desde_sepy = resultado.group(1)
        print(texto_desde_sepy)
        return texto_desde_sepy
    else:
        patron = r'Robot(.*)'
        resultado = re.search(patron, msg)
        if resultado:
            texto_desde_sepy = resultado.group(1)
            return texto_desde_sepy
        else:
            print("La palabra 'Robot' no fue encontrada en el texto.")

def transcribirYlocalizar():
    return encuentrapatron(transcribe())

def generaSolicitud():
    msg = str(transcribirYlocalizar())
    #msg = ", apunta, una Coca-Cola, dos tortillas, para la misa, tres por favor."
    url = "http://192.168.0.2:8000/pedidosIA"

    headers = {
        'Authorization': 'Basic Og==',  
        'Cookie': 'mesaIA=3; usuarioIA=root'
    }

    payload = {}
    params = {'msg': msg}

    response = requests.post(url, headers=headers, params=params, data=payload)

    if response.status_code == 200:
        response_data = response.json()
        respuesta = response_data.get('respuesta', '')
        print(respuesta)
    else:
        print(f"Error en la solicitud: {response.status_code}")
        print(response.text)
    


generaSolicitud()