# ==========================================================
# IMPORTACIONES
# ==========================================================

# ABC y abstractmethod permiten crear
# la clase abstracta Servicio.
from abc import ABC, abstractmethod

# Importamos las excepciones necesarias
# para controlar los errores de los servicios.
from Excepciones import (
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    DuracionInvalidaError
)

# Estas funciones guardan los eventos
# y errores dentro de eventos.log.
from Logger_sistema import (
    registrar_evento,
    registrar_error
)


# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(ABC):
    # Esta clase contiene los datos y comportamientos
    # que compartirán todos los servicios de Software FJ.

    def __init__(
        self,
        codigo,
        nombre,
        precio_base,
        disponible=True
    ):

        # Validamos el código.
        if codigo is None or str(codigo).strip() == "":
            registrar_error(
                "Se intentó crear un servicio sin código."
            )

            raise ServicioInvalidoError(
                "El código del servicio no puede estar vacío."
            )

        # Validamos el nombre.
        if nombre is None or str(nombre).strip() == "":
            registrar_error(
                "Se intentó crear un servicio sin nombre."
            )

            raise ServicioInvalidoError(
                "El nombre del servicio no puede estar vacío."
            )


        # Intentamos convertir el precio a número.
        # Esto permite controlar valores como texto o datos inválidos.
        try:
            precio_base = float(
                precio_base
            )

        except (TypeError, ValueError) as error:

            registrar_error(
                f"Precio inválido para el servicio: {precio_base}"
            )

            raise ServicioInvalidoError(
                "El precio base debe ser un número."
            ) from error


        if precio_base <= 0:
            registrar_error(
                f"Precio base no permitido: {precio_base}"
            )

            raise ServicioInvalidoError(
                "El precio base debe ser mayor que cero."
            )


        self.codigo = str(
            codigo
        ).strip()

        self.nombre = str(
            nombre
        ).strip()

        self.precio_base = precio_base

        self.disponible = bool(
            disponible
        )


        registrar_evento(
            f"Servicio creado: "
            f"{self.codigo} - {self.nombre}"
        )


    # ======================================================
    # DISPONIBILIDAD
    # ======================================================

    def verificar_disponibilidad(self):
        # Antes de procesar un servicio comprobamos
        # que se encuentre disponible.

        if not self.disponible:

            registrar_error(
                f"Servicio no disponible: "
                f"{self.codigo} - {self.nombre}"
            )

            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre} no está disponible."
            )

        return True


    # ======================================================
    # AJUSTES DEL PRECIO
    # ======================================================

    def aplicar_ajustes(
        self,
        subtotal,
        impuesto=0,
        descuento=0
    ):
        # Este método permite aplicar impuestos
        # y descuentos al valor calculado.

        try:
            impuesto = float(
                impuesto
            )

            descuento = float(
                descuento
            )

        except (TypeError, ValueError) as error:

            registrar_error(
                "Se ingresó un impuesto o descuento inválido."
            )

            raise ServicioInvalidoError(
                "El impuesto y el descuento deben ser números."
            ) from error


        # Evitamos porcentajes negativos
        # o mayores al 100%.
        if impuesto < 0 or impuesto > 100:

            registrar_error(
                f"Impuesto inválido: {impuesto}"
            )

            raise ServicioInvalidoError(
                "El impuesto debe estar entre 0 y 100."
            )


        if descuento < 0 or descuento > 100:

            registrar_error(
                f"Descuento inválido: {descuento}"
            )

            raise ServicioInvalidoError(
                "El descuento debe estar entre 0 y 100."
            )


        # Primero aplicamos el impuesto.
        total = subtotal + (
            subtotal * impuesto / 100
        )

        # Después aplicamos el descuento.
        total = total - (
            total * descuento / 100
        )

        return total


    # ======================================================
    # MÉTODOS ABSTRACTOS
    # ======================================================

    @abstractmethod
    def descripcion(self):
        # Cada servicio mostrará su propia descripción.
        pass


    @abstractmethod
    def validar_parametros(self, duracion):
        # Cada servicio validará los parámetros
        # que necesite para funcionar.
        pass


    @abstractmethod
    def calcular_costo(
        self,
        duracion,
        impuesto=0,
        descuento=0
    ):
        # impuesto y descuento son parámetros opcionales.
        #
        # Esto permite utilizar el método de diferentes formas:
        #
        # calcular_costo(duracion)
        # calcular_costo(duracion, impuesto)
        # calcular_costo(duracion, impuesto, descuento)
        #
        # De esta manera simulamos la sobrecarga de métodos
        # solicitada en el ejercicio.
        pass


# ==========================================================
# RESERVA DE SALA
# ==========================================================

