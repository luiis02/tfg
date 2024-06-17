import socket
import numpy as np
import wave

UDP_IP = "0.0.0.0"
UDP_PORT = 12345
samples_per_packet = 512

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Servidor escuchando en puerto:", UDP_PORT)

# Preparar archivo WAV para guardar el audio recibido
wave_file = wave.open('audio_received.wav', 'wb')
wave_file.setnchannels(1)  # Mono
wave_file.setsampwidth(2)  # 16 bits
wave_file.setframerate(16000)  # 16 kHz

try:
    while True:
        data, addr = sock.recvfrom(samples_per_packet * 2)  # Tamaño del buffer
        audio_samples = np.frombuffer(data, dtype=np.int16)
        wave_file.writeframes(audio_samples.tobytes())
        print("Recibido paquete de {}: {} bytes".format(addr, len(data)))
except KeyboardInterrupt:
    pass
finally:
    wave_file.close()
    sock.close()
    print("Servidor cerrado y archivo WAV guardado.")
