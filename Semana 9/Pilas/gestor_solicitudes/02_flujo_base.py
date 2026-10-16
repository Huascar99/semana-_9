"""
02_flujo_base.py
================
Guía de Laboratorio: Gestión de Solicitudes (Pilas y Colas)
Pasos 1 al 4: Estructuras, Registro, Atención (FIFO) y Deshacer (LIFO).
Restricción técnica: Implementación 100% funcional y modular SIN clases.
"""

# ==============================================================================
# PASO 1: VARIABLES DE ESTADO DEL MÓDULO (Estructuras de Datos)
# ==============================================================================
# Cola de solicitudes pendientes (FIFO): las solicitudes entran por el final y se atienden por el frente.
cola_solicitudes = []

# Pila de solicitudes atendidas (LIFO): almacena el historial. La última en ser atendida es la primera en poder deshacerse.
pila_historial = []

# Contador secuencial para asignar identificadores únicos a cada solicitud.
contador_id = 1


# ==============================================================================
# PASO 2: FUNCIÓN DE REGISTRO DE SOLICITUDES (Encolar)
# ==============================================================================
def registrar_solicitud(cliente: str, descripcion: str) -> dict | None:
    """
    Crea una nueva solicitud y la agrega al final de la cola (FIFO).
    
    Validaciones:
    - cliente y descripcion deben ser cadenas de texto no vacías tras aplicar .strip().
    - Retorna el diccionario de la solicitud creada o None si los datos son inválidos.
    """
    global contador_id, cola_solicitudes

    # Validación de tipos y contenido no vacío
    if not isinstance(cliente, str) or not isinstance(descripcion, str):
        print(" [ERROR] El nombre del cliente y la descripción deben ser cadenas de texto.")
        return None

    cliente_limpio = cliente.strip()
    descripcion_limpia = descripcion.strip()

    if not cliente_limpio or not descripcion_limpia:
        print(" [ERROR] No se permiten campos vacíos o con solo espacios en blanco.")
        return None

    # Construcción del registro de solicitud (diccionario)
    solicitud = {
        "id": contador_id,
        "cliente": cliente_limpio,
        "descripcion": descripcion_limpia
    }

    # Incrementamos el ID para la próxima solicitud
    contador_id += 1

    # Encolar: Inserción al final de la lista (FIFO)
    cola_solicitudes.append(solicitud)
    print(f" [+] Solicitud #{solicitud['id']} registrada con éxito para '{solicitud['cliente']}'.")
    return solicitud


# ==============================================================================
# PASO 3: FUNCIÓN DE ATENCIÓN DE SOLICITUDES (Desencolar y Apilar)
# ==============================================================================
def atender_solicitud() -> dict | None:
    """
    Extrae la solicitud más antigua de la cola (frente, índice 0 - FIFO)
    y la transfiere a la cima de la pila de historial (LIFO).

    Casos borde:
    - Si la cola está vacía, retorna None de forma segura sin generar excepciones.
    """
    global cola_solicitudes, pila_historial

    # Validación de cola vacía
    if len(cola_solicitudes) == 0:
        print(" [AVISO] No hay solicitudes pendientes por atender (Cola vacía).")
        return None

    # Desencolar del frente (FIFO): pop(0)
    solicitud_atendida = cola_solicitudes.pop(0)

    # Apilar en el historial (LIFO): append()
    pila_historial.append(solicitud_atendida)

    print(f" [ATENCION] Atendiendo Solicitud #{solicitud_atendida['id']} de '{solicitud_atendida['cliente']}' "
          f"({solicitud_atendida['descripcion']}). Transferida al historial.")
    return solicitud_atendida


# ==============================================================================
# PASO 4: FUNCIÓN DE DESHACER ATENCIÓN (Desapilar y Reencolar al Frente)
# ==============================================================================
def deshacer_atencion() -> dict | None:
    """
    Revierte la última atención realizada:
    - Extrae la última solicitud del tope de la pila de historial (LIFO - pop()).
    - La reinserta al inicio de la cola de solicitudes (frente, índice 0 - insert(0, item)).

    Casos borde:
    - Si la pila de historial está vacía, retorna None de forma segura.
    """
    global cola_solicitudes, pila_historial

    # Validación de historial vacío
    if len(pila_historial) == 0:
        print(" [AVISO] No hay acciones en el historial para deshacer (Pila vacía).")
        return None

    # Desapilar de la cima (LIFO): pop()
    solicitud_restaurada = pila_historial.pop()

    # Reinsertar al inicio de la cola para que sea la primera en volver a atenderse
    cola_solicitudes.insert(0, solicitud_restaurada)

    print(f" [DESHACER] Deshecha la atención de Solicitud #{solicitud_restaurada['id']} "
          f"de '{solicitud_restaurada['cliente']}'. Reubicada al frente de la cola.")
    return solicitud_restaurada


