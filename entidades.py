"""Define la abstracción general de las entidades del sistema."""
from abc import ABC, abstractmethod
from datetime import datetime

class Entidad(ABC):
    """Clase abstracta base para objetos identificables."""

    def __init__(self, identificador):
        identificador = str(identificador).strip()
        if not identificador:
            raise ValueError("El identificador no puede estar vacío.")
        self._identificador = identificador
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        """Devuelve el identificador sin permitir su modificación directa."""
        return self._identificador

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        """Cada entidad concreta debe proporcionar su descripción."""
        raise NotImplementedError
