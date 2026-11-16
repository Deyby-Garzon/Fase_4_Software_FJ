# Excepciones personalizadas del sistema

# Estas excepciones nos permiten identificar diferentes
# tipos de errores dentro del programa sin cerrar
# completamente la aplicacion.


class DatoInvalidoError(Exception):
    # Se utiliza cuando un dato recibido no cumple
    # con las condiciones necesarias.
    pass


class ClienteInvalidoError(Exception):
    # Se utiliza cuando no es posible crear o procesar
    # correctamente un cliente.
    pass


class ServicioInvalidoError(Exception):
    # Se utiliza cuando los datos de un servicio
    # no son correctos.
    pass


class ServicioNoDisponibleError(Exception):
    # Se utiliza cuando alguien intenta utilizar
    # un servicio que no esta disponible.
    pass


class DuracionInvalidaError(Exception):
    # Se utiliza cuando la duracion de un servicio
    # es incorrecta.
    pass


class ReservaInvalidaError(Exception):
    # Esta excepcion se utilizara posteriormente
    # cuando trabajemos con las reservas.
    pass


class OperacionNoPermitidaError(Exception):
    # Se utiliza cuando se intenta realizar una accion
    # que no esta permitida dentro del sistema.
    pass