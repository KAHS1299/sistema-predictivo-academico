from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"


# ==============================
# LOGIN DATA (TEMPORAL)
# ==============================
USER = "admin"
PASSWORD = "1234"


# ==============================
# LOGIN REQUIRED FUNCTION
# ==============================
def login_required():
    return 'user' in session


# ==============================
# LOGIN / HOME
# ==============================
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == USER and password == PASSWORD:
        session['user'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Invalid username or password")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


# ==============================
# DASHBOARD
# ==============================
@app.route('/dashboard')
def dashboard():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('dashboard.html', user=session['user'])


# ==============================
# USE CASES
# ==============================
@app.route('/usecase1')
def usecase1():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('usecase1.html')


@app.route('/usecase2')
def usecase2():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('usecase2.html')


@app.route('/usecase3')
def usecase3():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('usecase3.html')


@app.route('/usecase4')
def usecase4():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('usecase4.html')


# ==============================
# CLASSIFICATION (AdaBoost)
# ==============================
@app.route('/classification_explanation')
def classification_explanation():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('classification_basic.html')


@app.route('/classification_application')
def classification_application():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('classification_application.html')


# ==============================
# SUPERVISED ML
# ==============================
@app.route('/linear_explanation')
def linear_explanation():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('linear_basic.html')


@app.route('/linear_application')
def linear_application():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('linear_application.html')


@app.route('/logistic_explanation')
def logistic_explanation():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('logistic_explanation.html')


@app.route('/logistic_application')
def logistic_application():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('logistic_application.html')

# ==============================
# UNSUPERVISED - STRUCTURE
# ==============================

@app.route('/unsupervised_basics')
def unsupervised_basics():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('unsupervised_basics.html')


@app.route('/kmeans_manual')
def kmeans_manual():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('kmeans_manual.html')


@app.route('/kmeans_application')
def kmeans_application():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('kmeans_application.html')

# ==============================
# RUN APP
# ==============================
if __name__ == '__main__':
    app.run(debug=True)