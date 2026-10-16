"""
03_consola_interactiva.py
=========================
Guía de Laboratorio: Gestión de Solicitudes (Pilas y Colas)
Paso 5: Menú de Consola Interactivo Completo.
Restricción técnica: Implementación 100% funcional y modular SIN clases.
"""

import sys

# ==============================================================================
# VARIABLES DE ESTADO DEL SISTEMA (Módulo independiente)
# ==============================================================================
cola_solicitudes = []
pila_historial = []
contador_id = 1


# ==============================================================================
# FUNCIONES DE GESTIÓN DE SOLICITUDES
# ==============================================================================
def registrar_solicitud(cliente: str, descripcion: str) -> dict | None:
    """
    Registra una nueva solicitud al final de la cola (FIFO - append).
    Retorna el diccionario de la solicitud creada o None si hay error.
    """
    global contador_id, cola_solicitudes

    if not isinstance(cliente, str) or not isinstance(descripcion, str):
        return None

    cli = cliente.strip()
    desc = descripcion.strip()

    if not cli or not desc:
        return None

    solicitud = {
        "id": contador_id,
        "cliente": cli,
        "descripcion": desc
    }
    contador_id += 1
    cola_solicitudes.append(solicitud)
    return solicitud


def atender_solicitud() -> dict | None:
    """
    Extrae la solicitud más antigua (frente de la cola - pop(0) - FIFO)
    y la apila en el historial de atendidos (append - LIFO).
    Retorna la solicitud atendida o None si la cola está vacía.
    """
    global cola_solicitudes, pila_historial

    if not cola_solicitudes:
        return None

    atendida = cola_solicitudes.pop(0)
    pila_historial.append(atendida)
    return atendida


def deshacer_atencion() -> dict | None:
    """
    Desapila la última solicitud atendida (cima del historial - pop - LIFO)
    y la reinserta al inicio de la cola de espera (frente - insert(0) - FIFO).
    Retorna la solicitud restaurada o None si el historial está vacío.
    """
    global cola_solicitudes, pila_historial

    if not pila_historial:
        return None

    restaurada = pila_historial.pop()
    cola_solicitudes.insert(0, restaurada)
    return restaurada


def consultar_proxima_solicitud() -> dict | None:
    """
    Operación Peek: Devuelve la siguiente solicitud a ser atendida sin extraerla.
    Retorna la solicitud o None si la cola está vacía.
    """
    if not cola_solicitudes:
        return None
    return cola_solicitudes[0]


def consultar_ultima_atendida() -> dict | None:
    """
    Operación Peek sobre la pila: Devuelve la última solicitud atendida sin extraerla.
    Retorna la solicitud o None si el historial está vacío.
    """
    if not pila_historial:
        return None
    return pila_historial[-1]


# ==============================================================================
# FUNCIONES DE SALIDA EN PANTALLA Y MENÚ
# ==============================================================================
def mostrar_menu():
    """Imprime las opciones disponibles en la consola."""
    print("\n" + "=" * 60)
    print("      SISTEMA DE GESTION DE SOLICITUDES (PILAS Y COLAS)")
    print("=" * 60)
    print("  [1] Registrar nueva solicitud (Encolar - FIFO)")
    print("  [2] Atender siguiente solicitud (Desencolar y Apilar)")
    print("  [3] Deshacer ultima atencion (Desapilar y Reencolar)")
    print("  [4] Ver cola de solicitudes pendientes (FIFO)")
    print("  [5] Ver historial de solicitudes atendidas (LIFO)")
    print("  [6] Consultar proxima solicitud a atender (Peek)")
    print("  [7] Resumen general del sistema")
    print("  [0] Salir")
    print("=" * 60)


def opcion_registrar():
    """Maneja la entrada del usuario para registrar una nueva solicitud."""
    print("\n--- REGISTRAR NUEVA SOLICITUD ---")
    cliente = input(" Ingrese el nombre del cliente: ")
    descripcion = input(" Ingrese la descripcion del problema/solicitud: ")

    resultado = registrar_solicitud(cliente, descripcion)
    if resultado is not None:
        print(f" [OK] Solicitud #{resultado['id']} registrada con exito en la cola.")
    else:
        print(" [ERROR] Datos invalidos. El cliente y la descripcion no pueden estar vacios.")


def opcion_atender():
    """Maneja la acción de atender la siguiente solicitud."""
    print("\n--- ATENDER SIGUIENTE SOLICITUD (FIFO) ---")
    resultado = atender_solicitud()
    if resultado is not None:
        print(f" [OK] Se atendio la Solicitud #{resultado['id']}:")
        print(f"      Cliente    : {resultado['cliente']}")
        print(f"      Descripcion: {resultado['descripcion']}")
        print("      -> Movida con exito a la pila de historial.")
    else:
        print(" [AVISO] No hay solicitudes pendientes en la cola.")


