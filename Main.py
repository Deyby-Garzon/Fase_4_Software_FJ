# Archivo principal del sistema
# Aqui se integraran las clases y se ejecutara el programa

# ==========================================================
# IMPORTACIONES
# ==========================================================

# Importamos Cliente para poder registrar
# los clientes que utilizarán los servicios.
from Entidades import Cliente

# Importamos los tres tipos de servicios
# que ofrece la empresa Software FJ.
from Servicios import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

# Importamos la clase Reserva para relacionar
# clientes con los servicios disponibles.
from Reserva import Reserva

# Estas excepciones permiten controlar los diferentes
# problemas que pueden aparecer durante la ejecución.
from Excepciones import (
    DatoInvalidoError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    DuracionInvalidaError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)

# Estas funciones permiten guardar los eventos
# y errores importantes dentro de eventos.log.
from Logger_sistema import (
    registrar_evento,
    registrar_error
)


# ==========================================================
# CLASE PRINCIPAL DEL SISTEMA
# ==========================================================

class SistemaSoftwareFJ:
    # Esta clase permite organizar en un solo lugar
    # los clientes, servicios y reservas.
    #
    # La información se guarda únicamente durante
    # la ejecución utilizando listas, ya que el ejercicio
    # no permite utilizar bases de datos.

    def __init__(self):

        # Lista donde se guardarán los clientes.
        self.clientes = []

        # Lista donde se guardarán los diferentes servicios.
        self.servicios = []

        # Lista donde se guardarán las reservas.
        self.reservas = []

        registrar_evento(
            "Sistema Software FJ iniciado correctamente."
        )


    # ======================================================
    # BUSCAR CLIENTE
    # ======================================================

    def buscar_cliente(self, identificacion):

        # Recorremos la lista para encontrar un cliente
        # utilizando su identificación.
        for cliente in self.clientes:

            if cliente.identificacion == str(
                identificacion
            ).strip():

                return cliente

        return None


    # ======================================================
    # REGISTRAR CLIENTE
    # ======================================================

    def registrar_cliente(
        self,
        identificacion,
        nombre,
        correo,
        telefono
    ):

        # Primero comprobamos que la identificación
        # no esté registrada anteriormente.
        if self.buscar_cliente(
            identificacion
        ) is not None:

            registrar_error(
                f"Cliente repetido: {identificacion}"
            )

            raise ClienteInvalidoError(
                f"Ya existe un cliente con la identificación "
                f"{identificacion}."
            )


        # Cliente realiza internamente las demás
        # validaciones necesarias.
        cliente = Cliente(
            identificacion,
            nombre,
            correo,
            telefono
        )


        self.clientes.append(
            cliente
        )


        registrar_evento(
            f"Cliente agregado al sistema: "
            f"{cliente.identificacion}"
        )


        return cliente


    # ======================================================
    # BUSCAR SERVICIO
    # ======================================================

    def buscar_servicio(self, codigo):

        for servicio in self.servicios:

            if servicio.codigo == str(
                codigo
            ).strip():

                return servicio

        return None


    # ======================================================
    # REGISTRAR SERVICIO
    # ======================================================

    def registrar_servicio(
        self,
        servicio
    ):
        # Verificamos que el objeto recibido corresponda
        # realmente a uno de los servicios del sistema.
        if not isinstance(
            servicio,
            (ReservaSala, AlquilerEquipo, AsesoriaEspecializada)
        ):
            registrar_error(
                "Se intentó registrar un objeto que no es un servicio válido."
            )

            raise ServicioInvalidoError(
                "El objeto recibido no corresponde a un servicio válido."
            )

        # Verificamos que no exista otro servicio
        # con el mismo código.
        if self.buscar_servicio(
            servicio.codigo
        ) is not None:

            registrar_error(
                f"Servicio repetido: {servicio.codigo}"
            )

            raise ServicioInvalidoError(
                f"Ya existe un servicio con el código "
                f"{servicio.codigo}."
            )


        self.servicios.append(
            servicio
        )


        registrar_evento(
            f"Servicio agregado al sistema: "
            f"{servicio.codigo}"
        )


        return servicio


    # ======================================================
    # BUSCAR RESERVA
    # ======================================================

    def buscar_reserva(self, codigo):

        for reserva in self.reservas:

            if reserva.codigo == str(
                codigo
            ).strip():

                return reserva

        return None


    # ======================================================
    # CREAR RESERVA
    # ======================================================

    def crear_reserva(
        self,
        codigo,
        identificacion_cliente,
        codigo_servicio,
        duracion
    ):

        # No permitimos códigos repetidos.
        if self.buscar_reserva(
            codigo
        ) is not None:

            registrar_error(
                f"Reserva repetida: {codigo}"
            )

            raise ReservaInvalidaError(
                f"Ya existe una reserva con el código {codigo}."
            )


        # Buscamos primero el cliente.
        cliente = self.buscar_cliente(
            identificacion_cliente
        )


        if cliente is None:

            registrar_error(
                f"Cliente no encontrado: "
                f"{identificacion_cliente}"
            )

            raise ClienteInvalidoError(
                "El cliente indicado no se encuentra registrado."
            )


        # Buscamos también el servicio.
        servicio = self.buscar_servicio(
            codigo_servicio
        )


        if servicio is None:

            registrar_error(
                f"Servicio no encontrado: {codigo_servicio}"
            )

            raise ServicioInvalidoError(
                "El servicio indicado no se encuentra registrado."
            )


        # Creamos la reserva utilizando los objetos
        # encontrados anteriormente.
        reserva = Reserva(
            codigo,
            cliente,
            servicio,
            duracion
        )


        self.reservas.append(
            reserva
        )


        registrar_evento(
            f"Reserva agregada al sistema: {reserva.codigo}"
        )


        return reserva


    # ======================================================
    # MOSTRAR CLIENTES
    # ======================================================

    def mostrar_clientes(self):

        if len(self.clientes) == 0:

            print(
                "\nNo hay clientes registrados."
            )

            return


        print(
            "\n========== CLIENTES =========="
        )


        for cliente in self.clientes:

            print(
                cliente.mostrar_informacion()
            )


    # ======================================================
    # MOSTRAR SERVICIOS
    # ======================================================

    def mostrar_servicios(self):

        if len(self.servicios) == 0:

            print(
                "\nNo hay servicios registrados."
            )

            return


        print(
            "\n========== SERVICIOS =========="
        )


        for servicio in self.servicios:

            print(
                servicio.descripcion()
            )


    # ======================================================
    # MOSTRAR RESERVAS
    # ======================================================

    def mostrar_reservas(self):

        if len(self.reservas) == 0:

            print(
                "\nNo hay reservas registradas."
            )

            return


        print(
            "\n========== RESERVAS =========="
        )


        for reserva in self.reservas:

            print(
                reserva.mostrar_informacion()
            )


