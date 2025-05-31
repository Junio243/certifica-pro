import os, json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from firebase_admin import credentials, firestore, initialize_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from dotenv import load_dotenv
import qrcode
from io import BytesIO
import base64

load_dotenv()

cred = credentials.Certificate(os.getenv("FIREBASE_KEY", "firebase_key.json"))
initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "changeme")

login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    id = 1

@login_manager.user_loader
def load_user(user_id):
    return User()

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        codigo = request.form.get("codigo")
        cpf = request.form.get("cpf")
        query = db.collection("certificados")
        if codigo:
            results = query.where("codigo", "==", codigo).stream()
        else:
            results = query.where("cpf", "==", cpf).stream()
        cert = None
        for doc in results:
            cert = doc.to_dict()
        if cert:
            return render_template("resultado.html", cert=cert)
        else:
            flash("Certificado não localizado.", "danger")
    return render_template("index.html")

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        if user == os.getenv("ADMIN_USER", "admin") and password == os.getenv("ADMIN_PASS", "admin123"):
            login_user(User())
            return redirect(url_for("admin"))
        flash("Credenciais inválidas.", "danger")
    return render_template("login.html")

@app.route("/admin")
@login_required
def admin():
    certs = [doc.to_dict() for doc in db.collection("certificados").stream()]
    return render_template("admin.html", certs=certs)

@app.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/admin/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")
    if file and file.filename.endswith(".csv"):
        import csv
        reader = csv.DictReader(file.stream.read().decode("utf-8").splitlines())
        for row in reader:
            db.collection("certificados").add(row)
        flash("Upload realizado com sucesso!", "success")
    else:
        flash("Envie um arquivo CSV válido.", "danger")
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
