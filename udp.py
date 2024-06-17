import socket
import struct
import numpy as np
import wave
import time

# Configura el servidor UDP
UDP_IP = "192.168.0.2"  # Dirección IP donde esperas recibir los datos (debe ser la misma que en el ESP32)
UDP_PORT = 1234  # Puerto donde esperas recibir los datos (debe ser el mismo que en el ESP32)

# Crea el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Servidor UDP escuchando en {UDP_IP}:{UDP_PORT}")

# Configura el tamaño del buffer de recepción
sample_rate = 4000  # Frecuencia de muestreo
duration = 8  # Duración del segmento en segundos
buffer_size = sample_rate * duration  # Tamaño del buffer para 5 segundos de audio (ajusta según necesidad)

# Variables para acumular los datos durante 5 segundos
audio_buffer = []
start_time = time.time()

def save_wav(audio_data):
    # Configura los parámetros del archivo WAV
    sample_width = 2  # Tamaño de cada muestra en bytes (int16_t)
    num_channels = 1  # Número de canales (mono)
    sample_rate = 4000  # Frecuencia de muestreo
    
    # Abre un archivo WAV para escribir
    wav_filename = f"audio_{time.strftime('%Y%m%d%H%M%S')}.wav"
    with wave.open(wav_filename, 'wb') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(np.array(audio_data, dtype=np.int16).tobytes())

        print(f"Archivo WAV guardado: {wav_filename}")

while True:
    # Recibe datos del socket UDP
    data, addr = sock.recvfrom(buffer_size * 2)  # Recibe datos en bloques de 2 bytes (int16_t)
    
    # Decodifica los datos recibidos
    num_samples = len(data) // 2  # Cada muestra es de 2 bytes (int16_t)
    audio_data = struct.unpack(f"{num_samples}h", data)  # Convierte los datos binarios a una lista de enteros
    
    # Agrega los datos al buffer de audio
    audio_buffer.extend(audio_data)
    
    # Verifica si el buffer alcanzó su capacidad máxima
    if len(audio_buffer) >= buffer_size:
        # Guarda el buffer acumulado como archivo WAV
        save_wav(audio_buffer[:buffer_size])  # Guarda solo la cantidad máxima del buffer
        audio_buffer = audio_buffer[buffer_size:]  # Guarda el excedente para continuar la acumulación
    
