from abc import ABC, abstractmethod


class IAtacante(ABC):
    @abstractmethod
    def atacar(self, objetivo):
        pass


class IDefensor(ABC):
    @abstractmethod
    def defender(self):
        pass

    @abstractmethod
    def obtener_defensa_total(self):
        pass


class ICurable(ABC):
    @abstractmethod
    def curar_aliado(self, aliado, cantidad):
        pass

    @abstractmethod
    def revivir(self, aliado):
        pass


class IHabilidadEspecial(ABC):
    @abstractmethod
    def usar_habilidad_especial(self):
        pass

    @abstractmethod
    def obtener_costo_habilidad(self):
        pass
