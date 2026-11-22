"""Gestión y validación de clientes."""
import re
from entidades import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):
    """Representa un cliente con datos personales encapsulados."""

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatosInvalidosError(
                "El nombre debe tener al menos dos caracteres."
            )
        self._nombre = valor.strip().title()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if (
            not isinstance(valor, str)
            or not re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+",
                valor.strip()
            )
        ):
            raise DatosInvalidosError(
                "El correo electrónico no tiene un formato válido."
            )
        self._correo = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        limpio = re.sub(r"[\s+\-()]", "", str(valor))

        if not limpio.isdigit() or not 7 <= len(limpio) <= 15:
            raise DatosInvalidosError(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )
        self._telefono = limpio

    def describir(self):
        return (
            f"Cliente {self.nombre} | "
            f"ID: {self.identificador} | "
            f"Correo: {self.correo}"
        )

    def __str__(self):
        return self.describir()
