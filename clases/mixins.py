class LogMixin:
    def log(self, mensaje):
        print(f"[{self.__class__.__name__}] {mensaje}")


class InventarioMixin:
    def _preparar_inventario(self):
        if not hasattr(self, "inventario"):
            self.inventario = []

    def agregar_item(self, item):
        self._preparar_inventario()
        if not isinstance(item, str) or not item.strip():
            raise ValueError("El objeto debe tener un nombre válido.")
        self.inventario.append(item.strip())
        self.log(f"Se agregó '{item.strip()}' al inventario.")

    def usar_item(self, item):
        self._preparar_inventario()
        if item not in self.inventario:
            self.log(f"El objeto '{item}' no está en el inventario.")
            return False
        self.inventario.remove(item)
        self.log(f"Usó el objeto '{item}'.")
        return True

    def listar_inventario(self):
        self._preparar_inventario()
        contenido = ", ".join(self.inventario) if self.inventario else "Vacío"
        print(f"Inventario de {self.nombre}: {contenido}")
        return list(self.inventario)
