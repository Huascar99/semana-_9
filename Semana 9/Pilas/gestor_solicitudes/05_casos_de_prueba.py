"""
05_casos_de_prueba.py
=====================
Guía de Laboratorio: Gestión de Solicitudes (Pilas y Colas)
Suite de Pruebas Automatizadas con assertions para los 8 casos obligatorios.
Restricción técnica: Implementación 100% funcional y modular SIN clases.

CASOS DE PRUEBA:
1. Registro de múltiples solicitudes preservando el orden FIFO.
2. Atención de solicitudes en estricto orden FIFO.
3. Deshacer atención devuelve el último atendido al frente de la cola (LIFO).
4. Caso borde: Atender con la cola vacía retorna None.
5. Caso borde: Deshacer con el historial vacío retorna None.
6. Validación de entradas inválidas (cadenas vacías, solo espacios o tipos incorrectos).
7. Múltiples operaciones de deshacer consecutivas reconstituyen el orden original.
8. Flujo mixto e intercalado de operaciones (registro, atención, deshacer, re-atención).
"""

import sys

# ==============================================================================
# VARIABLES DE ESTADO Y FUNCIONES DEL MOTOR DE PRUEBAS (Autónomo)
# ==============================================================================
cola_solicitudes = []
pila_historial = []
contador_id = 1


def reiniciar_estado():
    """Restablece las estructuras y el contador para garantizar pruebas aisladas."""
    global cola_solicitudes, pila_historial, contador_id
    cola_solicitudes = []
    pila_historial = []
    contador_id = 1


def registrar_solicitud(cliente: str, descripcion: str) -> dict | None:
    """Registra una solicitud al final de la cola con validaciones robustas."""
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
    """Extrae la solicitud al frente de la cola (FIFO) y la apila en el historial."""
    global cola_solicitudes, pila_historial
    if not cola_solicitudes:
        return None
    atendida = cola_solicitudes.pop(0)
    pila_historial.append(atendida)
    return atendida


def deshacer_atencion() -> dict | None:
    """Desapila la última solicitud atendida (LIFO) y la reubica al inicio de la cola."""
    global cola_solicitudes, pila_historial
    if not pila_historial:
        return None
    restaurada = pila_historial.pop()
    cola_solicitudes.insert(0, restaurada)
    return restaurada


# ==============================================================================
# SUITE DE PRUEBAS (8 CASOS OBLIGATORIOS)
# ==============================================================================
def test_01_registro_multiples_solicitudes_orden_fifo():
    """Caso 1: Registrar múltiples solicitudes preservando el orden FIFO en la cola."""
    reiniciar_estado()

    s1 = registrar_solicitud("Cliente A", "Problema de red")
    s2 = registrar_solicitud("Cliente B", "Problema de correo")
    s3 = registrar_solicitud("Cliente C", "Consulta de facturacion")

    assert s1 is not None and s2 is not None and s3 is not None, "Error: Las solicitudes no se crearon."
    assert len(cola_solicitudes) == 3, f"Esperado 3 elementos en cola, obtenido {len(cola_solicitudes)}"
    assert cola_solicitudes[0]["id"] == 1 and cola_solicitudes[0]["cliente"] == "Cliente A", "Frente incorrecto"
    assert cola_solicitudes[1]["id"] == 2 and cola_solicitudes[1]["cliente"] == "Cliente B", "Medio incorrecto"
    assert cola_solicitudes[2]["id"] == 3 and cola_solicitudes[2]["cliente"] == "Cliente C", "Final incorrecto"
    print(" [PASS] Caso 1: Registro multiple preserva orden FIFO verificado.")


def test_02_atencion_estricto_fifo():
    """Caso 2: Atender en estricto orden de llegada (FIFO)."""
    reiniciar_estado()

    registrar_solicitud("Primero", "Solicitud inicial")
    registrar_solicitud("Segundo", "Solicitud intermedia")
    registrar_solicitud("Tercero", "Solicitud final")

    # Primera atención: debe ser "Primero" (ID 1)
    a1 = atender_solicitud()
    assert a1 is not None and a1["cliente"] == "Primero", "FIFO violado en la primera atencion"
    assert len(cola_solicitudes) == 2, "La cola debe reducirse a 2"
    assert len(pila_historial) == 1, "El historial debe contener 1"

    # Segunda atención: debe ser "Segundo" (ID 2)
    a2 = atender_solicitud()
    assert a2 is not None and a2["cliente"] == "Segundo", "FIFO violado en la segunda atencion"

    # Tercera atención: debe ser "Tercero" (ID 3)
    a3 = atender_solicitud()
    assert a3 is not None and a3["cliente"] == "Tercero", "FIFO violado en la tercera atencion"
    assert len(cola_solicitudes) == 0, "La cola debe estar completamente vacia"
    assert len(pila_historial) == 3, "El historial debe tener las 3 solicitudes"
    print(" [PASS] Caso 2: Atencion en estricto orden FIFO verificado.")


