from flask import Flask, request, jsonify
import numpy as np
import os
from scipy.io.wavfile import write
from pydub import AudioSegment
import speech_recognition as sr



app = Flask(__name__)


### Funciones para recibir audio y concatenar archivos ###

def count_received_audio():
    # Aquí implementa la lógica para contar los archivos recibidos
    files = [f for f in os.listdir('.') if f.startswith('received_audio') and f.endswith('.wav')]
    return len(files)

@app.route('/audio', methods=['POST'])
def receive_audio():
    try:
        audio_data = request.data        
        audio_buffer = np.frombuffer(audio_data, dtype=np.int16)
        sample_rate = 16000
        count = count_received_audio()
        temp_filename = f'received_audio{count + 1}.wav'
        write(temp_filename, sample_rate, audio_buffer)  # Guarda el audio en un archivo WAV
        return temp_filename  # Devuelve el nombre del archivo temporal generado
    
    except Exception as e:
        print(f"Error en la recepción de audio: {str(e)}")
        return jsonify({'error': 'Error en la recepción de audio'}), 500

def concatenate_received_audio(input_dir, output_file):
    # Obtener la lista de archivos que siguen el patrón received_audioX.wav
    audio_files = [f for f in os.listdir(input_dir) if f.startswith('received_audio') and f.endswith('.wav')]
    
    # Ordenar los archivos para asegurar la concatenación en el orden correcto
    audio_files.sort()

    # Inicializar una lista vacía para almacenar segmentos de audio
    audio_segments = []

    # Cargar cada archivo de entrada y agregarlo a la lista de segmentos
    for file in audio_files:
        audio_segments.append(AudioSegment.from_file(os.path.join(input_dir, file)))

    # Concatenar los segmentos de audio
    combined = audio_segments[0]
    for segment in audio_segments[1:]:
        combined = combined + segment

    # Guardar el audio combinado en el archivo de salida
    combined.export(output_file, format='wav')

    print(f"Archivos unidos correctamente y guardados como '{output_file}'.")

# Ejemplo de uso:
input_directory = '.'  # Directorio donde se encuentran los archivos de audio
output_file = 'combined_audio.wav'  # Nombre del archivo de salida combinado



if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    concatenate_received_audio(input_directory, output_file)

