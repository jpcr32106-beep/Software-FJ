"""Punto de entrada: demostración secuencial de más de diez operaciones."""
import logging
from sistema import SistemaGestion
from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSoftwareFJ

def ejecutar_operacion(etiqueta, funcion):
    """Aísla cada operación para que un error no detenga toda la demostración."""
    print(f"\n[{etiqueta}]")
    try:
        resultado = funcion()
    except ErrorSoftwareFJ as error:
        print(f"Error controlado: {error}")
        logging.getLogger("SoftwareFJ").error("%s | %s", etiqueta, error, exc_info=True)
    except (TypeError, ValueError) as error:
        print(f"Error de datos: {error}")
        logging.getLogger("SoftwareFJ").error("%s | %s", etiqueta, error, exc_info=True)
    else:
        print(resultado if resultado is not None else "Operación realizada correctamente.")
    finally:
        print("Operación finalizada.")

def demo():
    sistema = SistemaGestion()
    print("=== SOFTWARE FJ: SISTEMA INTEGRAL ===")

    ejecutar_operacion("1. Registrar cliente válido", lambda: sistema.registrar_cliente(
        Cliente("1001", "Laura Gómez", "laura@gmail.com", "3001234567")))
    ejecutar_operacion("2. Registrar segundo cliente válido", lambda: sistema.registrar_cliente(
        Cliente("1002", "Carlos Ruiz", "carlos@gmail.com", "3107654321")))
    ejecutar_operacion("3. Intentar cliente con correo inválido", lambda: Cliente(
        "1003", "Pedro Díaz", "correo-no-valido", "3001234567"))
    ejecutar_operacion("4. Intentar identificación duplicada", lambda: sistema.registrar_cliente(
        Cliente("1001", "Otra Persona", "otra@gmail.com", "3112223344")))

    sala = ReservaSala("S01", "Sala de reuniones", 50000, 12)
    equipo = AlquilerEquipo("E01", "Computadores portátiles", 12000, 3)
    asesoria = AsesoriaEspecializada("A01", "Asesoría tecnológica", 80000, "Desarrollo de software")
    ejecutar_operacion("5. Crear servicio de sala", lambda: sistema.agregar_servicio(sala))
    ejecutar_operacion("6. Crear servicio de alquiler de equipos", lambda: sistema.agregar_servicio(equipo))
    ejecutar_operacion("7. Crear servicio de asesoría", lambda: sistema.agregar_servicio(asesoria))
    ejecutar_operacion("8. Intentar servicio con tarifa negativa", lambda: ReservaSala(
        "S02", "Sala inválida", -100, 10))

    ejecutar_operacion("9. Crear reserva válida", lambda: sistema.crear_reserva("R001", "1001", "S01", 2))
    reserva = sistema.reservas[0]
    ejecutar_operacion("10. Confirmar reserva", lambda: f"Total confirmado: ${reserva.confirmar():,.2f}")
    ejecutar_operacion("11. Procesar reserva", lambda: f"Total procesado: ${reserva.procesar():,.2f}")
    ejecutar_operacion("12. Intentar cancelar reserva procesada", lambda: reserva.cancelar())
    ejecutar_operacion("13. Intentar reserva con cliente inexistente", lambda: sistema.crear_reserva(
        "R002", "9999", "E01", 1))
    ejecutar_operacion("14. Calcular asesoría con impuesto y descuento",
        lambda: f"Total: ${asesoria.calcular_costo(2, 0.19, 0.10):,.2f}")
    ejecutar_operacion("15. Intentar confirmar servicio no disponible", lambda: (
        ReservaSala("S03", "Sala fuera de servicio", 30000, 8, disponible=False).calcular_costo(1)))

    # try/except/else: else solo se ejecuta si no ocurrió excepción.
    print("\n[Ejemplo try/except/else]")
    try:
        total = sala.calcular_costo(1)
    except ErrorSoftwareFJ as error:
        sistema.registrar_error("cálculo con else", error)
    else:
        print(f"Cálculo correcto: ${total:,.2f}")

    # Encadenamiento de excepciones: la excepción original se conserva como causa.
    print("\n[Ejemplo de encadenamiento de excepciones]")
    try:
        try:
            float("dato-no-numérico")
        except ValueError as causa:
            raise ErrorSoftwareFJ("No fue posible convertir el dato recibido.") from causa
    except ErrorSoftwareFJ as error:
        print(f"Excepción encadenada controlada: {error}")
        sistema.logger.exception("Ejemplo de excepción encadenada")

    print("\n=== RESUMEN FINAL ===")
    print(sistema.resumen())
    print("Los errores y eventos se guardaron en logs/sistema.log.")
    print("El sistema terminó la demostración sin detenerse por los errores controlados.")

if __name__ == "__main__":
    demo()
