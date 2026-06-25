from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todoz.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

class Todoz(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.Sno} - {self.title}"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todoz = Todoz(title=title, desc=desc)
        db.session.add(todoz)
        db.session.commit()
    alltodo = Todoz.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method=="POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todoz = Todoz.query.filter_by(Sno=sno).first()
        todoz.title = title
        todoz.desc = desc
        db.session.commit()
        return redirect("/")

    todoz = Todoz.query.filter_by(Sno=sno).first()
    return render_template("update.html", todoz=todoz)

@app.route("/delete/<int:sno>")
def delete(sno):
    todoz = Todoz.query.filter_by(Sno=sno).first()
    db.session.delete(todoz)
    db.session.commit()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("/about.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)