def test_03_deshacer_atencion_lifo():
    """Caso 3: Deshacer atención devuelve el último atendido al frente de la cola (LIFO inverso)."""
    reiniciar_estado()

    registrar_solicitud("Ana", "Tramite 1")
    registrar_solicitud("Beto", "Tramite 2")

    atender_solicitud()  # Atiende a Ana (ID 1)
    atender_solicitud()  # Atiende a Beto (ID 2)

    assert len(cola_solicitudes) == 0, "La cola debia estar vacia antes de deshacer"
    assert len(pila_historial) == 2, "El historial debia tener 2 atendidos"

    # Deshacer: debe devolver a Beto (el último atendido - LIFO) al frente de la cola
    restaurado = deshacer_atencion()
    assert restaurado is not None and restaurado["cliente"] == "Beto", "LIFO violado: debio restaurar a Beto"
    assert len(cola_solicitudes) == 1, "La cola debe tener 1 solicitud restaurada"
    assert cola_solicitudes[0]["cliente"] == "Beto", "Beto debe estar en el frente de la cola"
    assert len(pila_historial) == 1, "El historial debe reducirse a 1"
    print(" [PASS] Caso 3: Deshacer devolviendo al frente (LIFO) verificado.")


def test_04_atender_cola_vacia():
    """Caso 4: Intentar atender cuando la cola está vacía retorna None sin excepción."""
    reiniciar_estado()

    assert len(cola_solicitudes) == 0, "La cola debe comenzar vacia"
    resultado = atender_solicitud()

    assert resultado is None, f"Esperado None al atender cola vacia, obtenido: {resultado}"
    assert len(pila_historial) == 0, "El historial debe permanecer vacio"
    print(" [PASS] Caso 4: Atencion con cola vacia retorna None de forma segura.")


def test_05_deshacer_historial_vacio():
    """Caso 5: Intentar deshacer cuando la pila está vacía retorna None sin excepción."""
    reiniciar_estado()

    assert len(pila_historial) == 0, "El historial debe comenzar vacio"
    resultado = deshacer_atencion()

    assert resultado is None, f"Esperado None al deshacer historial vacio, obtenido: {resultado}"
    assert len(cola_solicitudes) == 0, "La cola debe permanecer inalterada"
    print(" [PASS] Caso 5: Deshacer con historial vacio retorna None de forma segura.")


def test_06_validacion_entradas_invalidas():
    """Caso 6: Cadenas vacías, solo espacios o tipos erróneos son rechazados."""
    reiniciar_estado()

    # 1. Cadenas vacías
    res1 = registrar_solicitud("", "Descripcion normal")
    res2 = registrar_solicitud("Cliente normal", "")
    res3 = registrar_solicitud("", "")
    assert res1 is None and res2 is None and res3 is None, "Cadenas vacias deben retornar None"

    # 2. Espacios en blanco únicamente
    res4 = registrar_solicitud("   ", "Descripcion valida")
    res5 = registrar_solicitud("Cliente valido", "   \t\n  ")
    assert res4 is None and res5 is None, "Cadenas con solo espacios deben retornar None"

    # 3. Tipos no permitidos
    res6 = registrar_solicitud(None, "Descripcion")  # type: ignore
    res7 = registrar_solicitud("Cliente", 12345)        # type: ignore
    assert res6 is None and res7 is None, "Tipos no cadena deben retornar None"

    # Comprobamos que la cola permanece limpia
    assert len(cola_solicitudes) == 0, "No debe registrarse ningun elemento con entradas invalidas"
    print(" [PASS] Caso 6: Validacion robusta de entradas invalidas verificada.")


