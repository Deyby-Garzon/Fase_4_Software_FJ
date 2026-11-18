# Pruebas del sistema
# Aqui se realizaran las operaciones validas e invalidas
# para comprobar el manejo de excepciones y la estabilidad del programa

# ==========================================================
# IMPORTACIONES
# ==========================================================

# Importamos el sistema principal para poder crear
# clientes, servicios y reservas sin utilizar el menú.
from Main import SistemaSoftwareFJ

# Importamos los tres tipos de servicios
# utilizados por Software FJ.
from Servicios import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

# Importamos las excepciones para comprobar
# que los errores sean controlados correctamente.
from Excepciones import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError
)


# ==========================================================
# FUNCIÓN GENERAL PARA EJECUTAR PRUEBAS
# ==========================================================

def ejecutar_prueba(
    numero,
    descripcion,
    funcion,
    error_esperado=None
):
    # Esta función permite ejecutar cada prueba por separado.
    #
    # Si ocurre un error, el programa no se cierra
    # y continúa automáticamente con la siguiente prueba.

    print(
        "\n=============================================="
    )

    print(
        f"PRUEBA {numero}: {descripcion}"
    )

    print(
        "=============================================="
    )


    try:

        # Ejecutamos la función correspondiente
        # a la prueba actual.
        funcion()


        # Si esperábamos un error y no ocurrió,
        # indicamos que la prueba no dio el resultado esperado.
        if error_esperado is not None:

            print(
                "RESULTADO: PRUEBA NO SUPERADA"
            )

            print(
                "Se esperaba un error, pero la operación fue aceptada."
            )


        else:

            print(
                "RESULTADO: PRUEBA SUPERADA"
            )


    except Exception as error:

        # Si esta prueba estaba diseñada para producir
        # un determinado error, comprobamos su tipo.
        if (
            error_esperado is not None
            and isinstance(
                error,
                error_esperado
            )
        ):

            print(
                "RESULTADO: PRUEBA SUPERADA"
            )

            print(
                f"Error controlado correctamente: {error}"
            )


        else:

            # Si apareció un error que no esperábamos,
            # indicamos que la prueba debe revisarse.
            print(
                "RESULTADO: PRUEBA NO SUPERADA"
            )

            print(
                f"Error inesperado: {error}"
            )


# ==========================================================
# CREACIÓN DEL SISTEMA PARA LAS PRUEBAS
# ==========================================================

# Utilizamos una sola instancia para que los datos
# creados en las primeras pruebas puedan ser utilizados
# posteriormente por las demás.
sistema = SistemaSoftwareFJ()


# ==========================================================
# PRUEBA 1 - CLIENTE VÁLIDO
# ==========================================================

def prueba_1():

    cliente = sistema.registrar_cliente(
        "1001",
        "Daniela Briceño",
        "daniela@email.com",
        "3001234567"
    )

    print(
        cliente.mostrar_informacion()
    )


# ==========================================================
# PRUEBA 2 - CLIENTE CON CORREO INVÁLIDO
# ==========================================================

def prueba_2():

    # Este correo no tiene una estructura válida,
    # por lo tanto debe producir un error controlado.
    sistema.registrar_cliente(
        "1002",
        "Laura Gómez",
        "correo_incorrecto",
        "3012345678"
    )


# ==========================================================
# PRUEBA 3 - CLIENTE REPETIDO
# ==========================================================

def prueba_3():

    # La identificación 1001 ya fue utilizada
    # correctamente en la primera prueba.
    sistema.registrar_cliente(
        "1001",
        "Otro Cliente",
        "otro@email.com",
        "3023456789"
    )


# ==========================================================
# PRUEBA 4 - SERVICIOS VÁLIDOS
# ==========================================================

def prueba_4():

    # Registramos una sala.
    sala = ReservaSala(
        "S001",
        "Sala Principal",
        50000,
        20
    )

    sistema.registrar_servicio(
        sala
    )


    # Registramos un equipo.
    equipo = AlquilerEquipo(
        "S002",
        "Alquiler Portátil",
        30000,
        "Computador portátil"
    )

    sistema.registrar_servicio(
        equipo
    )


    # Registramos una asesoría especializada.
    asesoria = AsesoriaEspecializada(
        "S003",
        "Asesoría de Software",
        70000,
        "Desarrollo de software"
    )

    sistema.registrar_servicio(
        asesoria
    )


    print(
        "Los tres tipos de servicio fueron registrados correctamente."
    )


# ==========================================================
# PRUEBA 5 - SERVICIO CON PRECIO INVÁLIDO
# ==========================================================

def prueba_5():

    # Utilizamos texto donde debería existir
    # un valor numérico para el precio.
    servicio_invalido = ReservaSala(
        "S004",
        "Sala Incorrecta",
        "precio_invalido",
        10
    )

    sistema.registrar_servicio(
        servicio_invalido
    )


# ==========================================================
# PRUEBA 6 - SERVICIO REPETIDO
# ==========================================================

def prueba_6():

    # S001 ya fue registrado en la prueba 4.
    servicio_repetido = ReservaSala(
        "S001",
        "Otra Sala",
        60000,
        15
    )

    sistema.registrar_servicio(
        servicio_repetido
    )
