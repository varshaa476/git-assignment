from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = "mongodb+srv://varshaprabhudev03_db_user:Varsha2026db@cluster0.7nghuwf.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["assignment3_db"]
collection = db["submissions"]

# Task 1: /api route - reads from backend file, returns JSON
@app.route("/api")
def api():
    with open("data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

# Frontend form
@app.route("/")
def index():
    return render_template("index.html")

# Task 2: Form submission -> insert into MongoDB
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            return render_template("index.html", error="Name and Email are required.")

        collection.insert_one({"name": name, "email": email})
        return redirect(url_for("success"))

    except PyMongoError as e:
        return render_template("index.html", error=str(e))

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/todo")
def todo():
    return render_template("todo.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
