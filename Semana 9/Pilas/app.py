from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Instancia global temporal para el ejemplo web (Capacidad por defecto: 5)
from dataclasses import dataclass

class Stack:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items = []

    def is_empty(self): return len(self.items) == 0
    def is_full(self): return len(self.items) == self.capacity
    def push(self, item):
        if not self.is_full():
            self.items.append(item)
            return True, "Elemento apilado."
        return False, "La pila está llena."
    def pop(self):
        if not self.is_empty(): return self.items.pop()
        return None
    def peek(self):
        if not self.is_empty(): return self.items[-1]
        return None
    def get_stack(self): return list(reversed(self.items))

# Creamos una pila con capacidad de 5 elementos por defecto
mi_pila = Stack(capacity=5)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "items": mi_pila.get_stack(),
        "peek": mi_pila.peek(),
        "is_empty": mi_pila.is_empty(),
        "is_full": mi_pila.is_full(),
        "capacity": mi_pila.capacity
    })

@app.route("/api/push", methods=["POST"])
def api_push():
    data = request.get_json()
    valor = data.get("valor")
    if not valor:
        return jsonify({"success": False, "message": "El valor no puede estar vacío."}), 400
    
    success, message = mi_pila.push(valor)
    return jsonify({"success": success, "message": message})

@app.route("/api/pop", methods=["POST"])
def api_pop():
    item = mi_pila.pop()
    if item is not None:
        return jsonify({"success": True, "message": f"Elemento '{item}' desapilado."})
    return jsonify({"success": False, "message": "La pila está vacía."})

@app.route("/api/config", methods=["POST"])
def api_config():
    data = request.get_json()
    new_capacity = int(data.get("capacity", 5))
    global mi_pila
    mi_pila = Stack(capacity=new_capacity)
    return jsonify({"success": True, "message": f"Pila reiniciada con capacidad {new_capacity}."})

if __name__ == "__main__":
    app.run(debug=True)