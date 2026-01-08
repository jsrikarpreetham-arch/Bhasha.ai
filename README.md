# Bhasha.ai
We are building an AI Tone Corrector is a student-built project that uses modern AI tools to analyze and improve the tone of written text. The main goal of this system is to help users rewrite sentences in a more polite, professional, friendly, or confident manner without changing the original meaning. It works by understanding the context,emotion.

bhasha-ai/
│
├── app.py
├── database.py
├── models.py
├── auth.py
├── ai.py
├── requirements.txt
└── bhasha.db

import sqlite3

def get_db():
    conn = sqlite3.connect("bhasha.db")
    conn.row_factory = sqlite3.Row
    return conn

from database import get_db

def init_db():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS plans (
        user_id INTEGER,
        plan TEXT,
        usage INTEGER,
        last_reset TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        emotion TEXT,
        response TEXT,
        created_at TEXT
    )
    """)

    db.commit()
    db.close()

    from transformers import pipeline

emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

rewrite_model = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def rewrite(text, instruction):
    prompt = f"{instruction}:\n{text}"
    return rewrite_model(prompt, max_length=200)[0]["generated_text"]

from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

def create_user(email, password):
    db = get_db()
    cur = db.cursor()

    hashed = generate_password_hash(password)
    cur.execute(
        "INSERT INTO users (email,password) VALUES (?,?)",
        (email, hashed)
    )
    user_id = cur.lastrowid

    cur.execute(
        "INSERT INTO plans VALUES (?,?,?,date('now'))",
        (user_id, "FREE", 0)
    )

    db.commit()
    db.close()
    return user_id

def verify_user(email, password):
    db = get_db()
    cur = db.cursor()

    user = cur.execute(
        "SELECT * FROM users WHERE email=?", (email,)
    ).fetchone()

    db.close()

    if user and check_password_hash(user["password"], password):
        return user["id"]
    return None

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import date
from database import get_db
from models import init_db
from ai import rewrite, emotion_model
from auth import create_user, verify_user

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

init_db()

# -------- AUTH ----------
@app.route("/auth", methods=["POST"])
def auth():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user_id = verify_user(email, password)
    if not user_id:
        user_id = create_user(email, password)

    return jsonify({"user_id": user_id})

# -------- EMAIL ----------
@app.route("/email", methods=["POST"])
def email():
    data = request.json
    user_id = data.get("user_id")
    text = data.get("text")

    improved = rewrite(text, "Write a professional business email")

    return jsonify({"result": improved})

# -------- TONE ----------
@app.route("/tone", methods=["POST"])
def tone():
    data = request.json
    text = data.get("text")

    emotion = emotion_model(text)[0]["label"]
    improved = rewrite(text, "Rewrite calmly and professionally")

    return jsonify({
        "emotion": emotion,
        "improved_text": improved
    })

if __name__ == "__main__":
    app.run(debug=False)















