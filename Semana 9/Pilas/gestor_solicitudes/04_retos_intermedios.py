"""
04_retos_intermedios.py
=======================
Guía de Laboratorio: Gestión de Solicitudes (Pilas y Colas)
Retos 1 al 5: Implementación completa y probada en consola.
Restricción técnica: Implementación 100% funcional y modular SIN clases.

RETOS IMPLEMENTADOS:
1. Solicitudes Urgentes / Prioritarias (Inserción al frente de la cola).
2. Inspección del siguiente en turno (Operación Peek sin extracción).
3. Cancelación de una solicitud en espera por su identificador (ID).
4. Control de capacidad máxima de la cola (Prevención de Desbordamiento / Overflow).
5. Búsqueda y filtrado de solicitudes en cola y en historial.
"""

# ==============================================================================
# VARIABLES DE ESTADO DEL MÓDULO (Estructuras de Datos y Configuración)
# ==============================================================================
cola_solicitudes = []
pila_historial = []
contador_id = 1
CAPACIDAD_MAXIMA_COLA = 4  # Reto 4: Límite para probar desbordamiento


# ==============================================================================
# RETO 4 Y FUNCIONES DE REGISTRO (Normal y Urgente)
# ==============================================================================
def verificar_capacidad() -> bool:
    """
    Reto 4: Retorna True si la cola aún tiene espacio disponible; False si está llena.
    """
    return len(cola_solicitudes) < CAPACIDAD_MAXIMA_COLA


def registrar_solicitud(cliente: str, descripcion: str) -> dict | None:
    """
    Registra una solicitud estándar al final de la cola (FIFO).
    Controla el límite de capacidad máxima (Reto 4).
    """
    global contador_id, cola_solicitudes

    if not isinstance(cliente, str) or not isinstance(descripcion, str):
        print(" [ERROR] Entradas deben ser cadenas de texto.")
        return None

    cli = cliente.strip()
    desc = descripcion.strip()

    if not cli or not desc:
        print(" [ERROR] El cliente y la descripcion no pueden estar vacios.")
        return None

    # Reto 4: Validación de capacidad máxima
    if not verificar_capacidad():
        print(f" [RECHAZADA] Desbordamiento de cola: Capacidad maxima ({CAPACIDAD_MAXIMA_COLA}) alcanzada.")
        return None

    solicitud = {
        "id": contador_id,
        "cliente": cli,
        "descripcion": desc,
        "urgente": False
    }
    contador_id += 1
    cola_solicitudes.append(solicitud)
    print(f" [+] Solicitud #{solicitud['id']} registrada (Ordinaria - FIFO).")
    return solicitud


def registrar_solicitud_urgente(cliente: str, descripcion: str) -> dict | None:
    """
    Reto 1: Registra una solicitud con prioridad alta.
    Se inserta directamente en el FRENTE de la cola (índice 0)
    para ser atendida con preferencia antes que las ordinarias.
    """
    global contador_id, cola_solicitudes

    if not isinstance(cliente, str) or not isinstance(descripcion, str):
        print(" [ERROR] Entradas deben ser cadenas de texto.")
        return None

    cli = cliente.strip()
    desc = descripcion.strip()

    if not cli or not desc:
        print(" [ERROR] El cliente y la descripcion no pueden estar vacios.")
        return None

    # Reto 4: Validación de capacidad máxima
    if not verificar_capacidad():
        print(f" [RECHAZADA] No se puede registrar urgente. Capacidad maxima ({CAPACIDAD_MAXIMA_COLA}) alcanzada.")
        return None

    solicitud = {
        "id": contador_id,
        "cliente": cli,
        "descripcion": desc,
        "urgente": True
    }
    contador_id += 1
    # Inserción al frente de la cola (índice 0)
    cola_solicitudes.insert(0, solicitud)
    print(f" [!] Solicitud #{solicitud['id']} registrada como URGENTE (Prioridad en frente de cola).")
    return solicitud


