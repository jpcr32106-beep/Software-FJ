"""Modelo de reservas y operaciones sobre su estado."""
from entidades import Entidad
from excepciones import ReservaInvalidaError, EstadoReservaError

class Reserva(Entidad):
    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, codigo, cliente, servicio, duracion):
        super().__init__(codigo)
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("La reserva requiere un cliente y un servicio.")
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as exc:
            raise ReservaInvalidaError("La duración debe ser numérica.") from exc
        if duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser mayor que cero.")
        servicio.validar_disponibilidad()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._total = None

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def total(self):
        return self._total

    def confirmar(self):
        if self._estado != "PENDIENTE":
            raise EstadoReservaError("Solo se pueden confirmar reservas pendientes.")
        self._servicio.validar_disponibilidad()
        self._total = self._servicio.calcular_costo(self._duracion)
        self._estado = "CONFIRMADA"
        return self._total

    def cancelar(self):
        if self._estado not in ("PENDIENTE", "CONFIRMADA"):
            raise EstadoReservaError("No se puede cancelar una reserva procesada o cancelada.")
        self._estado = "CANCELADA"
        return True

    def procesar(self):
        if self._estado != "CONFIRMADA":
            raise EstadoReservaError("La reserva debe estar confirmada antes de procesarse.")
        self._estado = "PROCESADA"
        return self._total

    def describir(self):
        return (f"Reserva {self.identificador} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} h | Estado: {self.estado}")
