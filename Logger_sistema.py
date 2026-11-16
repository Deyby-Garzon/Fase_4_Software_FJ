# Registro de errores y eventos del sistema

# logging permite registrar automaticamente
# los eventos y errores del programa.
import logging

# Path nos ayuda a ubicar el archivo eventos.log
# dentro de la misma carpeta del proyecto.
from pathlib import Path


# ==========================================================
# CONFIGURACION DEL ARCHIVO DE LOGS
# ==========================================================

# Buscamos la carpeta donde esta este archivo
# y definimos alli eventos.log.
ruta_log = (
    Path(__file__).resolve().parent
    / "eventos.log"
)


# Creamos el logger que utilizara todo el proyecto.
logger = logging.getLogger(
    "SoftwareFJ"
)

logger.setLevel(
    logging.INFO
)


# Evitamos crear varios manejadores si el archivo
# se importa mas de una vez durante la ejecución.
if not logger.handlers:

    # Este manejador se encargara de escribir
    # dentro del archivo eventos.log.
    manejador_archivo = logging.FileHandler(
        ruta_log,
        encoding="utf-8"
    )

    # Definimos como aparecera cada registro.
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    manejador_archivo.setFormatter(
        formato
    )

    logger.addHandler(
        manejador_archivo
    )


# Evitamos que los mensajes se repitan
# en otros loggers de Python.
logger.propagate = False


# ==========================================================
# REGISTRAR EVENTOS
# ==========================================================

def registrar_evento(mensaje):
    # Guarda eventos normales del programa,
    # por ejemplo la creacion correcta de un cliente.
    logger.info(
        mensaje
    )


# ==========================================================
# REGISTRAR ERRORES
# ==========================================================

def registrar_error(mensaje):
    # Guarda los errores encontrados durante
    # el funcionamiento del sistema.
    logger.error(
        mensaje
    )