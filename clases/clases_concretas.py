import random

from clases.personaje import Personaje
from clases.interfaces import IAtacante, IDefensor, ICurable, IHabilidadEspecial
from clases.mixins import LogMixin, InventarioMixin


def _defensa_del(objetivo):
    return objetivo.obtener_defensa_total()


class Guerrero(LogMixin, InventarioMixin, Personaje, IAtacante, IDefensor, IHabilidadEspecial):
    def atacar(self, objetivo):
        dano = max(1, self.ataque_base * 1.5 - _defensa_del(objetivo))
        self.log(f"{self.nombre} ataca a {objetivo.nombre} con su espada.")
        return objetivo.recibir_dano(dano)

    def usar_habilidad_especial(self, objetivo=None, aliados=None, enemigos=None):
        if objetivo is None:
            return 0
        dano = max(1, self.ataque_base * 2 - _defensa_del(objetivo))
        self.log(f"{self.nombre} usa GOLPE APLASTANTE contra {objetivo.nombre}.")
        recibido = objetivo.recibir_dano(dano)
        self._defensa_reducida = True
        return recibido

    def obtener_costo_habilidad(self):
        return 20

    def obtener_defensa_total(self):
        defensa = self.defensa_base * (2 if self._defendiendo else 1)
        if getattr(self, "_defensa_reducida", False):
            defensa *= 0.5
            self._defensa_reducida = False
        return defensa

    def obtener_clase(self):
        return "Guerrero"

    def seleccionar_accion(self, aliados, enemigos):
        vivos = [e for e in enemigos if e.esta_vivo()]
        if not vivos:
            return
        objetivo = random.choice(vivos)
        if random.random() < 0.25:
            self.usar_habilidad_especial(objetivo, aliados, enemigos)
        elif random.random() < 0.15:
            self.defender()
        else:
            self.atacar(objetivo)


class Mago(LogMixin, InventarioMixin, Personaje, IAtacante, ICurable, IHabilidadEspecial):
    def atacar(self, objetivo):
        dano = self.ataque_base * 2.0
        self.log(f"{self.nombre} lanza un proyectil mágico a {objetivo.nombre}; ignora la defensa.")
        return objetivo.recibir_dano(dano)

    def curar_aliado(self, aliado, cantidad):
        self.log(f"{self.nombre} lanza un hechizo de curación sobre {aliado.nombre}.")
        return aliado.curar(cantidad)

    def revivir(self, aliado):
        if aliado.esta_vivo():
            self.log(f"{aliado.nombre} no necesita ser revivido.")
            return False
        aliado.salud = aliado.salud_maxima * 0.25
        self.log(f"{self.nombre} revivió a {aliado.nombre} con {aliado.salud:.1f} de salud.")
        return True

    def usar_habilidad_especial(self, objetivo=None, aliados=None, enemigos=None):
        enemigos = enemigos or ([objetivo] if objetivo else [])
        self.log(f"{self.nombre} usa BOLA DE FUEGO y daña a todos los enemigos.")
        total = 0
        for enemigo in [e for e in enemigos if e.esta_vivo()]:
            total += enemigo.recibir_dano(self.ataque_base * 1.4)
        return total

    def obtener_costo_habilidad(self):
        return 30

    def obtener_clase(self):
        return "Mago"

    def seleccionar_accion(self, aliados, enemigos):
        heridos = [a for a in aliados if a.esta_vivo() and a.salud < a.salud_maxima * 0.45]
        caidos = [a for a in aliados if not a.esta_vivo()]
        vivos = [e for e in enemigos if e.esta_vivo()]
        if caidos and random.random() < 0.15:
            self.revivir(random.choice(caidos))
        elif heridos and random.random() < 0.45:
            self.curar_aliado(min(heridos, key=lambda a: a.salud / a.salud_maxima), self.ataque_base * 1.5)
        elif vivos and random.random() < 0.25:
            self.usar_habilidad_especial(random.choice(vivos), aliados, enemigos)
        elif vivos:
            self.atacar(random.choice(vivos))


