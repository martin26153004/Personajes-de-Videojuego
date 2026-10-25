from abc import ABC, abstractmethod


class Personaje(ABC):
    def __init__(self, nombre, salud_maxima, ataque_base, defensa_base):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        valores = (salud_maxima, ataque_base, defensa_base)
        if any(not isinstance(valor, (int, float)) or isinstance(valor, bool) for valor in valores):
            raise TypeError("Las estadísticas deben ser valores numéricos.")
        if any(valor <= 0 for valor in valores):
            raise ValueError("Las estadísticas deben ser mayores que cero.")

        self.nombre = nombre.strip()
        self.nivel = 1
        self.salud_maxima = float(salud_maxima)
        self.salud = self.salud_maxima
        self.ataque_base = float(ataque_base)
        self.defensa_base = float(defensa_base)
        self._defendiendo = False

    @abstractmethod
    def atacar(self, objetivo):
        pass

    @abstractmethod
    def usar_habilidad_especial(self):
        pass

    @abstractmethod
    def obtener_clase(self):
        pass

    def recibir_dano(self, cantidad):
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo.")
        if not self.esta_vivo():
            return 0

        dano_real = float(cantidad)
        if self._defendiendo:
            dano_real *= 0.5
            self._defendiendo = False

        dano_real = max(0, dano_real)
        self.salud = max(0, self.salud - dano_real)
        self.log(f"{self.nombre} recibió {dano_real:.1f} de daño. Salud: {self.salud:.1f}/{self.salud_maxima:.1f}")
        if not self.esta_vivo():
            self.log(f"{self.nombre} ha sido derrotado.")
        return dano_real

    def defender(self):
        if not self.esta_vivo():
            return False
        self._defendiendo = True
        self.log(f"{self.nombre} se defiende: el próximo daño se reducirá a la mitad.")
        return True

    def curar(self, cantidad):
        if cantidad < 0:
            raise ValueError("La curación no puede ser negativa.")
        if not self.esta_vivo():
            return 0
        salud_anterior = self.salud
        self.salud = min(self.salud_maxima, self.salud + cantidad)
        curacion_real = self.salud - salud_anterior
        self.log(f"{self.nombre} recuperó {curacion_real:.1f} de salud.")
        return curacion_real

    def subir_nivel(self):
        self.nivel += 1
        self.salud_maxima *= 1.10
        self.ataque_base *= 1.10
        self.defensa_base *= 1.10
        self.salud = self.salud_maxima
        self.log(f"{self.nombre} subió al nivel {self.nivel}.")

    def esta_vivo(self):
        return self.salud > 0

    def mostrar_info(self):
        print(self)

    def obtener_defensa_total(self):
        return self.defensa_base * (2 if self._defendiendo else 1)

    def seleccionar_accion(self, aliados, enemigos):
        """Punto polimórfico: cada clase decide cómo actuar sin usar isinstance."""
        vivos = [enemigo for enemigo in enemigos if enemigo.esta_vivo()]
        if vivos:
            import random
            self.atacar(random.choice(vivos))

    def __str__(self):
        estado = "Vivo" if self.esta_vivo() else "Derrotado"
        return (
            f"{self.obtener_clase()} | {self.nombre} | Nivel {self.nivel} | "
            f"Salud {self.salud:.1f}/{self.salud_maxima:.1f} | "
            f"Ataque {self.ataque_base:.1f} | Defensa {self.defensa_base:.1f} | {estado}"
        )
