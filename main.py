import random
from collections import Counter

from clases.clases_concretas import Guerrero, Mago, Arquero, Sanador


CLASES_DISPONIBLES = {
    "guerrero": Guerrero,
    "mago": Mago,
    "arquero": Arquero,
    "sanador": Sanador,
}


def batalla(equipo1, equipo2):
    """Simula una batalla por turnos mediante polimorfismo puro."""
    if not equipo1 or not equipo2:
        raise ValueError("Los dos equipos deben tener al menos un personaje.")

    for personaje in equipo1 + equipo2:
        personaje.salud = personaje.salud_maxima
        personaje._defendiendo = False

    turno = 1
    while any(p.esta_vivo() for p in equipo1) and any(p.esta_vivo() for p in equipo2):
        print(f"\n{'=' * 55}\n⚔️  TURNO {turno}\n{'=' * 55}")

        for personaje in equipo1:
            if personaje.esta_vivo() and any(e.esta_vivo() for e in equipo2):
                personaje.seleccionar_accion(equipo1, equipo2)

        for personaje in equipo2:
            if personaje.esta_vivo() and any(e.esta_vivo() for e in equipo1):
                personaje.seleccionar_accion(equipo2, equipo1)

        imprimir_resumen(equipo1, equipo2)
        turno += 1

        if turno > 200:
            print("La batalla terminó en empate por límite de turnos.")
            return None

    ganador = 1 if any(p.esta_vivo() for p in equipo1) else 2
    print(f"\n🏆 ¡EQUIPO {ganador} GANA!")
    return ganador


def imprimir_resumen(equipo1, equipo2):
    print("\nEstado de los equipos:")
    for numero, equipo in enumerate((equipo1, equipo2), start=1):
        estado = " | ".join(f"{p.nombre}: {p.salud:.1f}" for p in equipo)
        print(f"Equipo {numero}: {estado}")


def leer_numero_positivo(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor <= 0:
                raise ValueError("El valor debe ser mayor que cero.")
            return valor
        except ValueError as error:
            print(f"Entrada no válida: {error}")


def crear_personaje(personajes):
    print("\nTipos permitidos: Guerrero, Mago, Arquero y Sanador")
    tipo = input("Tipo de personaje: ").strip().lower()
    if tipo not in CLASES_DISPONIBLES:
        raise ValueError("El tipo de personaje no está permitido.")

    nombre = input("Nombre: ").strip()
    salud = leer_numero_positivo("Salud máxima: ")
    ataque = leer_numero_positivo("Ataque base: ")
    defensa = leer_numero_positivo("Defensa base: ")

    personaje = CLASES_DISPONIBLES[tipo](nombre, salud, ataque, defensa)
    personajes.append(personaje)
    print(f"Personaje creado correctamente: {personaje}")


def ver_personajes(personajes):
    if not personajes:
        print("No hay personajes creados.")
        return
    print("\nPERSONAJES CREADOS")
    for indice, personaje in enumerate(personajes, start=1):
        print(f"{indice}. {personaje}")


def simular_batalla(personajes):
    if len(personajes) < 2:
        print("Se necesitan al menos dos personajes.")
        return

    maximo = len(personajes) // 2
    cantidad = int(leer_numero_positivo(f"Personajes por equipo (máximo {maximo}): "))
    if cantidad > maximo:
        raise ValueError(f"Solo se permiten hasta {maximo} personajes por equipo.")

    seleccionados = random.sample(personajes, cantidad * 2)
    equipo1 = seleccionados[:cantidad]
    equipo2 = seleccionados[cantidad:]

    print("\nEquipo 1:", ", ".join(p.nombre for p in equipo1))
    print("Equipo 2:", ", ".join(p.nombre for p in equipo2))
    batalla(equipo1, equipo2)


def ver_estadisticas(personajes):
    conteo = Counter(p.obtener_clase() for p in personajes)
    print("\nESTADÍSTICAS")
    for clase in ("Guerrero", "Mago", "Arquero", "Sanador"):
        print(f"{clase}: {conteo.get(clase, 0)}")
    print(f"Total: {len(personajes)}")


def mostrar_menu():
    print("\n" + "=" * 40)
    print("       VIDEOJUEGO POR TURNOS")
    print("=" * 40)
    print("1. Crear personaje")
    print("2. Ver personajes")
    print("3. Simular batalla")
    print("4. Ver estadísticas")
    print("5. Salir")


def main():
    personajes = []
    acciones = {
        "1": lambda: crear_personaje(personajes),
        "2": lambda: ver_personajes(personajes),
        "3": lambda: simular_batalla(personajes),
        "4": lambda: ver_estadisticas(personajes),
    }

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "5":
            print("Programa finalizado.")
            break
        try:
            accion = acciones.get(opcion)
            if accion is None:
                raise ValueError("Selecciona una opción del 1 al 5.")
            accion()
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")


if __name__ == "__main__":
    main()
