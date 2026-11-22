"""Excepciones propias del sistema Software FJ."""

class ErrorSoftwareFJ(Exception):
    """Excepción base para los errores controlados de la aplicación."""

class DatosInvalidosError(ErrorSoftwareFJ):
    """Se lanza cuando un dato no cumple las reglas de validación."""

class ClienteDuplicadoError(ErrorSoftwareFJ):
    """Se lanza cuando ya existe un cliente con la misma identificación."""

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio no está habilitado o no tiene disponibilidad."""

class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva no puede crearse o procesarse."""

class EstadoReservaError(ErrorSoftwareFJ):
    """Se lanza cuando una operación no corresponde al estado de la reserva."""