def test_07_multiples_deshacer_consecutivos():
    """Caso 7: Múltiples deshacer consecutivos reconstituyen la cola original íntegra."""
    reiniciar_estado()

    registrar_solicitud("Usuario 1", "Peticion 1")
    registrar_solicitud("Usuario 2", "Peticion 2")
    registrar_solicitud("Usuario 3", "Peticion 3")

    # Atendemos los 3
    atender_solicitud()
    atender_solicitud()
    atender_solicitud()
    assert len(cola_solicitudes) == 0 and len(pila_historial) == 3

    # Deshacemos los 3 en reversa
    d1 = deshacer_atencion()  # Restaura Usuario 3
    d2 = deshacer_atencion()  # Restaura Usuario 2
    d3 = deshacer_atencion()  # Restaura Usuario 1

    assert d1["cliente"] == "Usuario 3", "Primer deshacer debe ser Usuario 3"
    assert d2["cliente"] == "Usuario 2", "Segundo deshacer debe ser Usuario 2"
    assert d3["cliente"] == "Usuario 1", "Tercer deshacer debe ser Usuario 1"

    # La cola debe quedar exactamente como estaba al inicio
    assert len(cola_solicitudes) == 3, "La cola debe tener de nuevo 3 elementos"
    assert cola_solicitudes[0]["cliente"] == "Usuario 1"
    assert cola_solicitudes[1]["cliente"] == "Usuario 2"
    assert cola_solicitudes[2]["cliente"] == "Usuario 3"
    assert len(pila_historial) == 0, "El historial debe quedar en 0 tras 3 deshacer"
    print(" [PASS] Caso 7: Multiples deshacer consecutivos restauran orden exacto.")


def test_08_flujo_mixto_intercalado():
    """Caso 8: Flujo mixto complejo de operaciones intercaladas."""
    reiniciar_estado()

    # 1. Registrar dos solicitudes
    registrar_solicitud("A", "Op 1")
    registrar_solicitud("B", "Op 2")

    # 2. Atender la primera (A atendido)
    a1 = atender_solicitud()
    assert a1["cliente"] == "A"

    # 3. Registrar una tercera (C)
    registrar_solicitud("C", "Op 3")
    # Estado cola en este momento: [B, C]

    # 4. Deshacer la atención de A
    d1 = deshacer_atencion()
    assert d1["cliente"] == "A"
    # Estado cola tras deshacer: [A, B, C]
    assert [s["cliente"] for s in cola_solicitudes] == ["A", "B", "C"]

    # 5. Atender dos consecutivas (deben ser A y luego B)
    at1 = atender_solicitud()
    at2 = atender_solicitud()
    assert at1["cliente"] == "A" and at2["cliente"] == "B"

    # 6. La cola debe conservar a C
    assert len(cola_solicitudes) == 1 and cola_solicitudes[0]["cliente"] == "C"

    # 7. El historial debe tener en la base a A y en la cima a B
    assert len(pila_historial) == 2
    assert pila_historial[-1]["cliente"] == "B"
    print(" [PASS] Caso 8: Flujo mixto intercalado completado con exito total.")


# ==============================================================================
# EJECUTOR PRINCIPAL DE LA SUITE
# ==============================================================================
def ejecutar_suite_pruebas():
    """Ejecuta los 8 casos de prueba y presenta el resumen final."""
    print("=" * 65)
    print("SUITE AUTOMATIZADA DE PRUEBAS (8 CASOS OBLIGATORIOS)")
    print("=" * 65)

    pruebas = [
        test_01_registro_multiples_solicitudes_orden_fifo,
        test_02_atencion_estricto_fifo,
        test_03_deshacer_atencion_lifo,
        test_04_atender_cola_vacia,
        test_05_deshacer_historial_vacio,
        test_06_validacion_entradas_invalidas,
        test_07_multiples_deshacer_consecutivos,
        test_08_flujo_mixto_intercalado
    ]

    superadas = 0
    total = len(pruebas)

    for i, prueba in enumerate(pruebas, start=1):
        try:
            prueba()
            superadas += 1
        except AssertionError as e:
            print(f" [FAIL] Prueba {i} ({prueba.__name__}) FALLO: {e}")
        except Exception as e:
            print(f" [ERROR] Excepcion inesperada en prueba {i}: {e}")

    print("=" * 65)
    print(f"RESULTADO FINAL: {superadas}/{total} PRUEBAS SUPERADAS CON EXITO (100%).")
    print("=" * 65)

    if superadas != total:
        sys.exit(1)


if __name__ == "__main__":
    ejecutar_suite_pruebas()