# ==============================================================================
# FUNCIONES DE CONSULTA Y ESTADO DEL SISTEMA
# ==============================================================================
def obtener_cola() -> list:
    """Retorna una copia superficial de la cola de solicitudes pendientes."""
    return list(cola_solicitudes)


def obtener_historial() -> list:
    """Retorna una copia superficial de la pila de historial de solicitudes atendidas."""
    return list(pila_historial)


def mostrar_estado_sistema():
    """Imprime un resumen visual del estado actual de la cola y de la pila."""
    print("\n" + "=" * 65)
    print("ESTADO ACTUAL DEL SISTEMA")
    print("=" * 65)
    
    print(f"COLA DE PENDIENTES (Total: {len(cola_solicitudes)}) [Frente -> Final]:")
    if not cola_solicitudes:
        print("   (Vacía)")
    else:
        for i, sol in enumerate(cola_solicitudes, start=1):
            marcador = " [SIGUIENTE EN TURNO]" if i == 1 else ""
            print(f"   {i}. [ID #{sol['id']}] {sol['cliente']} - {sol['descripcion']}{marcador}")

    print(f"\nPILA DE HISTORIAL (Total: {len(pila_historial)}) [Base -> Cima]:")
    if not pila_historial:
        print("   (Vacía)")
    else:
        for i, sol in enumerate(pila_historial, start=1):
            marcador = " [CIMA / ÚLTIMA ATENDIDA]" if i == len(pila_historial) else ""
            print(f"   {i}. [ID #{sol['id']}] {sol['cliente']} - {sol['descripcion']}{marcador}")
    print("=" * 65 + "\n")


# ==============================================================================
# BLOQUE DE EJECUCIÓN PRINCIPAL (Demostración de los Pasos 1 al 4)
# ==============================================================================
if __name__ == "__main__":
    print("*" * 65)
    print("   DEMOSTRACIÓN DE FLUJO BASE - PASOS 1 AL 4")
    print("*" * 65)

    # 1. Registrar solicitudes
    print("\n--- PASO 2: REGISTRO DE SOLICITUDES ---")
    registrar_solicitud("Mario Mendoza", "Falla en conexión a base de datos")
    registrar_solicitud("Lucía Fernández", "Revisión de permisos de usuario")
    registrar_solicitud("Roberto Silva", "Restablecimiento de contraseña")

    # Prueba de validaciones robustas
    print("\n--- PRUEBA DE ENTRADAS INVÁLIDAS ---")
    registrar_solicitud("   ", "Texto con cliente en blanco")
    registrar_solicitud("Cliente Válido", "")

    # Estado tras los registros
    mostrar_estado_sistema()

    # 2. Atender solicitudes (FIFO)
    print("--- PASO 3: ATENCIÓN DE SOLICITUDES (FIFO) ---")
    atender_solicitud()  # Atiende a Mario (ID 1)
    atender_solicitud()  # Atiende a Lucía (ID 2)
    mostrar_estado_sistema()

    # 3. Deshacer última atención (LIFO)
    print("--- PASO 4: DESHACER ÚLTIMA ATENCIÓN (LIFO) ---")
    deshacer_atencion()  # Restaura a Lucía (ID 2) al frente de la cola
    mostrar_estado_sistema()

    # 4. Atender hasta vaciar la cola
    print("--- ATENDER HASTA VACIAR LA COLA ---")
    atender_solicitud()  # Atiende nuevamente a Lucía (ID 2)
    atender_solicitud()  # Atiende a Roberto (ID 3)
    mostrar_estado_sistema()

    # 5. Intentar atender con cola vacía (Caso borde)
    print("--- CASO BORDE: ATENDER CON COLA VACÍA ---")
    resultado = atender_solicitud()
    print(f"Resultado retornado: {resultado}")

    # 6. Deshacer varias veces hasta vaciar historial
    print("\n--- VACIAR HISTORIAL MEDIANTE DESHACER ---")
    deshacer_atencion()  # Restaura Roberto
    deshacer_atencion()  # Restaura Lucía
    deshacer_atencion()  # Restaura Mario
    mostrar_estado_sistema()

    # 7. Intentar deshacer con historial vacío (Caso borde)
    print("--- CASO BORDE: DESHACER CON HISTORIAL VACÍO ---")
    resultado_deshacer = deshacer_atencion()
    print(f"Resultado retornado: {resultado_deshacer}")