class Arquero(LogMixin, InventarioMixin, Personaje, IAtacante, IHabilidadEspecial):
    def atacar(self, objetivo):
        defensa_parcial = _defensa_del(objetivo) * 0.5
        dano = max(1, self.ataque_base * 1.2 - defensa_parcial)
        self.log(f"{self.nombre} dispara a {objetivo.nombre} e ignora la mitad de su defensa.")
        return objetivo.recibir_dano(dano)

    def usar_habilidad_especial(self, objetivo=None, aliados=None, enemigos=None):
        if objetivo is None:
            return 0
        critico = random.random() < 0.50
        multiplicador = 3.0 if critico else 1.7
        dano = max(1, self.ataque_base * multiplicador - _defensa_del(objetivo) * 0.25)
        texto = "CRÍTICO" if critico else "impacto normal"
        self.log(f"{self.nombre} usa FLECHA CERTERA contra {objetivo.nombre}: {texto}.")
        return objetivo.recibir_dano(dano)

    def obtener_costo_habilidad(self):
        return 15

    def obtener_clase(self):
        return "Arquero"

    def seleccionar_accion(self, aliados, enemigos):
        vivos = [e for e in enemigos if e.esta_vivo()]
        if vivos:
            objetivo = min(vivos, key=lambda e: e.salud)
            if random.random() < 0.30:
                self.usar_habilidad_especial(objetivo, aliados, enemigos)
            else:
                self.atacar(objetivo)


class Sanador(LogMixin, InventarioMixin, Personaje, ICurable, IDefensor, IHabilidadEspecial):
    def atacar(self, objetivo):
        dano = max(1, self.ataque_base * 0.8 - _defensa_del(objetivo))
        self.log(f"{self.nombre} golpea a {objetivo.nombre} con su báculo.")
        return objetivo.recibir_dano(dano)

    def curar_aliado(self, aliado, cantidad):
        self.log(f"{self.nombre} realiza una curación poderosa sobre {aliado.nombre}.")
        return aliado.curar(cantidad * 1.5)

    def revivir(self, aliado):
        if aliado.esta_vivo():
            self.log(f"{aliado.nombre} no necesita ser revivido.")
            return False
        aliado.salud = aliado.salud_maxima * 0.40
        self.log(f"{self.nombre} revivió a {aliado.nombre} con {aliado.salud:.1f} de salud.")
        return True

    def usar_habilidad_especial(self, objetivo=None, aliados=None, enemigos=None):
        aliados = aliados or []
        self.log(f"{self.nombre} usa BENDICIÓN y cura a todos los aliados vivos.")
        total = 0
        for aliado in [a for a in aliados if a.esta_vivo()]:
            total += aliado.curar(self.ataque_base * 1.8)
        return total

    def obtener_costo_habilidad(self):
        return 25

    def obtener_defensa_total(self):
        return self.defensa_base * (2 if self._defendiendo else 1)

    def obtener_clase(self):
        return "Sanador"

    def seleccionar_accion(self, aliados, enemigos):
        heridos = [a for a in aliados if a.esta_vivo() and a.salud < a.salud_maxima * 0.70]
        caidos = [a for a in aliados if not a.esta_vivo()]
        vivos = [e for e in enemigos if e.esta_vivo()]
        if caidos and random.random() < 0.25:
            self.revivir(random.choice(caidos))
        elif len(heridos) >= 2 and random.random() < 0.50:
            self.usar_habilidad_especial(None, aliados, enemigos)
        elif heridos:
            aliado = min(heridos, key=lambda a: a.salud / a.salud_maxima)
            self.curar_aliado(aliado, self.ataque_base * 2)
        elif random.random() < 0.25:
            self.defender()
        elif vivos:
            self.atacar(random.choice(vivos))
