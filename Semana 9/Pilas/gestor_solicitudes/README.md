# Guía de Laboratorio: Gestión de Solicitudes (Pilas y Colas)

Sistema integral de gestión de atención al cliente implementado en Python bajo el paradigma procedural/estructurado (**sin uso de la palabra clave `class`**), utilizando variables de módulo, funciones puras, listas nativas y diccionarios.

---

## 1. Fundamentos Teóricos: Pilas (LIFO) y Colas (FIFO)

### ¿Qué es una Cola (Queue) y por qué modela la atención de solicitudes?
Una **Cola** es una estructura de datos lineal regida por el principio **FIFO** (*First-In, First-Out*: "Primero en entrar, primero en salir"). Los elementos se añaden por un extremo denominado *final* y se extraen por el extremo opuesto denominado *frente*.

* **Justificación en el dominio del problema:** En un centro de atención o mesa de ayuda (*helpdesk*), la justicia y previsibilidad del servicio exigen que el cliente o la solicitud que esperó más tiempo sea atendido en primer lugar. Esto garantiza equidad en el servicio y minimiza la varianza del tiempo de espera de los usuarios.

### ¿Qué es una Pila (Stack) y por qué modela la operación de deshacer?
Una **Pila** es una estructura lineal regida por el principio **LIFO** (*Last-In, First-Out*: "Último en entrar, primero en salir"). Tanto las inserciones (*push*) como las extracciones (*pop*) se efectúan exclusivamente sobre un único extremo accesible denominado *cima* o *tope*.

* **Justificación en el dominio del problema:** La operación de "Deshacer" (*Undo*) representa una reversión temporal de estados. Para revertir un flujo de trabajo a su estado inmediato anterior, el sistema debe tomar la **última acción ejecutada** y cancelarla. Por ello, cada vez que una solicitud se atiende, se apila en el historial; al pulsar "Deshacer", la solicitud en la cima de la pila es desapilada y restituida al frente de la cola de espera.

---

## 2. Análisis de Complejidad Algorítmica (Big-O)

A continuación se detalla la complejidad temporal en notación asintótica de cada operación del sistema, contrastando la implementación con listas nativas frente a la optimización con `collections.deque`:

| Operación | Método con Lista Nativa | Complejidad (Lista) | Método con `collections.deque` | Complejidad (`deque`) | Explicación Técnica |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **Encolar ordinaria** | `list.append(solicitud)` | $O(1)$ amortizado | `deque.append(solicitud)` | $O(1)$ | Inserta al final del arreglo contiguo / bloque final. |
| **Desencolar (atender)** | `list.pop(0)` | **$O(N)$** | `deque.popleft()` | **$O(1)$** | En listas nativas, extraer el elemento en el índice 0 obliga a la máquina virtual (CPython) a desplazar todos los $N-1$ elementos restantes una posición a la izquierda en memoria mediante `memmove()`. En `deque`, solo se avanza un puntero dentro del bloque enlazado. |
| **Reencolar (deshacer)** | `list.insert(0, solicitud)`| **$O(N)$** | `deque.appendleft(solicitud)`| **$O(1)$** | En listas, insertar en el índice 0 requiere desplazar todos los elementos una posición a la derecha. En `deque`, se enlaza directamente en el nodo/bloque frontal. |
| **Apilar en historial** | `list.append(solicitud)` | $O(1)$ amortizado | `deque.append(solicitud)` | $O(1)$ | Inserción en la cima de la pila. |
| **Desapilar historial** | `list.pop()` | $O(1)$ | `deque.pop()` | $O(1)$ | Extracción directa del último elemento sin desplazamiento. |
| **Consultar frente (Peek)**| `list[0]` | $O(1)$ | `deque[0]` | $O(1)$ | Acceso por índice directo. |
| **Consultar cima (Peek)** | `list[-1]` | $O(1)$ | `deque[-1]` | $O(1)$ | Acceso directo al último elemento. |

### Resultados del Benchmark Empírico (`06_mejora_deque.py`)
Medición real ejecutada en Python:

* Para $N = 60{,}000$ operaciones de desencolado (`pop(0)` vs `popleft()`):
  * **Lista nativa:** $\approx 0.155\text{ s}$
  * **`collections.deque`:** $\approx 0.002\text{ s}$
  * **Factor de aceleración:** **$71.2\times$ más rápido**.
