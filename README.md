Video juego  por Turnos
Descripción
Este proyecto es un videojuego de rol por turnos desarrollado en Python utilizando Programación Orientada a Objetos.

El programa permite crear diferentes personajes, formar equipos y realizar batallas automáticas. Cada personaje tiene diferentes características, ataques y habilidades especiales.

Personajes
El programa cuenta con cuatro tipos de personajes:

Guerrero
Tiene buen ataque y defensa.
Puede atacar y defenderse.
Su habilidad especial es Golpe aplastante.
Mago
Realiza ataques mágicos.
Puede curar aliados.
Puede revivir personajes.
Su habilidad especial es Bola de fuego.
Arquero
Tiene buen ataque, pero poca defensa.
Puede ignorar parte de la defensa del enemigo.
Su habilidad especial es Flecha certera.
Sanador
Tiene mucha salud.
Puede curar y revivir aliados.
Puede defenderse.
Su habilidad especial es Bendición.
Estructura del proyecto
videojuego/
│
├── main.py
├── README.md
└── clases/
    ├── personaje.py
    ├── interfaces.py
    ├── mixins.py
    └── clases_concretas.py
Archivos
main.py: contiene el menú principal y la batalla.
personaje.py: contiene la clase abstracta Personaje.
interfaces.py: contiene las interfaces del programa.
mixins.py: contiene el registro de acciones y el inventario.
clases_concretas.py: contiene las clases Guerrero, Mago, Arquero y Sanador.
Conceptos utilizados
En este proyecto se utilizan varios conceptos de Programación Orientada a Objetos:

Clases: se utilizan para crear los personajes.
Herencia: permite compartir características entre las clases.
Clase abstracta: sirve como base para los personajes.
Interfaces: indican los métodos que debe tener cada personaje.
Polimorfismo: permite que cada personaje realice una misma acción de diferente manera.
Mixins: agregan funciones como el inventario y el registro de acciones.
Excepciones: permiten controlar errores utilizando try y except.
Menú principal
Cuando se ejecuta el programa aparece el siguiente menú:

========================================
       VIDEOJUEGO POR TURNOS
========================================
1. Crear personaje
2. Ver personajes
3. Simular batalla
4. Ver estadísticas
5. Salir
========================================
Opciones
1. Crear personaje

Permite seleccionar el tipo de personaje y escribir:

Nombre.
Salud máxima.
Ataque base.
Defensa base.
2. Ver personajes

Muestra los personajes que han sido creados y sus estadísticas.

3. Simular batalla

Forma dos equipos con los personajes disponibles y comienza una batalla por turnos.

4. Ver estadísticas

Muestra cuántos personajes existen de cada tipo.

5. Salir

Finaliza el programa.

Batalla
La batalla se realiza por turnos.

Durante cada turno los personajes pueden realizar acciones como:

Atacar.
Defenderse.
Curar.
Revivir aliados.
Utilizar habilidades especiales.
La batalla termina cuando uno de los equipos se queda sin personajes vivos.

El programa utiliza polimorfismo para que cada personaje decida cómo realizar sus acciones.

Validaciones
El programa verifica que:

El personaje seleccionado sea válido.
Las estadísticas sean números positivos.
Existan suficientes personajes para comenzar una batalla.
Las opciones del menú sean correctas.
También utiliza try/except para evitar que el programa termine cuando el usuario introduce un dato incorrecto.