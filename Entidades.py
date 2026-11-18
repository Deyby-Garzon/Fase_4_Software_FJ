# ==========================================================
# IMPORTACIONES
# ==========================================================

# ABC y abstractmethod se utilizan para crear la clase
# abstracta Entidad, que servirá como base para otras clases.
from abc import ABC, abstractmethod

# Utilizamos re para validar de una forma sencilla
# la estructura del correo electrónico.
import re

# Importamos las excepciones que vamos a utilizar
# para controlar datos incorrectos.
from Excepciones import DatoInvalidoError, ClienteInvalidoError

# Estas funciones permiten guardar en el archivo de logs
# los eventos correctos y los errores encontrados.
from Logger_sistema import registrar_evento, registrar_error


# ==========================================================
# CLASE ABSTRACTA ENTIDAD
# ==========================================================

class Entidad(ABC):
    # Esta clase representa los datos generales que pueden
    # compartir diferentes entidades dentro del sistema.

    def __init__(self, identificacion, nombre):

        # Verificamos que la identificación tenga un valor.
        if identificacion is None or str(identificacion).strip() == "":
            registrar_error(
                "Se intentó crear una entidad sin identificación."
            )

            raise DatoInvalidoError(
                "La identificación no puede estar vacía."
            )

        # Verificamos que el nombre también tenga información.
        if nombre is None or str(nombre).strip() == "":
            registrar_error(
                "Se intentó crear una entidad sin nombre."
            )

            raise DatoInvalidoError(
                "El nombre no puede estar vacío."
            )

        # Guardamos los datos generales.
        self._identificacion = str(identificacion).strip()
        self._nombre = str(nombre).strip()


    @property
    def identificacion(self):
        # Permite consultar la identificación.
        return self._identificacion


    @property
    def nombre(self):
        # Permite consultar el nombre.
        return self._nombre


    @abstractmethod
    def mostrar_informacion(self):
        # Las clases que hereden de Entidad deberán
        # crear su propia forma de mostrar la información.
        pass


# ==========================================================
# CLASE CLIENTE
# ==========================================================

class Cliente(Entidad):
    # Cliente hereda los datos generales de Entidad.
    # Además, guarda correo y teléfono como datos privados
    # para aplicar encapsulación.

    def __init__(
        self,
        identificacion,
        nombre,
        correo,
        telefono
    ):

        try:
            # Enviamos identificación y nombre
            # al constructor de la clase Entidad.
            super().__init__(
                identificacion,
                nombre
            )

            # Los atributos con doble guion bajo son privados.
            self.__correo = ""
            self.__telefono = ""

            # Utilizamos los setters para que los datos
            # sean validados antes de guardarlos.
            self.correo = correo
            self.telefono = telefono

        except DatoInvalidoError as error:
            # Convertimos el error general en un error
            # específico de Cliente.
            #
            # "from error" permite conservar el error original
            # y demuestra encadenamiento de excepciones.
            registrar_error(
                f"Error al crear cliente: {error}"
            )

            raise ClienteInvalidoError(
                f"No fue posible crear el cliente: {error}"
            ) from error

        # Si todo fue correcto, registramos el evento.
        registrar_evento(
            f"Cliente creado correctamente: "
            f"{self.identificacion} - {self.nombre}"
        )


    # ======================================================
    # CORREO
    # ======================================================

    @property
    def correo(self):
        # Permite consultar el correo del cliente.
        return self.__correo


    @correo.setter
    def correo(self, nuevo_correo):

        # Verificamos que se haya ingresado un valor.
        if nuevo_correo is None:
            registrar_error(
                "Se intentó registrar un cliente sin correo."
            )

            raise DatoInvalidoError(
                "El correo no puede estar vacío."
            )

        nuevo_correo = str(nuevo_correo).strip()

        if nuevo_correo == "":
            registrar_error(
                "Se intentó registrar un correo vacío."
            )

            raise DatoInvalidoError(
                "El correo no puede estar vacío."
            )

        # Esta expresión permite comprobar que el correo
        # tenga una estructura básica como:
        # nombre@dominio.com
        patron_correo = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(
            patron_correo,
            nuevo_correo
        ):
            registrar_error(
                f"Correo inválido: {nuevo_correo}"
            )

            raise DatoInvalidoError(
                "El correo electrónico no tiene un formato válido."
            )

        self.__correo = nuevo_correo


    # ======================================================
    # TELÉFONO
    # ======================================================

    @property
    def telefono(self):
        # Permite consultar el teléfono del cliente.
        return self.__telefono


    @telefono.setter
    def telefono(self, nuevo_telefono):

        if nuevo_telefono is None:
            registrar_error(
                "Se intentó registrar un cliente sin teléfono."
            )

            raise DatoInvalidoError(
                "El teléfono no puede estar vacío."
            )

        # Convertimos el dato a texto para facilitar
        # su validación.
        nuevo_telefono = str(
            nuevo_telefono
        ).strip()

        if nuevo_telefono == "":
            registrar_error(
                "Se intentó registrar un teléfono vacío."
            )

            raise DatoInvalidoError(
                "El teléfono no puede estar vacío."
            )

        # Para este proyecto aceptamos números
        # entre 7 y 15 dígitos.
        if (
            not nuevo_telefono.isdigit()
            or len(nuevo_telefono) < 7
            or len(nuevo_telefono) > 15
        ):
            registrar_error(
                f"Teléfono inválido: {nuevo_telefono}"
            )

            raise DatoInvalidoError(
                "El teléfono debe contener entre 7 y 15 números."
            )

        self.__telefono = nuevo_telefono


    # ======================================================
    # MOSTRAR INFORMACIÓN
    # ======================================================

    def mostrar_informacion(self):
        # Sobrescribimos el método abstracto de Entidad
        # para mostrar los datos propios del Cliente.

        return (
            f"ID: {self.identificacion} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )