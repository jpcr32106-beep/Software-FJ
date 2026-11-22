"""Capa de gestión: mantiene las listas internas y registra eventos."""
import logging
from pathlib import Path
from clientes import Cliente
from reservas import Reserva
from excepciones import ClienteDuplicadoError, DatosInvalidosError, ReservaInvalidaError

def configurar_logs(ruta=None):
    ruta = Path(ruta or Path(__file__).parent / "logs" / "sistema.log")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    # Evita duplicar manejadores al ejecutar varias veces desde el mismo intérprete.
    if not any(getattr(h, "baseFilename", None) == str(ruta.resolve()) for h in logger.handlers):
        manejador = logging.FileHandler(ruta, encoding="utf-8")
        manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(manejador)
    return logger

class SistemaGestion:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logger = configurar_logs()

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El objeto recibido no es un cliente válido.")
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ClienteDuplicadoError(f"Ya existe el cliente {cliente.identificador}.")
        self.clientes.append(cliente)
        self.logger.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    def agregar_servicio(self, servicio):
        from servicios import Servicio
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El objeto recibido no es un servicio válido.")
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise DatosInvalidosError(f"Ya existe el servicio {servicio.identificador}.")
        self.servicios.append(servicio)
        self.logger.info("Servicio agregado: %s", servicio.identificador)
        return servicio

    def crear_reserva(self, codigo, identificacion_cliente, codigo_servicio, duracion):
        cliente = next((c for c in self.clientes if c.identificador == str(identificacion_cliente)), None)
        servicio = next((s for s in self.servicios if s.identificador == str(codigo_servicio)), None)
        if cliente is None:
            raise ReservaInvalidaError("No se encontró el cliente solicitado.")
        if servicio is None:
            raise ReservaInvalidaError("No se encontró el servicio solicitado.")
        if any(r.identificador == str(codigo) for r in self.reservas):
            raise ReservaInvalidaError(f"Ya existe la reserva {codigo}.")
        reserva = Reserva(codigo, cliente, servicio, duracion)
        self.reservas.append(reserva)
        self.logger.info("Reserva creada: %s", codigo)
        return reserva

    def registrar_error(self, operacion, error):
        self.logger.exception("Error en %s: %s", operacion, error)

    def resumen(self):
        return (f"Clientes: {len(self.clientes)} | Servicios: {len(self.servicios)} | "
                f"Reservas: {len(self.reservas)}")
