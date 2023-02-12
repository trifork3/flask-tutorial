from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

N_CHARACTER_LIMIT = 240

app = Flask(__name__, template_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Concept: classes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(N_CHARACTER_LIMIT))
    date = db.Column(db.DateTime(timezone=True))

@app.route("/")
def index():
    notes = Note.query.all()
    return render_template("index.html", notes_list=notes)

@app.route("/add", methods=[ 'POST' ])
def add():
    text = request.form.get('text')
    added = Note(text=text, date=datetime.datetime.now())
    db.session.add(added)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    deleted = Note.query.filter_by(id=id).first()
    db.session.delete(deleted)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)