"""Servicios especializados y cálculo polimórfico de costos."""
from abc import abstractmethod
from entidades import Entidad
from excepciones import DatosInvalidosError, ServicioNoDisponibleError

class Servicio(Entidad):
    """Clase abstracta común a todos los servicios."""

    def __init__(self, codigo, nombre, tarifa, disponible=True):
        super().__init__(codigo)
        self.nombre = self._validar_texto(nombre, "nombre")
        self.tarifa = self._validar_numero(tarifa, "tarifa")
        self.disponible = bool(disponible)

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(f"El {campo} del servicio es obligatorio.")
        return valor.strip()

    @staticmethod
    def _validar_numero(valor, campo):
        try:
            numero = float(valor)
        except (TypeError, ValueError) as exc:
            raise DatosInvalidosError(f"La {campo} debe ser numérica.") from exc
        if numero <= 0:
            raise DatosInvalidosError(f"La {campo} debe ser mayor que cero.")
        return numero

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """
        Variante flexible del cálculo:
        calcular_costo(duracion), calcular_costo(duracion, impuesto)
        o calcular_costo(duracion, impuesto, descuento).
        En Python se simula la sobrecarga con parámetros opcionales.
        """
        self.validar_disponibilidad()
        horas = self._validar_numero(duracion, "duración")
        impuesto = float(impuesto)
        descuento = float(descuento)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise DatosInvalidosError("Impuesto y descuento deben estar entre 0 y 1.")
        subtotal = self._calcular_subtotal(horas)
        total = subtotal * (1 - descuento) * (1 + impuesto)
        if total < 0 or total > 1_000_000_000:
            raise DatosInvalidosError("El cálculo produjo un valor fuera del rango permitido.")
        return round(total, 2)

    @abstractmethod
    def _calcular_subtotal(self, duracion):
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        raise NotImplementedError


class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, tarifa_por_hora, capacidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_por_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def _calcular_subtotal(self, duracion):
        return self.tarifa * duracion

    def describir(self):
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} | Tarifa/hora: ${self.tarifa:.2f}"


class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, tarifa_por_hora, unidades, disponible=True):
        super().__init__(codigo, nombre, tarifa_por_hora, disponible)
        if not isinstance(unidades, int) or unidades <= 0:
            raise DatosInvalidosError("Las unidades deben ser un entero positivo.")
        self.unidades = unidades

    def _calcular_subtotal(self, duracion):
        return self.tarifa * duracion * self.unidades

    def describir(self):
        return f"Equipo: {self.nombre} | Unidades: {self.unidades} | Tarifa/unidad/hora: ${self.tarifa:.2f}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre, tarifa_por_hora, especialidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_por_hora, disponible)
        self.especialidad = self._validar_texto(especialidad, "especialidad")

    def _calcular_subtotal(self, duracion):
        return self.tarifa * duracion

    def describir(self):
        return f"Asesoría: {self.nombre} | Especialidad: {self.especialidad} | Tarifa/hora: ${self.tarifa:.2f}"
