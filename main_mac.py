import json
import speech_recognition as sr
from unidecode import unidecode
from gtts import gTTS
import os

# Cambiar rutas a las de su ordenador antes de ejecutar
RUTA_AUDIO = "/Users/rosamorenolopez/Documents/MIA/sistemas_expertos/Sistemas-Expertos-MIA"
RUTA_JSON = 'MIA/sistemas_expertos/Sistemas-Expertos-MIA/carreras.json'

class Carrera:
    def __init__(self, nombre, requisitos, rango_salarial):
        self.nombre = nombre
        self.requisitos = requisitos
        self.rango_salarial = rango_salarial

def cargar_carreras_desde_json(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        data = json.load(f)
    carreras = []
    for carrera_data in data:
        carrera = Carrera(carrera_data['nombre'], carrera_data['requisitos'], carrera_data['rango_salarial'])
        carreras.append(carrera)
    return carreras

def recomendar_carrera(skills, carreras):
    carreras_recomendadas = []
    skills = [unidecode(skill).lower() for skill in skills]
    for carrera in carreras:
        if any(unidecode(req).lower() in skills for req in carrera.requisitos):
            carreras_recomendadas.append((carrera.nombre, carrera.rango_salarial))
    return carreras_recomendadas

def filtrar_por_rango_salarial(rango_deseado, carreras):
    carreras_filtradas = []
    for carrera, rango in carreras:
        if rango_deseado >= rango['minimo'] and rango_deseado <= rango['maximo']:
            carreras_filtradas.append((carrera, rango))
    return carreras_filtradas

def obtener_habilidades_por_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Por favor, di tus habilidades:")
        decir("Por favor, di tus habilidades:")
        audio = recognizer.listen(source)

    try:
        habilidades = recognizer.recognize_google(audio, language='es-ES').split(',')
        return habilidades
    except sr.UnknownValueError:
        print("No se pudo entender la entrada de voz de tus habilidades.")
        return []
    except sr.RequestError as e:
        print("Error en la solicitud de reconocimiento de voz: {0}".format(e))
        return []

def obtener_expectativa_salarial_por_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Por favor, di tu expectativa salarial:")
        decir("Por favor, di tu expectativa salarial:")
        audio = recognizer.listen(source)

    try:
        salario = recognizer.recognize_google(audio, language='es-ES')
        salario = salario.replace('mil', '000').replace(' ', '').replace(',', ''). replace('euros', '').replace('€', '').replace('.', '')
        return int(salario)
    except sr.UnknownValueError:
        print("No se pudo entender la entrada de voz.")
        return 0
    except sr.RequestError as e:
        print("Error en la solicitud de reconocimiento de voz: {0}".format(e))
        return 0


def decir(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save(RUTA_AUDIO+"voz.mp3")
    os.system(f"afplay {RUTA_AUDIO}voz.mp3")

def main():
    print("¡Bienvenido al Sistema Experto de Orientación Laboral!")
    decir("¡Bienvenido al Sistema Experto de Orientación Laboral!")
    skills = obtener_habilidades_por_voz()
    print(f"Tus habilidades son: {skills}")

    carreras = cargar_carreras_desde_json(RUTA_JSON)
    carreras_recomendadas = recomendar_carrera(skills, carreras)
    expectativa_salarial = obtener_expectativa_salarial_por_voz()
    print(f"Expectativa salarial:{expectativa_salarial}")

    if carreras_recomendadas:
        
        carreras_recomendadas = filtrar_por_rango_salarial(expectativa_salarial,carreras_recomendadas)
        print(carreras_recomendadas)
        if len(carreras_recomendadas) == 0:
            decir("Lo siento, no encontramos ninguna carrera que coincida con tu expectativa salarial.")
            return
        
        decir("Basado en tus habilidades y tus expectativas salariales, las siguientes carreras podrían ser adecuadas para ti:")
        
        for carrera in carreras_recomendadas:
            decir(f"La carrera: {carrera[0]} con un salario mínimo de {carrera[1]['minimo']} y máximo de {carrera[1]['maximo']}")
            
    else:
        decir("Lo siento, no encontramos ninguna carrera que coincida con tus habilidades y expectativa salarial.")

if __name__ == "__main__":
    main()
