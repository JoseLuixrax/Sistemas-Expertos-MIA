import json
from unidecode import unidecode


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

def main():
    print("¡Bienvenido al Sistema Experto de Desarrollo Profesional!")
    skills = input("Ingresa tus habilidades separadas por comas: ").split(',')
    print(skills)

    carreras = cargar_carreras_desde_json(r'C:\Users\Jose Luixrax\Develop\CEIABD\MIA\Sistemas Expertos\carreras2.json')
    carreras_recomendadas = recomendar_carrera(skills, carreras)

    if carreras_recomendadas:
        print("\nBasado en tus habilidades, las siguientes carreras podrían ser adecuadas para ti:")
        for carrera in carreras_recomendadas:
            print("-", carrera)
    else:
        print("\nLo siento, no encontramos ninguna carrera que coincida con tus habilidades.")

if __name__ == "__main__":
    main()