class ReservaSala(Servicio):
    # Representa el servicio de alquiler
    # de salas de la empresa.

    def __init__(
        self,
        codigo,
        nombre,
        precio_base,
        capacidad,
        disponible=True
    ):

        super().__init__(
            codigo,
            nombre,
            precio_base,
            disponible
        )


        try:
            capacidad = int(
                capacidad
            )

        except (TypeError, ValueError) as error:

            registrar_error(
                f"Capacidad de sala inválida: {capacidad}"
            )

            raise ServicioInvalidoError(
                "La capacidad de la sala debe ser un número entero."
            ) from error


        if capacidad <= 0:

            registrar_error(
                f"Capacidad no permitida: {capacidad}"
            )

            raise ServicioInvalidoError(
                "La capacidad debe ser mayor que cero."
            )


        self.capacidad = capacidad


    def descripcion(self):

        return (
            f"Reserva de sala: {self.nombre} | "
            f"Capacidad: {self.capacidad} personas | "
            f"Precio por hora: ${self.precio_base:.2f}"
        )


    def validar_parametros(self, duracion):

        try:
            duracion = float(
                duracion
            )

        except (TypeError, ValueError) as error:

            registrar_error(
                f"Duración inválida para reserva de sala: {duracion}"
            )

            raise DuracionInvalidaError(
                "La duración debe ser un número."
            ) from error


        if duracion <= 0:

            registrar_error(
                f"Duración no permitida: {duracion}"
            )

            raise DuracionInvalidaError(
                "La duración debe ser mayor que cero."
            )


        return duracion


    def calcular_costo(
        self,
        duracion,
        impuesto=0,
        descuento=0
    ):

        # Confirmamos que el servicio pueda utilizarse.
        self.verificar_disponibilidad()

        # Validamos la duración.
        duracion = self.validar_parametros(
            duracion
        )

        # El valor se calcula según las horas reservadas.
        subtotal = (
            self.precio_base
            * duracion
        )

        total = self.aplicar_ajustes(
            subtotal,
            impuesto,
            descuento
        )

        registrar_evento(
            f"Costo calculado para reserva de sala "
            f"{self.codigo}: ${total:.2f}"
        )

        return total


# ==========================================================
# ALQUILER DE EQUIPO
# ==========================================================

class AlquilerEquipo(Servicio):
    # Representa el alquiler de equipos
    # ofrecidos por Software FJ.

    def __init__(
        self,
        codigo,
        nombre,
        precio_base,
        tipo_equipo,
        disponible=True
    ):

        super().__init__(
            codigo,
            nombre,
            precio_base,
            disponible
        )


        if (
            tipo_equipo is None
            or str(tipo_equipo).strip() == ""
        ):

            registrar_error(
                "Se intentó crear un alquiler sin tipo de equipo."
            )

            raise ServicioInvalidoError(
                "El tipo de equipo no puede estar vacío."
            )


        self.tipo_equipo = str(
            tipo_equipo
        ).strip()


    def descripcion(self):

        return (
            f"Alquiler de equipo: {self.nombre} | "
            f"Equipo: {self.tipo_equipo} | "
            f"Precio por hora: ${self.precio_base:.2f}"
        )


    def validar_parametros(self, duracion):

        try:
            duracion = float(
                duracion
            )

        except (TypeError, ValueError) as error:

            registrar_error(
                f"Duración inválida para alquiler: {duracion}"
            )

            raise DuracionInvalidaError(
                "La duración debe ser un número."
            ) from error


        if duracion <= 0:

            registrar_error(
                f"Duración no permitida: {duracion}"
            )

            raise DuracionInvalidaError(
                "La duración debe ser mayor que cero."
            )


        return duracion


    def calcular_costo(
        self,
        duracion,
        impuesto=0,
        descuento=0
    ):

        self.verificar_disponibilidad()

        duracion = self.validar_parametros(
            duracion
        )

        subtotal = (
            self.precio_base
            * duracion
        )

        total = self.aplicar_ajustes(
            subtotal,
            impuesto,
            descuento
        )

        registrar_evento(
            f"Costo calculado para alquiler de equipo "
            f"{self.codigo}: ${total:.2f}"
        )

        return total


# ==========================================================
# ASESORÍA ESPECIALIZADA
# ==========================================================

class AsesoriaEspecializada(Servicio):
    # Representa las asesorías ofrecidas
    # por la empresa.

    def __init__(
        self,
        codigo,
        nombre,
        precio_base,
        especialidad,
        disponible=True
    ):

        super().__init__(
            codigo,
            nombre,
            precio_base,
            disponible
        )


        if (
            especialidad is None
            or str(especialidad).strip() == ""
        ):

            registrar_error(
                "Se intentó crear una asesoría sin especialidad."
            )

            raise ServicioInvalidoError(
                "La especialidad no puede estar vacía."
            )


        self.especialidad = str(
            especialidad
        ).strip()


    def descripcion(self):

        return (
            f"Asesoría especializada: {self.nombre} | "
            f"Área: {self.especialidad} | "
            f"Precio por hora: ${self.precio_base:.2f}"
        )


    def validar_parametros(self, duracion):

        try:
            duracion = float(
                duracion
            )

        except (TypeError, ValueError) as error:

            registrar_error(
                f"Duración inválida para asesoría: {duracion}"
            )

            raise DuracionInvalidaError(
                "La duración debe ser un número."
            ) from error


        if duracion <= 0:

            registrar_error(
                f"Duración no permitida: {duracion}"
            )

            raise DuracionInvalidaError(
                "La duración debe ser mayor que cero."
            )


        return duracion


    def calcular_costo(
        self,
        duracion,
        impuesto=0,
        descuento=0
    ):

        self.verificar_disponibilidad()

        duracion = self.validar_parametros(
            duracion
        )

        subtotal = (
            self.precio_base
            * duracion
        )

        total = self.aplicar_ajustes(
            subtotal,
            impuesto,
            descuento
        )

        registrar_evento(
            f"Costo calculado para asesoría "
            f"{self.codigo}: ${total:.2f}"
        )

        return total