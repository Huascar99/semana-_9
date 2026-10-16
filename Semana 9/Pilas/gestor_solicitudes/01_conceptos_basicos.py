"""
01_conceptos_basicos.py
========================
Guía de Laboratorio: Gestión de Solicitudes (Pilas y Colas)
Tema: Fundamentos de FIFO (First-In, First-Out) y LIFO (Last-In, First-Out)
Restricción técnica: Implementación 100% funcional y modular SIN clases.
"""

def demostrar_cola_fifo():
    """
    Demuestra el funcionamiento de una Cola (Queue) bajo el principio FIFO:
    - First-In, First-Out: El primer elemento en ingresar es el primero en salir.
    - Implementación nativa en Python con listas:
        * Encolar (enqueue): list.append(elemento) -> Inserta al final.
        * Desencolar (dequeue): list.pop(0) -> Extrae del inicio (índice 0).
    """
    print("=" * 65)
    print("DEMOSTRACIÓN 1: COLA (QUEUE) - PRINCIPIO FIFO (First-In, First-Out)")
    print("=" * 65)
    print("Imagina la fila de un banco: quien llega primero, es atendido primero.\n")

    # Estructura nativa: lista vacía que actuará como cola
    cola = []

    # 1. Encolar elementos (append agrega al extremo derecho / final de la lista)
    solicitudes = [
        {"id": 1, "cliente": "Ana Torres", "tramite": "Consulta de saldo"},
        {"id": 2, "cliente": "Carlos Ruiz", "tramite": "Apertura de cuenta"},
        {"id": 3, "cliente": "Diana Meza", "tramite": "Reclamo de tarjeta"}
    ]

    print("--- [PASO 1: ENCOLAR SOLICITUDES (append)] ---")
    for sol in solicitudes:
        cola.append(sol)
        print(f" -> Encolado: [ID {sol['id']}] {sol['cliente']} - {sol['tramite']}")
        print(f"    Estado de la cola: {[s['cliente'] for s in cola]}")

    print("\n--- [PASO 2: DESENCOLAR Y ATENDER (pop(0))] ---")
    print("Extraemos siempre del frente (índice 0):\n")

    while len(cola) > 0:
        # pop(0) extrae el primer elemento y desplaza los restantes
        atendido = cola.pop(0)
        print(f" <- Atendiendo ahora a: [ID {atendido['id']}] {atendido['cliente']}")
        print(f"    Cola restante: {[s['cliente'] for s in cola] if cola else '¡Cola vacía!'}")

    # Caso borde: Intentar desencolar cuando está vacía
    print("\n--- [PASO 3: CASO BORDE (Cola vacía)] ---")
    if len(cola) == 0:
        elemento = None
        print(" Intentando desencolar de cola vacía...")
        print(f" Resultado seguro: {elemento} (Sin excepciones ni caídas de sistema)\n")


def demostrar_pila_lifo():
    """
    Demuestra el funcionamiento de una Pila (Stack) bajo el principio LIFO:
    - Last-In, First-Out: El último elemento en ingresar es el primero en salir.
    - Implementación nativa en Python con listas:
        * Apilar (push): list.append(elemento) -> Inserta en el tope (cima).
        * Desapilar (pop): list.pop() -> Extrae del tope (último índice).
        * Tope (peek): list[-1] -> Inspecciona la cima sin extraer.
    """
    print("=" * 65)
    print("DEMOSTRACIÓN 2: PILA (STACK) - PRINCIPIO LIFO (Last-In, First-Out)")
    print("=" * 65)
    print("Imagina una pila de platos o la función Deshacer (Ctrl + Z):\n"
          "la última acción realizada es la primera en revertirse.\n")

    # Estructura nativa: lista vacía que actuará como pila
    pila = []

    acciones = [
        {"paso": 1, "accion": "Escribir párrafo 1"},
        {"paso": 2, "accion": "Aplicar negrita al título"},
        {"paso": 3, "accion": "Insertar imagen de logotipo"}
    ]

    print("--- [PASO 1: APILAR ACCIONES (append)] ---")
    for act in acciones:
        pila.append(act)
        print(f" -> Apilado en cima: [Paso {act['paso']}] {act['accion']}")
        print(f"    Pila actual (base -> cima): {[a['accion'] for a in pila]}")

    print("\n--- [PASO 2: INSPECCIONAR CIMA (PEEK) SIN EXTRAER] ---")
    if len(pila) > 0:
        cima = pila[-1]
        print(f" Cima actual (list[-1]): [Paso {cima['paso']}] {cima['accion']}")
        print(f" Tamaño de la pila intacto: {len(pila)} elementos")

    print("\n--- [PASO 3: DESAPILAR (pop) - OPERACIÓN DESHACER] ---")
    while len(pila) > 0:
        revertido = pila.pop()
        print(f" <- Deshaciendo acción: [Paso {revertido['paso']}] {revertido['accion']}")
        print(f"    Pila restante: {[a['accion'] for a in pila] if pila else '¡Pila vacía!'}")

    # Caso borde: Intentar desapilar cuando está vacía
    print("\n--- [PASO 4: CASO BORDE (Pila vacía)] ---")
    if len(pila) == 0:
        elemento = None
        print(" Intentando desapilar de pila vacía...")
        print(f" Resultado seguro: {elemento} (Sin excepciones de tipo IndexError)\n")


def mostrar_cuadro_comparativo():
    """
    Imprime un resumen visual comparativo entre FIFO y LIFO con listas nativas.
    """
    print("=" * 65)
    print("CUADRO COMPARATIVO: COLA (FIFO) vs PILA (LIFO) EN PYTHON")
    print("=" * 65)
    print(f"{'Característica':<20} | {'Cola (Queue - FIFO)':<22} | {'Pila (Stack - LIFO)':<20}")
    print("-" * 65)
    print(f"{'Orden de salida':<20} | {'Primero en entrar (1°)':<22} | {'Último en entrar (N°)':<20}")
    print(f"{'Método inserción':<20} | {'append(x) (al final)':<22} | {'append(x) (a la cima)':<20}")
    print(f"{'Método extracción':<20} | {'pop(0) (del inicio)':<22} | {'pop() (de la cima)':<20}")
    print(f"{'Complejidad extrae':<20} | {'O(N) (desplaza lista)':<22} | {'O(1) (inmediato)':<20}")
    print(f"{'Uso en el gestor':<20} | {'Turno de espera':<22} | {'Historial para deshacer':<20}")
    print("=" * 65)


if __name__ == "__main__":
    demostrar_cola_fifo()
    demostrar_pila_lifo()
    mostrar_cuadro_comparativo()