def opcion_deshacer():
    """Maneja la acción de deshacer la última solicitud atendida."""
    print("\n--- DESHACER ULTIMA ATENCION (LIFO) ---")
    resultado = deshacer_atencion()
    if resultado is not None:
        print(f" [OK] Se revirtio la atencion de la Solicitud #{resultado['id']}:")
        print(f"      Cliente    : {resultado['cliente']}")
        print(f"      Descripcion: {resultado['descripcion']}")
        print("      -> Reinsertada al frente de la cola de espera.")
    else:
        print(" [AVISO] No hay solicitudes en el historial para deshacer.")


def opcion_ver_cola():
    """Muestra todas las solicitudes pendientes en orden de atención."""
    print("\n--- COLA DE SOLICITUDES PENDIENTES (FIFO) ---")
    if not cola_solicitudes:
        print(" (La cola esta vacia. No hay solicitudes pendientes.)")
        return

    print(f" Total en espera: {len(cola_solicitudes)}")
    print(f" {'No.':<4} | {'ID':<6} | {'Cliente':<22} | {'Descripcion'}")
    print("-" * 60)
    for i, sol in enumerate(cola_solicitudes, start=1):
        etiqueta = " [PROXIMO]" if i == 1 else ""
        print(f" {i:<4} | #{sol['id']:<5} | {sol['cliente']:<22} | {sol['descripcion']}{etiqueta}")


def opcion_ver_historial():
    """Muestra el historial de solicitudes atendidas en orden de pila (LIFO)."""
    print("\n--- HISTORIAL DE SOLICITUDES ATENDIDAS (LIFO) ---")
    if not pila_historial:
        print(" (El historial esta vacio. No se han atendido solicitudes.)")
        return

    print(f" Total atendidas: {len(pila_historial)}")
    print(f" {'No.':<4} | {'ID':<6} | {'Cliente':<22} | {'Descripcion'}")
    print("-" * 60)
    # Mostramos desde la cima (último atendido) hacia la base
    for idx, sol in enumerate(reversed(pila_historial), start=1):
        etiqueta = " [CIMA / ULTIMO ATENDIDO]" if idx == 1 else ""
        print(f" {idx:<4} | #{sol['id']:<5} | {sol['cliente']:<22} | {sol['descripcion']}{etiqueta}")


def opcion_consultar_proxima():
    """Consulta la próxima solicitud en cola sin extraerla."""
    print("\n--- PROXIMA SOLICITUD EN TURNO (PEEK) ---")
    proxima = consultar_proxima_solicitud()
    if proxima is not None:
        print(f" [INFO] La proxima solicitud a ser atendida es:")
        print(f"        ID         : #{proxima['id']}")
        print(f"        Cliente    : {proxima['cliente']}")
        print(f"        Descripcion: {proxima['descripcion']}")
    else:
        print(" [AVISO] La cola esta vacia. No hay solicitudes en turno.")


def opcion_resumen_sistema():
    """Presenta un cuadro de mando con las métricas actuales del sistema."""
    print("\n--- RESUMEN GENERAL DEL SISTEMA ---")
    print(f" Solicitudes pendientes en cola : {len(cola_solicitudes)}")
    print(f" Solicitudes atendidas (pila)   : {len(pila_historial)}")
    
    proxima = consultar_proxima_solicitud()
    ultima = consultar_ultima_atendida()

    proxima_str = f"#{proxima['id']} ({proxima['cliente']})" if proxima else "Ninguna"
    ultima_str = f"#{ultima['id']} ({ultima['cliente']})" if ultima else "Ninguna"

    print(f" Siguiente en cola de atencion  : {proxima_str}")
    print(f" Ultima atendida (tope pila)    : {ultima_str}")


def ejecutar_consola():
    """Bucle principal de la consola interactiva."""
    while True:
        try:
            mostrar_menu()
            opcion = input(" Seleccione una opcion [0-7]: ").strip()

            if opcion == "1":
                opcion_registrar()
            elif opcion == "2":
                opcion_atender()
            elif opcion == "3":
                opcion_deshacer()
            elif opcion == "4":
                opcion_ver_cola()
            elif opcion == "5":
                opcion_ver_historial()
            elif opcion == "6":
                opcion_consultar_proxima()
            elif opcion == "7":
                opcion_resumen_sistema()
            elif opcion == "0":
                print("\n Gracias por utilizar el Gestor de Solicitudes. Saliendo...")
                break
            else:
                print(" [ERROR] Opcion invalida. Ingrese un numero entre 0 y 7.")

        except (KeyboardInterrupt, EOFError):
            print("\n\n [INFO] Operacion cancelada por el usuario. Saliendo...")
            break
        except Exception as e:
            print(f" [ERROR INESPERADO] {e}")


if __name__ == "__main__":
    ejecutar_consola()