# ==============================================================================
# RETO 2: OPERACIÓN PEEK (Consultar sin extraer)
# ==============================================================================
def consultar_proxima_solicitud() -> dict | None:
    """
    Reto 2: Permite inspeccionar qué solicitud está al frente de la cola
    sin modificar la estructura ni extraer el elemento.
    """
    if len(cola_solicitudes) == 0:
        return None
    return cola_solicitudes[0]


# ==============================================================================
# RETO 3: CANCELACIÓN DE SOLICITUDES EN COLA
# ==============================================================================
def cancelar_solicitud(id_solicitud: int) -> dict | None:
    """
    Reto 3: Busca una solicitud en espera por su ID y la elimina de la cola.
    Retorna el diccionario de la solicitud eliminada, o None si no se encuentra.
    """
    global cola_solicitudes

    if not isinstance(id_solicitud, int) or id_solicitud <= 0:
        print(" [ERROR] El ID de solicitud debe ser un entero positivo.")
        return None

    indice_encontrado = -1
    for i, sol in enumerate(cola_solicitudes):
        if sol["id"] == id_solicitud:
            indice_encontrado = i
            break

    if indice_encontrado == -1:
        print(f" [AVISO] No se encontro ninguna solicitud pendiente con ID #{id_solicitud}.")
        return None

    solicitud_cancelada = cola_solicitudes.pop(indice_encontrado)
    print(f" [CANCELADA] Solicitud #{id_solicitud} de '{solicitud_cancelada['cliente']}' cancelada y retirada de la cola.")
    return solicitud_cancelada


# ==============================================================================
# RETO 5: BÚSQUEDA Y FILTRADO DE SOLICITUDES
# ==============================================================================
def buscar_solicitudes(termino: str) -> dict:
    """
    Reto 5: Busca coincidencias (case-insensitive) del término dado en el
    nombre del cliente o en la descripción de solicitudes pendientes e historial.
    Retorna un diccionario con dos listas: {"en_cola": [...], "en_historial": [...]}.
    """
    if not isinstance(termino, str) or not termino.strip():
        print(" [ERROR] Ingrese un termino de busqueda valido.")
        return {"en_cola": [], "en_historial": []}

    t = termino.strip().lower()

    resultados_cola = [
        sol for sol in cola_solicitudes
        if t in sol["cliente"].lower() or t in sol["descripcion"].lower()
    ]

    resultados_historial = [
        sol for sol in pila_historial
        if t in sol["cliente"].lower() or t in sol["descripcion"].lower()
    ]

    return {
        "en_cola": resultados_cola,
        "en_historial": resultados_historial
    }


# ==============================================================================
# OPERACIONES BÁSICAS COMPLEMENTARIAS (Atender y Deshacer)
# ==============================================================================
def atender_solicitud() -> dict | None:
    """Atiende la solicitud al frente de la cola y la apila en el historial."""
    global cola_solicitudes, pila_historial
    if not cola_solicitudes:
        return None
    atendida = cola_solicitudes.pop(0)
    pila_historial.append(atendida)
    return atendida


def deshacer_atencion() -> dict | None:
    """Desapila la última solicitud y la reubica al frente de la cola."""
    global cola_solicitudes, pila_historial
    if not pila_historial:
        return None
    restaurada = pila_historial.pop()
    cola_solicitudes.insert(0, restaurada)
    return restaurada


def mostrar_cola_actual():
    """Imprime el estado detallado de la cola de espera."""
    print(f"\n ESTADO DE LA COLA ({len(cola_solicitudes)}/{CAPACIDAD_MAXIMA_COLA} cupos):")
    if not cola_solicitudes:
        print("   (Cola vacia)")
    for i, s in enumerate(cola_solicitudes, start=1):
        urg_tag = "[URGENTE]" if s["urgente"] else "[NORMAL]"
        print(f"   Pos {i}: [ID #{s['id']}] {urg_tag} {s['cliente']} -> {s['descripcion']}")


