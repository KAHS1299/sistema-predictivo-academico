from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)
# Security key for session management
app.secret_key = "secure_key_123"

# ------------------- USERS DATABASE -------------------
users = {"admin": "1234"}

# ------------------- LOGIN ROUTE -------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Corregido: Ahora coincide con tu HTML ("Usuario" y "Clave")
        username = request.form["Usuario"]
        password = request.form["Clave"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ------------------- DASHBOARD (WITH ANALYTICS) -------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    
    plot_url = None
    try:
        # 1. Load the dataset (Ensure 'salaries.csv' is in your root folder)
        data = pd.read_csv('salaries.csv')

        # 2. Configure visualization style
        plt.figure(figsize=(10, 6))
        sns.set_style("whitegrid")
        
        # Linear Regression Plot (Purple dots, Red line)
        sns.regplot(x='YearsExperience', y='Salary', data=data, 
                    scatter_kws={"color": "#6a1b9a", "alpha":0.6}, 
                    line_kws={"color": "#ff5252", "lw": 3})
        
        plt.title('Analysis: Salary vs. Work Experience', fontsize=14)
        plt.xlabel('Years of Experience', fontsize=12)
        plt.ylabel('Salary ($)', fontsize=12)
        plt.tight_layout()

        # 3. Save plot to a memory buffer
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        
        # 4. Encode to Base64 string for the HTML template
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close() 
        
    except Exception as e:
        print(f"Error generating graph: {e}")

    # Enviamos 'graph' al HTML
    return render_template("dashboard.html", graph=plot_url)

# ------------------- NAVIGATION ROUTES -------------------
@app.route("/usecase1")
def usecase1():
    return render_template("usecase1.html")

@app.route("/usecase2")
def usecase2():
    return render_template("usecase2.html")

@app.route("/usecase3")
def usecase3():
    return render_template("usecase3.html")

# ------------------- PREDICTION MODELS -------------------

#---------------DATASET--------------------

@app.route("/predict_salary", methods=["POST"])
def predict_salary():
    experience = float(request.form["experience"])
    education = int(request.form["education"])
    hours = float(request.form["hours"])

    salary = (experience * 200) + (education * 500) + (hours * 20)
    result = f"Estimated Salary: ${salary:,.2f}"

    return render_template("linear_application.html", result=result)


# ------------------- USE CASE 1 -------------------
@app.route("/predict_house", methods=["POST"])
def predict_house():
    size = float(request.form["size"])
    rooms = int(request.form["rooms"])
    age = int(request.form["age"])

    price = (size * 3000) + (rooms * 5000) - (age * 1000)
    result = f"Estimated Price: ${price:,.2f}"
    return render_template("usecase1.html", result=result)

# ------------------- CHATBOT API -------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data["message"].lower()

    if "hello" in msg or "hi" in msg:
        reply = "Hello! I am your AI assistant. How can I help you today?"
    elif "price" in msg:
        reply = "You can calculate property values in Use Case 1."
    else:
        reply = "I am your ML assistant 🤖."

    return jsonify({"reply": reply})

# ------------------- LOGOUT -------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/linear")
def linear_page():
    return render_template("linear_application.html")

# ESTA PARTE SIEMPRE DEBE IR AL FINAL DE TODO
if __name__ == "__main__":
    app.run(debug=True)