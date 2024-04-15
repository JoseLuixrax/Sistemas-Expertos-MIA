import json
import speech_recognition as sr
from unidecode import unidecode
from gtts import gTTS
import os

# Cambiar Rutas a las de su ordenador antes de ejecutar
RUTA_AUDIO = "/Users/rosamorenolopez/Documents/MIA/sistemas_expertos/"
RUTA_JSON = 'MIA/sistemas_expertos/Sistemas-Expertos-MIA/carreras2.json'

class Carrera:
    def __init__(self, nombre, requisitos):
        self.nombre = nombre
        self.requisitos = requisitos

def cargar_carreras_desde_json(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        data = json.load(f)
    carreras = []
    for carrera_data in data:
        carrera = Carrera(carrera_data['nombre'], carrera_data['requisitos'])
        carreras.append(carrera)
    return carreras

def recomendar_carrera(skills, carreras):
    carreras_recomendadas = []
    skills = [unidecode(skill).lower() for skill in skills]
    for carrera in carreras:
        if any(unidecode(req).lower() in skills for req in carrera.requisitos):
            print(f"Req: {carrera.requisitos} - Skills: {skills}")
            carreras_recomendadas.append(carrera.nombre)
    return carreras_recomendadas

def obtener_habilidades_por_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Por favor, di tus habilidades:")
        audio = recognizer.listen(source)

    try:
        habilidades = recognizer.recognize_google(audio, language='es-ES').split(',')
        return habilidades
    except sr.UnknownValueError:
        print("No se pudo entender la entrada de voz.")
        return []
    except sr.RequestError as e:
        print("Error en la solicitud de reconocimiento de voz: {0}".format(e))
        return []

def decir(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save(RUTA_AUDIO+"voz.mp3")
    os.system(f"afplay {RUTA_AUDIO}voz.mp3")

def main():
    decir("¡Bienvenido al Sistema Experto de Desarrollo Profesional!")
    # skills = input("Ingresa tus habilidades separadas por comas: ").split(',')
    skills = obtener_habilidades_por_voz()
    print(skills)

    carreras = cargar_carreras_desde_json(RUTA_JSON)
    carreras_recomendadas = recomendar_carrera(skills, carreras)

    if carreras_recomendadas:
        decir("Basado en tus habilidades, las siguientes carreras podrían ser adecuadas para ti:")
        for carrera in carreras_recomendadas:
            decir(carrera)
            print("-", carrera)
    else:
        decir("Lo siento, no encontramos ninguna carrera que coincida con tus habilidades.")

if __name__ == "__main__":
    main()
