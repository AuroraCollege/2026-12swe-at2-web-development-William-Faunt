from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///score.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(20), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html') # type: ignore

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

@app.get("/leaderboard")
def leaderboard(mode):
    top = Score.query.filter_by(mode=mode).order_by(Score.score.desc()).limit(10)
    results = [
        {"username": s.user.username, "score": s.score}
        for s in top
    ]
    return jsonify(results)
