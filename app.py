from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pickle

app = Flask(__name__)
app.secret_key = "secure key"

# ------------------- USERS -------------------
users = {"admin": "1234"}


# ------------------- LOGIN -------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["Usuario"]
        password = request.form["Clave"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# ------------------- DASHBOARD -------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


# ------------------- USE CASES -------------------
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


# ------------------- LINEAR REGRESSION -------------------
@app.route("/linear")
def linear():
    return render_template("linear.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        gpa = float(request.form["gpa"])
        courses = int(request.form["courses"])
        hours = float(request.form["hours"])
        failed = int(request.form["failed"])

        with open("model.pkl", "rb") as f:
            model = pickle.load(f)

        X_new = [[gpa, courses, hours, failed]]

        risk_class = model.predict(X_new)[0]
        risk_prob = model.predict_proba(X_new)[0][1]

        result = "HIGH RISK" if risk_class == 1 else "LOW RISK"
        prediction = f"Prediction: {result} (Probability: {risk_prob:.2f})"

        return render_template("linear.html", prediction=prediction)

    except Exception as e:
        return render_template("linear.html", prediction=f"Error: {str(e)}")


# ------------------- USE CASE 1 -------------------
@app.route("/predict_house", methods=["POST"])
def predict_house():
    size = float(request.form["size"])
    rooms = int(request.form["rooms"])
    age = int(request.form["age"])

    price = (size * 3000) + (rooms * 5000) - (age * 1000)

    result = f"Estimated Price: ${price}"
    return render_template("usecase1.html", result=result)


# ------------------- USE CASE 2 -------------------
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


# ------------------- USE CASE 3 -------------------
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


# ------------------- CHATBOT -------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data["message"].lower()

    if "hello" in msg:
        reply = "Hi! How can I help you?"
    elif "price" in msg:
        reply = "You can use the house prediction model."
    elif "health" in msg:
        reply = "Try the medical diagnosis model."
    elif "student" in msg:
        reply = "Use the student performance model."
    else:
        reply = "I am your ML assistant 🤖"

    return jsonify({"reply": reply})


# ------------------- LOGOUT -------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ------------------- RUN -------------------
if __name__ == "__main__":
    app.run(debug=True)