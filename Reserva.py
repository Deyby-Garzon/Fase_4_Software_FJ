# ==========================================================
# IMPORTACIONES
# ==========================================================

# Importamos Cliente para comprobar que una reserva
# tenga un cliente válido registrado en el sistema.
from entidades import Cliente

# Servicio es la clase base de los diferentes servicios
# que puede reservar un cliente.
from servicios import Servicio

# Importamos las excepciones que utilizaremos
# para controlar problemas relacionados con reservas.
from excepciones import (
    ReservaInvalidaError,
    DuracionInvalidaError,
    ServicioNoDisponibleError,
    ServicioInvalidoError,
    OperacionNoPermitidaError
)

# Estas funciones permiten guardar en eventos.log
# lo que ocurre durante el manejo de las reservas.
from logger_sistema import (
    registrar_evento,
    registrar_error
)


# ==========================================================
# CLASE RESERVA
# ==========================================================

class Reserva:
    # Esta clase relaciona un cliente con uno de los
    # servicios disponibles de Software FJ.
    #
    # Cada reserva tendrá:
    # cliente
    # servicio
    # duración
    # estado
    # costo total

    def __init__(
        self,
        codigo,
        cliente,
        servicio,
        duracion
    ):

        # Verificamos que la reserva tenga un código.
        if codigo is None or str(codigo).strip() == "":

            registrar_error(
                "Se intentó crear una reserva sin código."
            )

            raise ReservaInvalidaError(
                "El código de la reserva no puede estar vacío."
            )


        # Verificamos que el objeto recibido realmente
        # corresponda a un Cliente.
        if not isinstance(cliente, Cliente):

            registrar_error(
                f"Cliente inválido para la reserva {codigo}."
            )

            raise ReservaInvalidaError(
                "La reserva debe tener un cliente válido."
            )


        # También comprobamos que el servicio recibido
        # pertenezca a alguna clase derivada de Servicio.
        if not isinstance(servicio, Servicio):

            registrar_error(
                f"Servicio inválido para la reserva {codigo}."
            )

            raise ReservaInvalidaError(
                "La reserva debe tener un servicio válido."
            )


        # Utilizamos la validación propia del servicio.
        # Cada tipo de servicio puede comprobar la duración
        # de acuerdo con sus propias reglas.
        try:

            duracion_validada = servicio.validar_parametros(
                duracion
            )

        except DuracionInvalidaError as error:

            registrar_error(
                f"No fue posible crear la reserva {codigo}: {error}"
            )

            # Utilizamos "from error" para conservar
            # la causa original del problema.
            raise ReservaInvalidaError(
                f"La duración de la reserva no es válida: {error}"
            ) from error


        # Guardamos los datos cuando todas
        # las validaciones fueron correctas.
        self.codigo = str(
            codigo
        ).strip()

        self.cliente = cliente

        self.servicio = servicio

        self.duracion = duracion_validada

        # Todas las reservas comienzan pendientes.
        self.estado = "Pendiente"

        # El costo se calculará cuando la reserva
        # sea procesada.
        self.costo_total = 0


        registrar_evento(
            f"Reserva creada: {self.codigo} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre}"
        )


    # ======================================================
    # CONFIRMAR RESERVA
    # ======================================================

    def confirmar(self):
        # No permitimos confirmar una reserva
        # que ya fue cancelada.
        if self.estado == "Cancelada":

            registrar_error(
                f"Se intentó confirmar la reserva cancelada "
                f"{self.codigo}."
            )

            raise OperacionNoPermitidaError(
                "Una reserva cancelada no puede ser confirmada."
            )


        # Tampoco necesitamos confirmar dos veces
        # una misma reserva.
        if self.estado == "Confirmada":

            registrar_error(
                f"La reserva {self.codigo} ya estaba confirmada."
            )

            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra confirmada."
            )


        # Antes de confirmar verificamos que
        # el servicio todavía esté disponible.
        self.servicio.verificar_disponibilidad()


        self.estado = "Confirmada"


        registrar_evento(
            f"Reserva confirmada: {self.codigo}"
        )


        return True


    # ======================================================
    # CANCELAR RESERVA
    # ======================================================

    def cancelar(self):
        # Evitamos cancelar varias veces
        # una misma reserva.
        if self.estado == "Cancelada":

            registrar_error(
                f"Se intentó cancelar nuevamente "
                f"la reserva {self.codigo}."
            )

            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada."
            )


        self.estado = "Cancelada"


        registrar_evento(
            f"Reserva cancelada: {self.codigo}"
        )


        return True


    # ======================================================
    # PROCESAR RESERVA
    # ======================================================

    def procesar(
        self,
        impuesto=0,
        descuento=0
    ):
        # Este método permite calcular el costo de la reserva
        # y confirmar que todo el proceso pueda realizarse.
        #
        # Aquí utilizamos try, except, else y finally para
        # manejar de forma ordenada los posibles errores.

        try:

            # Una reserva cancelada ya no puede procesarse.
            if self.estado == "Cancelada":

                raise OperacionNoPermitidaError(
                    "Una reserva cancelada no puede ser procesada."
                )


            # Calculamos el costo usando el método
            # correspondiente al tipo de servicio.
            #
            # Gracias al polimorfismo, este mismo llamado
            # funciona con ReservaSala, AlquilerEquipo
            # o AsesoriaEspecializada.
            total = self.servicio.calcular_costo(
                self.duracion,
                impuesto,
                descuento
            )


        except (
            ServicioNoDisponibleError,
            ServicioInvalidoError,
            DuracionInvalidaError,
            OperacionNoPermitidaError
        ) as error:

            # Registramos el problema encontrado.
            registrar_error(
                f"Error al procesar reserva "
                f"{self.codigo}: {error}"
            )

            # Convertimos el error recibido en un problema
            # propio de la reserva y conservamos su causa.
            raise ReservaInvalidaError(
                f"No fue posible procesar la reserva: {error}"
            ) from error


        else:

            # Este bloque se ejecuta solamente
            # cuando no se produjo ninguna excepción.
            self.costo_total = total

            # Si todavía estaba pendiente,
            # pasa automáticamente a confirmada.
            if self.estado == "Pendiente":
                self.estado = "Confirmada"


            registrar_evento(
                f"Reserva procesada correctamente: "
                f"{self.codigo} | "
                f"Total: ${self.costo_total:.2f}"
            )


            return self.costo_total


        finally:

            # finally se ejecuta tanto si la operación
            # salió bien como si ocurrió un error.
            registrar_evento(
                f"Finalizó el intento de procesamiento "
                f"de la reserva {self.codigo}."
            )


    # ======================================================
    # MOSTRAR INFORMACIÓN
    # ======================================================

    def mostrar_informacion(self):
        # Retornamos un resumen de los principales
        # datos de la reserva.

        return (
            f"Reserva: {self.codigo} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} horas | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo_total:.2f}"
        )