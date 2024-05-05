import speech_recognition as sr
import time

def convertirTexto():
    r = sr.Recognizer()
    with sr.AudioFile('C:\\Users\\luis\\Documents\\GitHub\\tfg\\audio.wav') as source:
        audio = r.listen(source)
        try:
            print("Procesando audio...")
            text = r.recognize_google(audio, language='es-ES')
            time.sleep(1.5)
            print(text)
            return 0,text
        except:
            print("Lo siento, no he podido entender lo que has dicho. Por favor, inténtalo de nuevo.")
            return 1