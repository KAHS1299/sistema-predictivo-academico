from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pickle

app = Flask(__name__)
app.secret_key = "secret_key"

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

        # Load model
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)

        # Input data
        X_new = [[gpa, courses, hours, failed]]

        # Prediction
        risk_class = model.predict(X_new)[0]
        risk_prob = model.predict_proba(X_new)[0][1]

        result = "HIGH RISK" if risk_class == 1 else "LOW RISK"
        prediction = f"Prediction: {result} (Probability: {risk_prob:.2f})"

        return render_template("linear.html", prediction=prediction)

    except Exception as e:
        return render_template("linear.html", prediction=f"Error: {str(e)}")

# ------------------- SPAM DETECTION -------------------
@app.route("/spam", methods=["POST"])
def spam():
    email_text = request.form["correo"]

    spam_result = "Likely SPAM" if "gratis" in email_text.lower() else "Not SPAM"

    return render_template("dashboard.html", spam_result=spam_result)


# ------------------- CHATBOT -------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]

    reply = f"I received your message: {user_message}"

    return jsonify({"reply": reply})


# ------------------- LOGOUT -------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
#----------------------------------------------
@app.route("/predict_house", methods=["POST"])
def predict_house():
    size = float(request.form["size"])
    rooms = int(request.form["rooms"])
    age = int(request.form["age"])

    price = (size * 3000) + (rooms * 5000) - (age * 1000)

    result = f"Estimated Price: ${price}"

    return render_template("usecase1.html", result=result)
# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(debug=True)