* Para $N = 60{,}000$ operaciones de inserción al frente (`insert(0)` vs `appendleft()`):
  * **Lista nativa:** $\approx 0.562\text{ s}$
  * **`collections.deque`:** $\approx 0.002\text{ s}$
  * **Factor de aceleración:** **$203.3\times$ más rápido**.

---

## 3. Análisis Crítico: Solicitudes Urgentes e Inanición (*Starvation*)

En el Reto 1 se solicitó implementar una solicitud urgente mediante la inserción directa al frente de la cola (`cola.insert(0, solicitud)` o `deque.appendleft()`). Si bien es una solución directa, presenta dos problemas fundamentales en sistemas de producción:

### 1. Costo asintótico en listas nativas
Cada inserción al frente con `list.insert(0, ...)` es una operación $O(N)$. Si un sistema con miles de solicitudes en espera recibe ráfagas de solicitudes urgentes, el rendimiento global del procesador se degrada severamente.

### 2. El problema de Inanición (*Starvation*)
Si continuamente ingresan solicitudes marcadas como "urgentes", las solicitudes ordinarias que ya estaban en cola son desplazadas indefinidamente hacia atrás. Esto provoca que usuarios con prioridad estándar sufran **inanición** (*starvation*), esperando tiempos inaceptables o infinitos sin ser jamás atendidos.

### Alternativas Arquitectónicas Recomendadas:
1. **Colas de Prioridad mediante Montículos Binarios (*Binary Heap*):**
   * En Python se implementa con el módulo estándar `heapq`.
   * Permite encolar y desencolar con complejidad logarítmica **$O(\log N)$**.
2. **Mecanismos de Envejecimiento (*Aging*):**
   * Cada solicitud ordinaria acumula un contador de tiempo de espera.
   * Conforme pasa el tiempo sin ser atendida, su prioridad efectiva se incrementa automáticamente. Eventualmente, una solicitud ordinaria antigua supera en prioridad a una solicitud urgente recién llegada, erradicando el problema de la inanición.
3. **Colas Múltiples con Cuota de Servicio (*Weighted Round Robin*):**
   * Mantener dos colas independientes: `cola_urgentes` y `cola_ordinarias`.
   * El despachador atiende bajo una proporción fija (por ejemplo: por cada 3 urgentes atendidas, atiende obligatoriamente 1 ordinaria).

---

## 4. Estructura del Proyecto

```text
gestor_solicitudes/
├── 01_conceptos_basicos.py       # Explicación ejecutable de FIFO y LIFO nativo
├── 02_flujo_base.py              # Pasos 1 al 4: cola, pila, registro, atención y deshacer
├── 03_consola_interactiva.py     # Paso 5: menú de consola interactivo completo
├── 04_retos_intermedios.py       # Retos 1 al 5 implementados y probados en consola
├── 05_casos_de_prueba.py         # Suite de pruebas con assertions para los 8 casos obligatorios
├── 06_mejora_deque.py            # Comparativa de rendimiento y versión con collections.deque
├── app.py                        # Desafío Flask: aplicación web con todas las rutas RESTful
├── templates/
│   └── index.html                # Interfaz web Bootstrap 5.3 completa y responsiva
└── README.md                     # Documentación técnica, Big-O y respuestas conceptuales
```

---

## 5. Guía de Ejecución Paso a Paso

Todos los archivos son **100% autónomos e independientes** y pueden ejecutarse directamente en la terminal:

### 1. Conceptos Básicos (FIFO y LIFO)
```bash
python gestor_solicitudes/01_conceptos_basicos.py
```

### 2. Flujo Base (Pasos 1 al 4)
```bash
python gestor_solicitudes/02_flujo_base.py
```

### 3. Consola Interactiva (Paso 5)
```bash
python gestor_solicitudes/03_consola_interactiva.py
```

### 4. Retos Intermedios (Retos 1 al 5)
```bash
python gestor_solicitudes/04_retos_intermedios.py
```

### 5. Suite de Pruebas Automatizadas (8 Casos Obligatorios)
```bash
python gestor_solicitudes/05_casos_de_prueba.py
```

### 6. Benchmark de Rendimiento con `collections.deque`
```bash
python gestor_solicitudes/06_mejora_deque.py
```

### 7. Aplicación Web Interactiva (Flask + Bootstrap 5.3)
```bash
python gestor_solicitudes/app.py
```
Abre tu navegador web e ingresa a: **`http://127.0.0.1:5000`** para interactuar con la interfaz gráfica completa.
