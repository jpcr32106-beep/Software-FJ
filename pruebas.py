"""Pruebas automatizadas básicas del sistema (ejecutar: python -m unittest -v)."""
import unittest
from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva
from sistema import SistemaGestion
from excepciones import DatosInvalidosError, EstadoReservaError, ServicioNoDisponibleError

class PruebasSoftwareFJ(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaGestion()
        self.cliente = Cliente("T-1", "Ana Pérez", "ana@example.com", "3001234567")
        self.sala = ReservaSala("S-1", "Sala A", 40000, 10)
        self.sistema.registrar_cliente(self.cliente)
        self.sistema.agregar_servicio(self.sala)

    def test_cliente_valido(self):
        self.assertEqual(self.cliente.nombre, "Ana Pérez")

    def test_correo_invalido(self):
        with self.assertRaises(DatosInvalidosError):
            Cliente("T-2", "Ana", "correo", "3001234567")

    def test_cliente_duplicado(self):
        with self.assertRaises(Exception):
            self.sistema.registrar_cliente(self.cliente)

    def test_calculo_sala(self):
        self.assertEqual(self.sala.calcular_costo(2), 80000.0)

    def test_calculo_con_impuesto_descuento(self):
        self.assertEqual(self.sala.calcular_costo(2, 0.19, 0.10), 85680.0)

    def test_equipo_polimorfismo(self):
        equipo = AlquilerEquipo("E-1", "Portátiles", 10000, 2)
        self.assertEqual(equipo.calcular_costo(3), 60000.0)

    def test_asesoria_polimorfismo(self):
        asesoria = AsesoriaEspecializada("A-1", "Consultoría", 50000, "TI")
        self.assertEqual(asesoria.calcular_costo(2), 100000.0)

    def test_servicio_no_disponible(self):
        servicio = ReservaSala("S-2", "Cerrada", 10000, 5, disponible=False)
        with self.assertRaises(ServicioNoDisponibleError):
            servicio.calcular_costo(1)

    def test_confirmar_reserva(self):
        reserva = Reserva("R-1", self.cliente, self.sala, 2)
        self.assertEqual(reserva.confirmar(), 80000.0)
        self.assertEqual(reserva.estado, "CONFIRMADA")

    def test_procesar_sin_confirmar(self):
        reserva = Reserva("R-2", self.cliente, self.sala, 1)
        with self.assertRaises(EstadoReservaError):
            reserva.procesar()

    def test_cancelar_reserva(self):
        reserva = Reserva("R-3", self.cliente, self.sala, 1)
        self.assertTrue(reserva.cancelar())
        self.assertEqual(reserva.estado, "CANCELADA")

if __name__ == "__main__":
    unittest.main()