# ==========================================================
# FUNCIONES PARA LA INTERFAZ DE CONSOLA
# ==========================================================

def mostrar_menu():

    print(
        "\n======================================"
    )

    print(
        "       SISTEMA SOFTWARE FJ"
    )

    print(
        "======================================"
    )

    print(
        "1. Registrar cliente"
    )

    print(
        "2. Registrar reserva de sala"
    )

    print(
        "3. Registrar alquiler de equipo"
    )

    print(
        "4. Registrar asesoría especializada"
    )

    print(
        "5. Crear reserva"
    )

    print(
        "6. Confirmar reserva"
    )

    print(
        "7. Procesar reserva"
    )

    print(
        "8. Cancelar reserva"
    )

    print(
        "9. Mostrar clientes"
    )

    print(
        "10. Mostrar servicios"
    )

    print(
        "11. Mostrar reservas"
    )

    print(
        "0. Salir"
    )


# ==========================================================
# REGISTRO DE CLIENTE DESDE CONSOLA
# ==========================================================

def opcion_registrar_cliente(
    sistema
):

    print(
        "\n--- REGISTRAR CLIENTE ---"
    )


    identificacion = input(
        "Identificación: "
    )

    nombre = input(
        "Nombre: "
    )

    correo = input(
        "Correo: "
    )

    telefono = input(
        "Teléfono: "
    )


    cliente = sistema.registrar_cliente(
        identificacion,
        nombre,
        correo,
        telefono
    )


    print(
        "\nCliente registrado correctamente."
    )

    print(
        cliente.mostrar_informacion()
    )


# ==========================================================
# REGISTRO DE RESERVA DE SALA
# ==========================================================

