from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "secret123"


# ==============================
# LOGIN DATA (TEMPORAL)
# ==============================
USER = "admin"
PASSWORD = "1234"

#test


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

@app.route('/manual_exercise')
def manual_exercise():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('manual_exercise.html')

@app.route('/kmeans_manual')
def kmeans_manual():
    if not login_required():
        return redirect(url_for('home'))
    return render_template('kmeans_manual.html')

@app.route('/kmeans_application')
def kmeans_application():

    df = pd.read_excel('kmeans_dataset.xlsx')

    X = df[['Products_Sold (X)', 'Profit (Y)']].copy()
    X = X.apply(pd.to_numeric, errors='coerce').dropna()

    if X.empty or X.shape[1] < 2:
        return "Error: dataset vacío o columnas inválidas"

    # KMEANS
    kmeans = KMeans(n_clusters=3, random_state=42)
    df = df.loc[X.index].copy()
    df['Cluster'] = kmeans.fit_predict(X)
    centroids = kmeans.cluster_centers_

    # SUMMARY
    summary = (
        df.groupby('Cluster')[['Products_Sold (X)', 'Profit (Y)']]
          .agg(['count','mean','min','max'])
          .round(2)
    )

    # ====== CLUSTER GRAPH ======
    plt.figure(figsize=(8,6))
    plt.scatter(X.iloc[:,0], X.iloc[:,1], c=df['Cluster'], cmap='viridis', s=60)
    plt.scatter(centroids[:,0], centroids[:,1],
                color='red', s=300, marker='X', label='Centroids')
    plt.title('K-Means Clustering')
    plt.xlabel('Products Sold')
    plt.ylabel('Profit')
    plt.legend()
    plt.tight_layout()

    os.makedirs('static/img', exist_ok=True)

    img_path = 'static/img/clusters.png'
    plt.savefig(img_path)
    plt.close()

    # ====== VARIANCE GRAPH ======
    inertia_values = []

    for k in range(1, 6):
        km = KMeans(n_clusters=k, random_state=42)
        km.fit(X)
        inertia_values.append(km.inertia_)

    plt.figure()
    plt.plot(range(1,6), inertia_values, marker='o')
    plt.title('Variance Reduction Across Iterations')
    plt.xlabel('Clusters')
    plt.ylabel('Variance')
    plt.grid()

    variance_path = 'static/img/variance.png'
    plt.savefig(variance_path)
    plt.close()

    # ====== RETURN ======
    return render_template(
        'kmeans_application.html',
        tables=df.head(40).to_html(
            classes='table table-striped table-hover text-center', index=False
        ),
        summary=summary.to_html(classes='table table-sm table-striped text-center'),
        centroids=centroids,
        image=img_path,
        variance_img=variance_path,  
        total=len(df),
        columns=['Products_Sold (X)', 'Profit (Y)']
    )

# ==============================
# RUN APP
# ==============================
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)