"""
06_mejora_deque.py
==================
Guía de Laboratorio: Gestión de Solicitudes (Pilas y Colas)
Tema: Optimización Algorítmica con collections.deque y Benchmark Comparativo.
Restricción técnica: Implementación 100% funcional y modular SIN clases.

¿POR QUÉ MEJORAR CON COLLECTIONS.DEQUE?
- En listas nativas de Python:
    * list.pop(0) e list.insert(0, ...) tienen un costo computacional de O(N).
      Al estar basadas en arreglos dinámicos contiguos en memoria (PyListObject),
      eliminar o insertar al inicio obliga a desplazar los N-1 elementos restantes en memoria.
- En collections.deque:
    * deque.popleft() y deque.appendleft(...) tienen costo constante O(1).
      Internamente está implementada en C como una lista doblemente enlazada de bloques
      de tamaño fijo (64 elementos), permitiendo inserciones y extracciones ultrarrápidas
      en ambos extremos sin reorganización masiva de memoria.
"""

import time
from collections import deque

# ==============================================================================
# GESTOR DE SOLICITUDES OPTIMIZADO CON DEQUE (Sin clases)
# ==============================================================================
cola_solicitudes_deque = deque()
pila_historial_lista = []
contador_id_deque = 1


def reiniciar_gestor_deque():
    """Limpia las estructuras del gestor optimizado."""
    global cola_solicitudes_deque, pila_historial_lista, contador_id_deque
    cola_solicitudes_deque.clear()
    pila_historial_lista.clear()
    contador_id_deque = 1


def registrar_solicitud_optimizada(cliente: str, descripcion: str, urgente: bool = False) -> dict | None:
    """
    Encola una solicitud en O(1):
    - Ordinaria: deque.append(solicitud) -> O(1) al final.
    - Urgente  : deque.appendleft(solicitud) -> O(1) al frente.
    """
    global contador_id_deque, cola_solicitudes_deque

    if not isinstance(cliente, str) or not isinstance(descripcion, str):
        return None

    cli = cliente.strip()
    desc = descripcion.strip()

    if not cli or not desc:
        return None

    solicitud = {
        "id": contador_id_deque,
        "cliente": cli,
        "descripcion": desc,
        "urgente": urgente
    }
    contador_id_deque += 1

    if urgente:
        # Inserción O(1) al frente de la cola con deque
        cola_solicitudes_deque.appendleft(solicitud)
    else:
        # Inserción O(1) al final de la cola
        cola_solicitudes_deque.append(solicitud)

    return solicitud


def atender_solicitud_optimizada() -> dict | None:
    """
    Desencola del frente en O(1) con popleft() y apila en el historial con append().
    """
    global cola_solicitudes_deque, pila_historial_lista

    if not cola_solicitudes_deque:
        return None

    # Extracción O(1) del frente sin desplazar elementos en memoria
    solicitud_atendida = cola_solicitudes_deque.popleft()
    pila_historial_lista.append(solicitud_atendida)
    return solicitud_atendida


def deshacer_atencion_optimizada() -> dict | None:
    """
    Desapila en O(1) y reinserta al frente de la cola en O(1) con appendleft().
    """
    global cola_solicitudes_deque, pila_historial_lista

    if not pila_historial_lista:
        return None

    solicitud_restaurada = pila_historial_lista.pop()
    # Reubicación O(1) al inicio con deque (en lista nativa era insert(0) O(N))
    cola_solicitudes_deque.appendleft(solicitud_restaurada)
    return solicitud_restaurada


# ==============================================================================
# BENCHMARK COMPARATIVO: LISTA NATIVA vs COLLECTIONS.DEQUE
# ==============================================================================
def medir_rendimiento_desencolado(tamano: int) -> tuple[float, float]:
    """
    Mide el tiempo requerido para vaciar una cola de tamaño N:
    1. Lista nativa usando list.pop(0) -> O(N^2) total acumulado.
    2. collections.deque usando deque.popleft() -> O(N) total acumulado.
    """
    # 1. Prueba con Lista Nativa (pop(0))
    lista_prueba = list(range(tamano))
    inicio_lista = time.perf_counter()
    while lista_prueba:
        lista_prueba.pop(0)
    tiempo_lista = time.perf_counter() - inicio_lista

    # 2. Prueba con Deque (popleft())
    deque_prueba = deque(range(tamano))
    inicio_deque = time.perf_counter()
    while deque_prueba:
        deque_prueba.popleft()
    tiempo_deque = time.perf_counter() - inicio_deque

    return tiempo_lista, tiempo_deque