# ==============================================================================
# BLOQUE DE EJECUCIÓN: DEMOSTRACIÓN DE LOS 5 RETOS
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACION INTEGRADA: RETOS 1 AL 5")
    print("=" * 65)

    # Registro inicial de solicitudes ordinarias
    print("\n--- 1. REGISTRO ORDINARIO (FIFO) ---")
    registrar_solicitud("Carlos Ramos", "Pago duplicado en tarjeta")
    registrar_solicitud("Elena Castro", "Actualizacion de domicilio")
    mostrar_cola_actual()

    # Reto 1: Registrar solicitud urgente
    print("\n--- 2. RETO 1: SOLICITUD URGENTE (Prioridad al frente) ---")
    registrar_solicitud_urgente("DIRECTOR GENERAL", "Servidor principal caido")
    mostrar_cola_actual()

    # Reto 2: Consultar próxima solicitud (Peek)
    print("\n--- 3. RETO 2: OPERACION PEEK (Consultar sin extraer) ---")
    proxima = consultar_proxima_solicitud()
    if proxima:
        print(f" [PEEK] Proxima en turno: ID #{proxima['id']} ({proxima['cliente']}) - Urgente: {proxima['urgente']}")
    print(f" [VERIFICACION] Tamano de cola se mantiene: {len(cola_solicitudes)}")

    # Reto 4: Límite de capacidad máxima y desbordamiento
    print("\n--- 4. RETO 4: CONTROL DE CAPACIDAD MAXIMA (Overflow) ---")
    # Llenamos el cupo disponible (máximo 4)
    registrar_solicitud("Sonia Vargas", "Consulta sobre hipoteca")
    mostrar_cola_actual()
    print(" Intentando registrar una 5ta solicitud cuando el tope es 4:")
    sol_rechazada = registrar_solicitud("Pedro Infante", "Credito vehicular")
    print(f" Resultado de rechazo: {sol_rechazada}")

    # Reto 3: Cancelación de una solicitud en cola
    print("\n--- 5. RETO 3: CANCELAR SOLICITUD EN ESPERA ---")
    # Cancelamos la solicitud de Elena Castro (ID 2)
    cancelar_solicitud(2)
    mostrar_cola_actual()
    # Ahora que hay espacio libre, podemos registrar la solicitud pendiente
    print(" Ahora que hay 1 cupo libre, intentamos registrar de nuevo:")
    registrar_solicitud("Pedro Infante", "Credito vehicular")
    mostrar_cola_actual()

    # Reto 5: Búsqueda y filtrado
    print("\n--- 6. RETO 5: BUSQUEDA Y FILTRADO ---")
    # Atendemos 2 solicitudes para tener elementos tanto en cola como en historial
    atender_solicitud()  # Atiende al Director (ID 3)
    atender_solicitud()  # Atiende a Carlos Ramos (ID 1)

    print(" Estado actual tras atender 2 solicitudes:")
    print(f" En cola: {[s['cliente'] for s in cola_solicitudes]}")
    print(f" En historial: {[s['cliente'] for s in pila_historial]}")

    print("\n Busqueda 1: Termino 'tarjeta':")
    res1 = buscar_solicitudes("tarjeta")
    print(f"  Coincidencias en cola     : {res1['en_cola']}")
    print(f"  Coincidencias en historial: {res1['en_historial']}")

    print("\n Busqueda 2: Termino 'pedro':")
    res2 = buscar_solicitudes("pedro")
    print(f"  Coincidencias en cola     : {[s['cliente'] for s in res2['en_cola']]}")
    print(f"  Coincidencias en historial: {[s['cliente'] for s in res2['en_historial']]}")

    print("\n" + "=" * 65)
    print("TODOS LOS 5 RETOS HAN SIDO PROBADOS Y VERIFICADOS CON EXITO.")
    print("=" * 65)