def opcion_registrar_sala(
    sistema
):

    print(
        "\n--- REGISTRAR SALA ---"
    )


    codigo = input(
        "Código del servicio: "
    )

    nombre = input(
        "Nombre de la sala: "
    )

    precio = input(
        "Precio por hora: "
    )

    capacidad = input(
        "Capacidad de personas: "
    )


    servicio = ReservaSala(
        codigo,
        nombre,
        precio,
        capacidad
    )


    sistema.registrar_servicio(
        servicio
    )


    print(
        "\nReserva de sala registrada correctamente."
    )

    print(
        servicio.descripcion()
    )


# ==========================================================
# REGISTRO DE ALQUILER DE EQUIPO
# ==========================================================

def opcion_registrar_equipo(
    sistema
):

    print(
        "\n--- REGISTRAR EQUIPO ---"
    )


    codigo = input(
        "Código del servicio: "
    )

    nombre = input(
        "Nombre del servicio: "
    )

    precio = input(
        "Precio por hora: "
    )

    tipo_equipo = input(
        "Tipo de equipo: "
    )


    servicio = AlquilerEquipo(
        codigo,
        nombre,
        precio,
        tipo_equipo
    )


    sistema.registrar_servicio(
        servicio
    )


    print(
        "\nAlquiler de equipo registrado correctamente."
    )

    print(
        servicio.descripcion()
    )


# ==========================================================
# REGISTRO DE ASESORÍA
# ==========================================================

def opcion_registrar_asesoria(
    sistema
):

    print(
        "\n--- REGISTRAR ASESORÍA ---"
    )


    codigo = input(
        "Código del servicio: "
    )

    nombre = input(
        "Nombre de la asesoría: "
    )

    precio = input(
        "Precio por hora: "
    )

    especialidad = input(
        "Especialidad: "
    )


    servicio = AsesoriaEspecializada(
        codigo,
        nombre,
        precio,
        especialidad
    )


    sistema.registrar_servicio(
        servicio
    )


    print(
        "\nAsesoría registrada correctamente."
    )

    print(
        servicio.descripcion()
    )


# ==========================================================
# CREAR RESERVA DESDE CONSOLA
# ==========================================================

def opcion_crear_reserva(
    sistema
):

    print(
        "\n--- CREAR RESERVA ---"
    )


    codigo = input(
        "Código de la reserva: "
    )

    identificacion = input(
        "Identificación del cliente: "
    )

    codigo_servicio = input(
        "Código del servicio: "
    )

    duracion = input(
        "Duración en horas: "
    )


    reserva = sistema.crear_reserva(
        codigo,
        identificacion,
        codigo_servicio,
        duracion
    )


    print(
        "\nReserva creada correctamente."
    )

    print(
        reserva.mostrar_informacion()
    )


# ==========================================================
# CONFIRMAR RESERVA
# ==========================================================

def opcion_confirmar_reserva(
    sistema
):

    codigo = input(
        "\nCódigo de la reserva: "
    )


    reserva = sistema.buscar_reserva(
        codigo
    )


    if reserva is None:

        registrar_error(
        f"Se intentó confirmar una reserva inexistente: {codigo}"
    )

        raise ReservaInvalidaError(
            f"No existe la reserva {codigo}."
        )


    # También evitamos intentar confirmar
    # una reserva que ya fue procesada.
    if reserva.estado == "Procesada":

        raise OperacionNoPermitidaError(
            f"La reserva {codigo} ya fue procesada."
        )


    reserva.confirmar()


    print(
        "\nReserva confirmada correctamente."
    )


# ==========================================================
# PROCESAR RESERVA
# ==========================================================

def opcion_procesar_reserva(
    sistema
):

    codigo = input(
        "\nCódigo de la reserva: "
    )


    reserva = sistema.buscar_reserva(
        codigo
    )


    if reserva is None:

        registrar_error(
        f"Se intentó procesar una reserva inexistente: {codigo}"
    )

        raise ReservaInvalidaError(
            f"No existe la reserva {codigo}."
        )


    # Los valores pueden dejarse vacíos.
    impuesto = input(
        "Impuesto (%), Enter para 0: "
    )

    descuento = input(
        "Descuento (%), Enter para 0: "
    )


    if impuesto.strip() == "":
        impuesto = 0


    if descuento.strip() == "":
        descuento = 0


    total = reserva.procesar(
        impuesto,
        descuento
    )


    print(
        f"\nReserva procesada correctamente."
    )

    print(
        f"Total a pagar: ${total:.2f}"
    )


