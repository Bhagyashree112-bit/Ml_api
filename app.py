from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = "supersecretkey"   # required for session login

# Load your model
model = joblib.load("heart_disease_model.pkl")

# Dummy login credentials
USERNAME = "admin"
PASSWORD = "123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")

@app.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    prediction_text = ""
    if request.method == "POST":
        try:
            age = int(request.form["age"])
            sex = 1 if request.form["sex"] == "Male" else 0
            cp = int(request.form["cp"])
            trestbps = int(request.form["trestbps"])
            chol = int(request.form["chol"])
            thalach = int(request.form["thalach"])
            exang = int(request.form["exang"])

            features = np.array([[age, sex, cp, trestbps, chol, thalach, exang]])
            prediction = model.predict(features)

            if prediction[0] == 1:
                prediction_text = "⚠️ High risk of Heart Disease"
            else:
                prediction_text = "✅ No Heart Disease Detected"
        except:
            prediction_text = "Error in input. Please try again."

    return render_template("predict.html", prediction=prediction_text)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)