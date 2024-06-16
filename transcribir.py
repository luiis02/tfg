import re
import requests

def transcribe():
    api_key = 'sk-proj-32XqN4cv9rGWph5rRYmwT3BlbkFJ78jZpRO3kuMEM0BCi8JY'
    url = 'https://api.openai.com/v1/audio/transcriptions'
    audio_file_path = 'combined_audio.wav'
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
        print("Texto transcrito:")
        print(transcription['text'])
    else:
        print(f"Error al transcribir el audio. Código de estado: {response.status_code}")
        print(response.text)

def encuentrapatron(msg):
    patron = r'Sepy(.*)'
    # Buscar la coincidencia en el texto
    resultado = re.search(patron, texto)

    # Verificar si se encontró la palabra "Sepy"
    if resultado:
        # Obtener el texto que sigue después de "Sepy"
        texto_desde_sepy = resultado.group(1)
        print("Texto desde 'Sepy' en adelante:")
        print(texto_desde_sepy)
    else:
        print("La palabra 'Sepy' no fue encontrada en el texto.")


texto = """
Vale, pues a ver, esta prueba debería de todos y unirlos, los que reciban un día cada dos segundos, 
y yo cada tres, y los que recibir en uno propio. Así que a ver cómo funciona esto y a ver qué ocurre.
Sepy, apunta unos calamares y un colacao
"""

encuentrapatron ("")