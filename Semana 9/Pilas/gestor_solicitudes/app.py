"""
app.py
======
Guía de Laboratorio: Gestión de Solicitudes (Pilas y Colas)
Desafío Flask: Aplicación web interactiva con todas las rutas RESTful.
Restricción técnica: Implementación 100% funcional y modular SIN clases.
"""

from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Creación de la aplicación Flask
app = Flask(__name__)

# ==============================================================================
# VARIABLES DE ESTADO DEL MÓDULO (Estructuras de Datos y Configuración)
# ==============================================================================
# Cola de solicitudes pendientes (FIFO)
cola_solicitudes = []

# Pila de historial de solicitudes atendidas (LIFO)
pila_historial = []

# Identificador secuencial incremental
contador_id = 1

# Límite de capacidad máxima para control de desbordamiento
CAPACIDAD_MAXIMA = 10


# ==============================================================================
# FUNCIONES LÓGICAS PURAS DEL GESTOR (Sin clases)
# ==============================================================================
def registrar_solicitud(cliente: str, descripcion: str, urgente: bool = False) -> tuple[bool, str, dict | None]:
    """
    Registra una solicitud en la cola respetando capacidad máxima y prioridad.
    - Si es urgente: Inserción al frente de la cola (índice 0).
    - Si es ordinaria: Inserción al final de la cola (append).
    """
    global contador_id, cola_solicitudes

    if not isinstance(cliente, str) or not isinstance(descripcion, str):
        return False, "Los datos enviados deben ser cadenas de texto.", None

    cli = cliente.strip()
    desc = descripcion.strip()

    if not cli or not desc:
        return False, "El nombre del cliente y la descripción no pueden estar vacíos.", None

    if len(cola_solicitudes) >= CAPACIDAD_MAXIMA:
        return False, f"Capacidad máxima de la cola ({CAPACIDAD_MAXIMA}) alcanzada.", None

    hora_registro = datetime.now().strftime("%H:%M:%S")

    solicitud = {
        "id": contador_id,
        "cliente": cli,
        "descripcion": desc,
        "urgente": bool(urgente),
        "hora_registro": hora_registro
    }
    contador_id += 1

    if urgente:
        cola_solicitudes.insert(0, solicitud)
        mensaje = f"Solicitud #{solicitud['id']} registrada como URGENTE en el frente de la cola."
    else:
        cola_solicitudes.append(solicitud)
        mensaje = f"Solicitud #{solicitud['id']} encolada correctamente (FIFO)."

    return True, mensaje, solicitud


def atender_solicitud() -> tuple[bool, str, dict | None]:
    """
    Extrae la solicitud al frente de la cola (FIFO - pop(0)) y la apila en el historial.
    """
    global cola_solicitudes, pila_historial

    if not cola_solicitudes:
        return False, "No hay solicitudes pendientes en la cola para atender.", None

    solicitud_atendida = cola_solicitudes.pop(0)
    solicitud_atendida["hora_atencion"] = datetime.now().strftime("%H:%M:%S")
    pila_historial.append(solicitud_atendida)

    mensaje = f"Solicitud #{solicitud_atendida['id']} de '{solicitud_atendida['cliente']}' atendida con éxito."
    return True, mensaje, solicitud_atendida


def deshacer_atencion() -> tuple[bool, str, dict | None]:
    """
    Desapila la última solicitud del historial (LIFO - pop()) y la reubica al inicio de la cola.
    """
    global cola_solicitudes, pila_historial

    if not pila_historial:
        return False, "No hay solicitudes en el historial para deshacer.", None

    solicitud_restaurada = pila_historial.pop()
    cola_solicitudes.insert(0, solicitud_restaurada)

    mensaje = f"Atención deshecha. Solicitud #{solicitud_restaurada['id']} reubicada al frente de la cola."
    return True, mensaje, solicitud_restaurada


def cancelar_solicitud(id_solicitud: int) -> tuple[bool, str, dict | None]:
    """
    Busca y elimina una solicitud pendiente por su ID dentro de la cola.
    """
    global cola_solicitudes

    indice_encontrado = -1
    for i, sol in enumerate(cola_solicitudes):
        if sol["id"] == id_solicitud:
            indice_encontrado = i
            break

    if indice_encontrado == -1:
        return False, f"No se encontró ninguna solicitud con ID #{id_solicitud} en la cola.", None

    cancelada = cola_solicitudes.pop(indice_encontrado)
    mensaje = f"Solicitud #{id_solicitud} de '{cancelada['cliente']}' ha sido cancelada."
    return True, mensaje, cancelada


