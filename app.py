from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import csv

app = Flask(__name__)
app.secret_key = "secure_key_123"

# ------------------- BASE DE DATOS DE USUARIOS ---------------- #
users = {"admin": "1234"}

# ------------------- RUTAS DE ARCHIVOS ------------------- #
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_PATH = os.path.join(BASE_PATH, 'salaries.csv')

# ------------------- LOGIN ------------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("Usuario")
        password = request.form.get("Clave")
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

# ------------------- DASHBOARD (GRÁFICO) ------------------- #
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    plot_url = None
    try:
        if os.path.exists(CSV_PATH):
            data = pd.read_csv(CSV_PATH)
            if not data.empty:
                plt.figure(figsize=(10, 6))
                sns.set_style("whitegrid")
                sns.regplot(x='YearsExperience', y='Salary', data=data, 
                            scatter_kws={"color": "#6a1b9a"}, line_kws={"color": "#ff5252"})
                img = io.BytesIO()
                plt.savefig(img, format='png', bbox_inches='tight')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode('utf8')
                plt.close() 
    except Exception as e:
        print(f"Error: {e}")
    return render_template("dashboard.html", graph=plot_url)

# ------------------- RUTAS DE NAVEGACIÓN ------------------- #
@app.route("/usecase1")
def usecase1(): return render_template("usecase1.html")

@app.route("/usecase2")
def usecase2(): return render_template("usecase2.html")

@app.route("/usecase3")
def usecase3(): return render_template("usecase3.html")

@app.route("/usecase4") # <-- ESTA RUTA CARGA TU HTML DEL CHAT
def usecase4():
    return render_template("chatbot.html")

# ------------------- CHATBOT API (LÓGICA) ------------------- #
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "").lower()
    if "hola" in msg or "hi" in msg:
        reply = "¡Hola! Soy tu asistente de ML. ¿En qué puedo ayudarte?"
    elif "precio" in msg:
        reply = "Puedes calcular valores de propiedades en el Caso de Uso 1."
    else:
        reply = "Soy tu asistente inteligente 🤖."
    return jsonify({"reply": reply})

# ------------------- MODELOS Y LOGOUT ------------------- #
@app.route("/predict_salary", methods=["POST"])
def predict_salary():
    # ... (Tu lógica de predicción de salario aquí)
    return render_template("linear_application.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)