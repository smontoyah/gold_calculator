from flask import Flask, request, jsonify, render_template
import numpy as np
from scipy.optimize import curve_fit
import os

# Datos de la tabla
kilates = np.array([24, 22, 20, 18, 14, 12, 10])  # Kilates
densidad = np.array([19.32, 17.69, 16.08, 14.47, 11.25, 9.65, 8.04])  # Densidad
ley = np.array([100, 916, 900, 750, 585, 500, 417])  # Ley

# Función polinómica para ajuste
def poly_func(x, a, b, c):
    return a * x**2 + b * x + c

# Ajuste para kilates
params_k, _ = curve_fit(poly_func, densidad, kilates)
# Ajuste para ley
params_l, _ = curve_fit(poly_func, densidad, ley)

# Función para estimar kilates y ley
def estimar_kilates_ley(densidad_input):
    kilates_est = poly_func(densidad_input, *params_k)
    ley_est = poly_func(densidad_input, *params_l)
    return kilates_est, ley_est

# Inicializar Flask
app = Flask(__name__)

# Ruta principal con formulario
@app.route('/')
def index():
    return render_template('index.html')  # Página HTML para la interfaz

# API para estimar kilates y ley
@app.route('/api/calcular', methods=['POST'])
def calcular():
    try:
        data = request.json
        densidad_input = float(data['densidad'])
        kilates_estimados, ley_estimada = estimar_kilates_ley(densidad_input)
        return jsonify({
            "kilates": round(kilates_estimados, 2),
            "ley": round(ley_estimada, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

