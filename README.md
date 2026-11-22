# Software FJ — Sistema Integral de Gestión

Aplicación de consola desarrollada en Python con programación orientada a objetos. Gestiona clientes, servicios (salas, alquiler de equipos y asesorías) y reservas sin utilizar bases de datos. Los datos viven en listas y objetos durante la ejecución; el archivo de log conserva eventos y errores.

# Requisitos
- Python 3.10 o superior.
- No requiere instalar paquetes externos.

# Ejecución
Desde esta carpeta, abrir una terminal y ejecutar:

```bash
python main.py

Para ejecutar las pruebas automatizadas:

```bash
python -m unittest pruebas -v

# Estructura
- `entidades.py`: clase abstracta Entidad.
- `clientes.py`: Cliente y validaciones encapsuladas.
- `servicios.py`: Servicio abstracto y tres servicios concretos.
- `reservas.py`: creación, confirmación, cancelación y procesamiento.
- `excepciones.py`: excepciones personalizadas.
- `sistema.py`: listas internas, operaciones de gestión y logging.
- `main.py`: demostración secuencial de 15 operaciones.
- `pruebas.py`: pruebas automatizadas.
- `logs/sistema.log`: registro generado automáticamente.

# Decisiones de diseño
Python no implementa sobrecarga tradicional de métodos por firma como otros lenguajes. Para cumplir ese propósito, `Servicio.calcular_costo` acepta parámetros opcionales: duración, impuesto y descuento. Así permite distintas formas de invocación con un único método.

Los errores de dominio se representan con excepciones personalizadas. Las operaciones de demostración están aisladas para que un fallo no detenga el resto. Los registros se guardan en un archivo de texto mediante el módulo estándar `logging`.