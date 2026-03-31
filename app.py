from flask import Flask, render_template, request, redirect, url_for, session, jsonify

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc

df = pd.read_csv("boston.csv")

X = df[["RM"]]
y = df["MEDV"]

model = LinearRegression()
model = LinearRegression()
model.fit(X, y)

app = Flask(__name__)
app.secret_key = "secure_key"

#-------------DATASET LOGISTIC----------------

df_log = pd.read_csv("loan_risk_prediction_dataset.csv")

num_cols = df_log.select_dtypes(include=['number']).columns
df_log = df_log.dropna()

df_log[num_cols] = df_log[num_cols].fillna(df_log[num_cols].mean())

X = df_log[["Age","Income","LoanAmount","CreditScore","YearsExperience"]]
y = df_log["LoanApproved"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)


# -----------USERS (LOGIN SIMPLE)----------
users = {
    "admin": "1234"
}

#-------- FUNCION LOGIN REQUIRED------------
def login_required():
    return "user" in session


# ==============================
# LOGIN
# ==============================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")



#---------------- DASHBOARD----------------

@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("dashboard.html")



#-------------USE CASES------------------

@app.route("/usecase1")
def usecase1():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("usecase1.html")


@app.route("/usecase2")
def usecase2():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("usecase2.html")


@app.route("/usecase3")
def usecase3():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("usecase3.html")


@app.route("/usecase4")
def usecase4():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("usecase4.html")



#---------------- LINEAR REGRESSION--------------

@app.route("/linear_explanation")
def linear_explanation():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("linear_basic.html")


@app.route("/linear_application")
def linear_application():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("linear_application.html")



#---------------LOGISTIC REGRESSION----------------

@app.route("/logistic_application", methods=["GET","POST"])
def logistic_application():

    result = None
    cm_plot = None
    roc_plot = None
    dynamic_plot = None

    if request.method == "POST":
        try:
            age = float(request.form["age"])
            income = float(request.form["income"])
            loan = float(request.form["loan"])
            credit = float(request.form["credit"])
            exp = float(request.form["exp"])

            input_data = pd.DataFrame([{
                "Age": age,
                "Income": income,
                "LoanAmount": loan,
                "CreditScore": credit,
                "YearsExperience": exp
            }])

            pred = log_model.predict(input_data)
            prob = log_model.predict_proba(input_data)[0][1]

            result = f"Approved ✅ (Probability: {prob:.2f})" if pred[0] == 1 else f"Rejected ❌ (Probability: {prob:.2f})"

        except:
            result = "Error in input data"

        # ===== GRAFICA DINAMICA =====
        plt.figure()

        # datos reales
        plt.scatter(df_log["CreditScore"], df_log["LoanAmount"], c=y)

        # punto del usuario
        plt.scatter(credit, loan, marker='o', s=150)

        plt.xlabel("Credit Score")
        plt.ylabel("Loan Amount")
        plt.title("Loan Approval Distribution")

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        dynamic_plot = base64.b64encode(img.getvalue()).decode()
        plt.close()

    # METRICAS
    y_pred = log_model.predict(X_test)
    y_prob = log_model.predict_proba(X_test)[:,1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # MATRIZ
    cm = confusion_matrix(y_test, y_pred)

    plt.figure()
    plt.imshow(cm)
    plt.title("Confusion Matrix")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    cm_plot = base64.b64encode(img.getvalue()).decode()
    plt.close()

    # ROC
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr)
    plt.plot([0,1],[0,1],'--')
    plt.title(f"ROC Curve (AUC={roc_auc:.2f})")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    roc_plot = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template("logistic_application.html",
        result=result,
        accuracy=round(accuracy,2),
        precision=round(precision,2),
        recall=round(recall,2),
        f1=round(f1,2),
        cm_plot=cm_plot,
        roc_plot=roc_plot,
        dynamic_plot=dynamic_plot,
    )
@app.route("/logistic_explanation")
def logistic_explanation():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("logistic_basic.html")

# ==============================
# CLASSIFICATION MODEL
# ==============================
@app.route("/classification_explanation")
def classification_explanation():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("classification_basic.html")


@app.route("/classification_application")
def classification_application():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("classification_application.html")

# ==============================
# PREDICCION - REGRESION LINEAL
# ==============================
@app.route("/predict_house_ml", methods=["GET", "POST"])
def predict_house_ml():
    if not login_required():
        return redirect(url_for("login"))

    plot_url = None
    result = None

    if request.method == "POST":
        try:
            rm = float(request.form["rm"])

            # -------- PREDICCIÓN REAL --------
            prediction = model.predict([[rm]])
            result = f"Estimated Price (MEDV): {prediction[0]:.2f}"

            # -------- GRAFICA --------
            plt.figure()

            # puntos reales
            plt.scatter(X, y)

            # línea de regresión
            plt.plot(X, model.predict(X))

            # punto ingresado
            plt.scatter(rm, prediction, marker='o')

            plt.xlabel("Rooms (RM)")
            plt.ylabel("House Price (MEDV)")
            plt.title("Linear Regression Model")

            # convertir a imagen
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()

        except Exception:
            result = "Error in input data"

    return render_template(
        "linear_application.html",
        result=result,
        plot=plot_url
    )


# ==============================
# USE CASE 1 - HOUSE SIMPLE
# ==============================
@app.route("/predict_house", methods=["POST"])
def predict_house():
    if not login_required():
        return redirect(url_for("login"))

    try:
        size = float(request.form["size"])
        rooms = int(request.form["rooms"])
        age = int(request.form["age"])

        price = (size * 3000) + (rooms * 5000) - (age * 1000)

        result = f"Estimated Price: ${price:,.2f}"

    except Exception:
        result = "Error in input data"

    return render_template("usecase1.html", result=result)


# ==============================
# USE CASE 2 - HEALTH
# ==============================
@app.route("/predict_health", methods=["POST"])
def predict_health():
    if not login_required():
        return redirect(url_for("login"))

    try:
        age = int(request.form["age"])
        heart = int(request.form["heart"])
        pressure = int(request.form["pressure"])

        if heart > 100 or pressure > 140:
            result = "⚠️ High risk of disease"
        else:
            result = "✅ Healthy"

    except Exception:
        result = "Error in input data"

    return render_template("usecase2.html", result=result)


# ==============================
# USE CASE 3 - STUDENT
# ==============================
@app.route("/predict_student", methods=["POST"])
def predict_student():
    if not login_required():
        return redirect(url_for("login"))

    try:
        hours = float(request.form["hours"])
        attendance = float(request.form["attendance"])
        grades = float(request.form["grades"])

        if hours > 2 and attendance > 70 and grades > 3:
            result = "🎉 Pass"
        else:
            result = "❌ Fail"

    except Exception:
        result = "Error in input data"

    return render_template("usecase3.html", result=result)


# ==============================
# CHATBOT
# ==============================
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


# ==============================
# LOGOUT
# ==============================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ==============================
# RUN APP
# ==============================

@app.route("/predict_classification", methods=["POST"])
def predict_classification():
    f1 = request.form["feat1"]
    f2 = request.form["feat2"]
    # Por ahora, una lógica simple para probar que el botón funciona:
    res = "Clase A" if float(f1) > 50 else "Clase B"
    return render_template("classification_application.html", result=res)

if __name__ == "__main__":
    app.run(debug=True)