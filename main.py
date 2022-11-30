from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///books.db'
db = SQLAlchemy()
db.init_app(app)
Bootstrap(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


class BookForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    book_author = StringField('Book Author', validators=[DataRequired()])
    rating = StringField('Rating (out of 10)', validators=[DataRequired()])
    submit = SubmitField('Add Book')


class EditForm(FlaskForm):
    new_rating = StringField('Rating (out of 10)', validators=[DataRequired()])
    submit = SubmitField('Change Rating')


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route('/delete')
def delete():
    # DELETE RECORD
    print("hello")
    book_id = request.args.get('identifier')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BookForm()
    if form.validate_on_submit():
        print("True")
        new_book = Book(title=form.book_name.data, author=form.book_author.data, rating=form.rating.data)
        with app.app_context():
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditForm()
    if form.validate_on_submit():
        # UPDATE RECORD
        book_id = request.args.get('identifier')
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = form.new_rating.data
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('identifier')
    book_selected = Book.query.get(book_id)
    return render_template("edit.html", form=form, book=book_selected)


if __name__ == "__main__":
    app.run(debug=True)
