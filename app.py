from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.secret_key = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reaction.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

@app.post("/register")
def register():
    data = request.json
    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(username=data["username"], password_hash=hashed)
    db.session.add(user)
    db.session.commit()
    return jsonify({"status": "ok"})
@app.post("/login")

def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password_hash, data["password"]):
        session["user_id"] = user.id
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 401

@app.post("/submit_score")
def submit_score():
    if "user_id" not in session:
        return jsonify({"error": "not logged in"}), 403

    data = request.json
    score = Score(
        user_id=session["user_id"],
        mode=data["mode"],
        score=data["score"]
    )
    db.session.add(score)
    db.session.commit()
    return jsonify({"status": "ok"})

@app.get("/leaderboard/<int:mode>")
def leaderboard(mode):
    top = Score.query.filter_by(mode=mode).order_by(Score.score.desc()).limit(10)
    results = [
        {"username": s.user.username, "score": s.score}
        for s in top
    ]
    return jsonify(results)