def reiniciar_sistema() -> tuple[bool, str]:
    """
    Limpia la cola y la pila, restableciendo el contador a 1.
    """
    global cola_solicitudes, pila_historial, contador_id
    cola_solicitudes.clear()
    pila_historial.clear()
    contador_id = 1
    return True, "Sistema reiniciado completamente. Cola e historial vaciados."


def obtener_estado_completo() -> dict:
    """
    Genera un diccionario con el estado actual consolidado para el frontend.
    """
    proxima = cola_solicitudes[0] if cola_solicitudes else None
    ultima_atendida = pila_historial[-1] if pila_historial else None

    # En el historial retornamos una copia invertida para que el frontend
    # muestre la cima (último atendido) en la parte superior
    historial_visual = list(reversed(pila_historial))

    return {
        "cola": cola_solicitudes,
        "historial": historial_visual,
        "total_cola": len(cola_solicitudes),
        "total_historial": len(pila_historial),
        "capacidad_maxima": CAPACIDAD_MAXIMA,
        "proxima_solicitud": proxima,
        "ultima_atendida": ultima_atendida
    }


# ==============================================================================
# RUTAS WEB Y ENDPOINTS DE LA API (RESTful)
# ==============================================================================
@app.route("/")
def index():
    """Renderiza la interfaz gráfica principal con Bootstrap 5.3."""
    return render_template("index.html")


@app.route("/api/estado", methods=["GET"])
def api_estado():
    """Devuelve el estado completo actual de la cola y de la pila en formato JSON."""
    return jsonify(obtener_estado_completo())


@app.route("/api/solicitudes", methods=["POST"])
def api_registrar_solicitud():
    """
    Endpoint para registrar una nueva solicitud.
    Espera JSON: {"cliente": str, "descripcion": str, "urgente": bool}
    """
    datos = request.get_json(silent=True) or {}
    cliente = datos.get("cliente", "")
    descripcion = datos.get("descripcion", "")
    urgente = bool(datos.get("urgente", False))

    exito, mensaje, solicitud = registrar_solicitud(cliente, descripcion, urgente)

    if not exito:
        return jsonify({"success": False, "message": mensaje}), 400

    return jsonify({
        "success": True,
        "message": mensaje,
        "solicitud": solicitud,
        "estado": obtener_estado_completo()
    }), 201


@app.route("/api/atender", methods=["POST"])
def api_atender_solicitud():
    """
    Endpoint para atender la siguiente solicitud de la cola (FIFO).
    """
    exito, mensaje, atendida = atender_solicitud()

    if not exito:
        return jsonify({"success": False, "message": mensaje}), 400

    return jsonify({
        "success": True,
        "message": mensaje,
        "atendida": atendida,
        "estado": obtener_estado_completo()
    }), 200


@app.route("/api/deshacer", methods=["POST"])
def api_deshacer_atencion():
    """
    Endpoint para deshacer la última atención realizada (LIFO).
    """
    exito, mensaje, restaurada = deshacer_atencion()

    if not exito:
        return jsonify({"success": False, "message": mensaje}), 400

    return jsonify({
        "success": True,
        "message": mensaje,
        "restaurada": restaurada,
        "estado": obtener_estado_completo()
    }), 200


@app.route("/api/solicitudes/<int:solicitud_id>", methods=["DELETE"])
def api_cancelar_solicitud(solicitud_id: int):
    """
    Endpoint para cancelar una solicitud pendiente en la cola.
    """
    exito, mensaje, cancelada = cancelar_solicitud(solicitud_id)

    if not exito:
        return jsonify({"success": False, "message": mensaje}), 404

    return jsonify({
        "success": True,
        "message": mensaje,
        "cancelada": cancelada,
        "estado": obtener_estado_completo()
    }), 200


@app.route("/api/reiniciar", methods=["POST"])
def api_reiniciar_sistema():
    """
    Endpoint para limpiar todo el sistema y restablecer contadores.
    """
    exito, mensaje = reiniciar_sistema()
    return jsonify({
        "success": exito,
        "message": mensaje,
        "estado": obtener_estado_completo()
    }), 200


# ==============================================================================
# EJECUCIÓN DEL SERVIDOR DE DESARROLLO
# ==============================================================================
if __name__ == "__main__":
    # Servidor local en http://127.0.0.1:5000
    app.run(debug=True, port=5000)
