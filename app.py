from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////workspaces/2026-12swe-at2-web-development-William-Faunt/score.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)



@app.route('/')
def index():
    return render_template('Index.html')

@app.post("/submit_score")
def submit_score():
    data = request.json

    score = Score(
        username=data["username"],
        mode=data["mode"],
        score=data["score"]
    )

    db.session.add(score)
    db.session.commit()

    return jsonify({"status": "ok"})

@app.route('/Test')
def test():
    return render_template('Test.html')

@app.route('/Leaderboard')
def leaderboard_page():
    return render_template('Leaderboard.html')

@app.get("/Leaderboard/<int:mode>")
def leaderboard(mode):
    top = Score.query.filter_by(mode=mode).order_by(Score.score.desc()).limit(10).all()
    results = [
        {"username": s.username, "score": s.score}
        for s in top
    ]
    return jsonify(results)

