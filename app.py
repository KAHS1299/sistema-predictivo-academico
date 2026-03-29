from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "secure_key"

# ---------------- USERS ----------------
users = {"admin": "1234"}

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["Usuario"]
        password = request.form["Clave"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


# ---------------- USE CASES ----------------
@app.route("/usecase1")
def usecase1():
    return render_template("usecase1.html")

@app.route("/usecase2")
def usecase2():
    return render_template("usecase2.html")

@app.route("/usecase3")
def usecase3():
    return render_template("usecase3.html")

@app.route("/usecase4")
def usecase4():
    return render_template("usecase4.html")


# ---------------- LINEAR OPTION ----------------
@app.route("/linear_explanation")
def linear_explanation():
    return render_template("linear_basic.html")

@app.route("/linear_application")
def linear_application():
    return render_template("linear_application.html")

# ---------------- PREDICTION - LINEAR REGRESSION ----------------
@app.route("/predict_salary", methods=["POST"])
def predict_salary():
    try:
        experience = float(request.form["experience"])
        education = int(request.form["education"])
        hours = float(request.form["hours"])

        # Modelo de regresión múltiple (simulado)
        salary = (experience * 200) + (education * 500) + (hours * 20)

        result = f"Estimated Salary: ${salary}"

        return render_template("linear_application.html", result=result)

    except:
        return render_template("linear_application.html", result="Error in input data")
    
# ---------------- LOGISTIC REGRESSION ----------------

@app.route("/logistic_explanation")
def logistic_explanation():
    return render_template("logistic_basic.html")

@app.route("/logistic_application")
def logistic_application():
    return render_template("logistic_application.html")


# ---------------- USE CASE 1 ----------------
@app.route("/predict_house", methods=["POST"])
def predict_house():
    size = float(request.form["size"])
    rooms = int(request.form["rooms"])
    age = int(request.form["age"])

    price = (size * 3000) + (rooms * 5000) - (age * 1000)

    result = f"Estimated Price: ${price}"

    return render_template("usecase1.html", result=result)


# ---------------- USE CASE 2 ----------------
@app.route("/predict_health", methods=["POST"])
def predict_health():
    age = int(request.form["age"])
    heart = int(request.form["heart"])
    pressure = int(request.form["pressure"])

    if heart > 100 or pressure > 140:
        result = "⚠️ High risk of disease"
    else:
        result = "✅ Healthy"

    return render_template("usecase2.html", result=result)


# ---------------- USE CASE 3 ----------------
@app.route("/predict_student", methods=["POST"])
def predict_student():
    hours = float(request.form["hours"])
    attendance = float(request.form["attendance"])
    grades = float(request.form["grades"])

    if hours > 2 and attendance > 70 and grades > 3:
        result = "🎉 Pass"
    else:
        result = "❌ Fail"

    return render_template("usecase3.html", result=result)


# ---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data["message"].lower()

    if "hello" in msg:
        reply = "Hi! How can I help you?"
    elif "price" in msg:
        reply = "Try the house prediction model."
    elif "health" in msg:
        reply = "Try the medical diagnosis model."
    elif "student" in msg:
        reply = "Use the student performance model."
    else:
        reply = "I am your ML assistant 🤖"

    return jsonify({"reply": reply})


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)