def medir_rendimiento_insercion_frente(tamano: int) -> tuple[float, float]:
    """
    Mide el tiempo para insertar N elementos al frente:
    1. Lista nativa usando list.insert(0, x) -> O(N^2) acumulado.
    2. collections.deque usando deque.appendleft(x) -> O(N) acumulado.
    """
    # 1. Prueba con Lista Nativa (insert(0))
    lista_prueba = []
    inicio_lista = time.perf_counter()
    for i in range(tamano):
        lista_prueba.insert(0, i)
    tiempo_lista = time.perf_counter() - inicio_lista

    # 2. Prueba con Deque (appendleft)
    deque_prueba = deque()
    inicio_deque = time.perf_counter()
    for i in range(tamano):
        deque_prueba.appendleft(i)
    tiempo_deque = time.perf_counter() - inicio_deque

    return tiempo_lista, tiempo_deque


def ejecutar_benchmark_completo():
    """Ejecuta y muestra una tabla comparativa de rendimiento empírico."""
    print("=" * 75)
    print("BENCHMARK COMPARATIVO: LISTA NATIVA vs COLLECTIONS.DEQUE")
    print("=" * 75)
    print("Evaluando tiempo de extraccion al frente (pop(0) vs popleft()):")
    print(f" {'N Elementos':<14} | {'Lista (pop(0))':<18} | {'Deque (popleft())':<18} | {'Aceleracion'}")
    print("-" * 75)

    tamanos = [10000, 30000, 60000]

    for n in tamanos:
        t_lista, t_deque = medir_rendimiento_desencolado(n)
        speedup = t_lista / t_deque if t_deque > 0 else 0
        print(f" {n:<14} | {t_lista:14.6f} s | {t_deque:14.6f} s | {speedup:10.1f}x mas rapido")

    print("\n" + "=" * 75)
    print("Evaluando tiempo de insercion al frente (insert(0) vs appendleft()):")
    print(f" {'N Elementos':<14} | {'Lista (insert(0))':<18} | {'Deque (appendleft)':<18} | {'Aceleracion'}")
    print("-" * 75)

    for n in tamanos:
        t_lista_ins, t_deque_ins = medir_rendimiento_insercion_frente(n)
        speedup_ins = t_lista_ins / t_deque_ins if t_deque_ins > 0 else 0
        print(f" {n:<14} | {t_lista_ins:14.6f} s | {t_deque_ins:14.6f} s | {speedup_ins:10.1f}x mas rapido")
    print("=" * 75)


def demostrar_gestor_optimizado():
    """Demuestra el funcionamiento de la versión optimizada con deque."""
    print("\n" + "=" * 75)
    print("DEMOSTRACION DEL GESTOR OPTIMIZADO CON DEQUE")
    print("=" * 75)
    reiniciar_gestor_deque()

    # Registros
    registrar_solicitud_optimizada("Banco Central", "Transferencia interbancaria", urgente=False)
    registrar_solicitud_optimizada("Soporte IT", "Mantenimiento ordinario", urgente=False)
    # Urgente: entra directo al frente en O(1)
    registrar_solicitud_optimizada("Presidencia", "Fallo de ciberseguridad critico", urgente=True)

    print(f" Estado de la cola (deque): {[s['cliente'] for s in cola_solicitudes_deque]}")

    # Atender en O(1)
    atendida = atender_solicitud_optimizada()
    print(f" [ATENCION O(1)] Atendido de inmediato: {atendida['cliente']} (Urgente: {atendida['urgente']})")

    # Deshacer en O(1)
    restaurada = deshacer_atencion_optimizada()
    print(f" [DESHACER O(1)] Reinsertado al frente: {restaurada['cliente']}")
    print(f" Estado final de la cola: {[s['cliente'] for s in cola_solicitudes_deque]}")
    print("=" * 75)


if __name__ == "__main__":
    demostrar_gestor_optimizado()
    print("\nIniciando pruebas de carga y benchmark (puede tardar un par de segundos)...")
    ejecutar_benchmark_completo()
