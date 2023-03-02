from flask import Flask, jsonify, render_template, request, redirect, url_for
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request

app = Flask(__name__)
##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///date_2.db"
# Optional: But it will silence the deprecation warning in the console.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)


db.create_all()

# настроили дату
first_time = datetime.datetime.today()
last_time = first_time.strftime("%m/%d/%Y")


@app.route('/', methods=['GET', 'POST'])
def home():
    all_books = db.session.query(Book).all()
    if request.method == "POST":
        # CREATE RECORD
        new_book = Book(
            title=request.form["title"],
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("index.html", x1=all_books, x2=last_time)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    book_to_delete = Book.query.get(post_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