# ==========================================================
# CANCELAR RESERVA
# ==========================================================

def opcion_cancelar_reserva(
    sistema
):

    codigo = input(
        "\nCódigo de la reserva: "
    )


    reserva = sistema.buscar_reserva(
        codigo
    )


    if reserva is None:

        registrar_error(
        f"Se intentó cancelar una reserva inexistente: {codigo}"
    )

        raise ReservaInvalidaError(
            f"No existe la reserva {codigo}."
        )


    # Una reserva que ya fue procesada
    # no debería cancelarse después del pago.
    if reserva.estado == "Procesada":

        raise OperacionNoPermitidaError(
            f"La reserva {codigo} ya fue procesada "
            f"y no puede ser cancelada."
        )


    reserva.cancelar()


    print(
        "\nReserva cancelada correctamente."
    )


# ==========================================================
# EJECUCIÓN PRINCIPAL
# ==========================================================

def ejecutar_programa():

    # Creamos una sola instancia del sistema.
    sistema = SistemaSoftwareFJ()


    print(
        "\nBienvenido al sistema de gestión de Software FJ."
    )


    # El ciclo permite mantener la aplicación abierta
    # hasta que el usuario seleccione la opción de salir.
    while True:

        mostrar_menu()


        opcion = input(
            "\nSeleccione una opción: "
        ).strip()


        try:

            if opcion == "1":

                opcion_registrar_cliente(
                    sistema
                )


            elif opcion == "2":

                opcion_registrar_sala(
                    sistema
                )


            elif opcion == "3":

                opcion_registrar_equipo(
                    sistema
                )


            elif opcion == "4":

                opcion_registrar_asesoria(
                    sistema
                )


            elif opcion == "5":

                opcion_crear_reserva(
                    sistema
                )


            elif opcion == "6":

                opcion_confirmar_reserva(
                    sistema
                )


            elif opcion == "7":

                opcion_procesar_reserva(
                    sistema
                )


            elif opcion == "8":

                opcion_cancelar_reserva(
                    sistema
                )


            elif opcion == "9":

                sistema.mostrar_clientes()


            elif opcion == "10":

                sistema.mostrar_servicios()


            elif opcion == "11":

                sistema.mostrar_reservas()


            elif opcion == "0":

                registrar_evento(
                    "El usuario cerró el sistema."
                )

                print(
                    "\nPrograma finalizado."
                )

                break


            else:

                # Guardamos también las opciones incorrectas
                # para tener un registro más completo del uso del sistema.
                registrar_error(
                    f"Opción de menú no válida: {opcion}"
                )

                print(
                    "\nOpción no válida. Intente nuevamente."
                )


        # Aquí reunimos las excepciones personalizadas
        # que pueden ocurrir durante las operaciones.
        except (
            DatoInvalidoError,
            ClienteInvalidoError,
            ServicioInvalidoError,
            ServicioNoDisponibleError,
            DuracionInvalidaError,
            ReservaInvalidaError,
            OperacionNoPermitidaError
        ) as error:

            registrar_error(
                f"Error controlado en el programa: {error}"
            )

            print(
                f"\nERROR: {error}"
            )


        # También controlamos errores de conversión
        # que puedan aparecer por datos incorrectos.
        except ValueError as error:

            registrar_error(
                f"Valor incorrecto ingresado: {error}"
            )

            print(
                "\nERROR: Se ingresó un valor numérico incorrecto."
            )


        # Este bloque evita que un error inesperado
        # cierre completamente el programa.
        except Exception as error:

            registrar_error(
                f"Error inesperado: {error}"
            )

            print(
                f"\nOcurrió un error inesperado: {error}"
            )


# ==========================================================
# INICIO DEL PROGRAMA
# ==========================================================

# Esta condición permite ejecutar el programa solamente
# cuando Main.py se abre directamente.
#
# También nos permitirá importar SistemaSoftwareFJ
# posteriormente desde Pruebas.py sin iniciar el menú.
if __name__ == "__main__":

    ejecutar_programa()