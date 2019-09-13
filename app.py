import os
from forms import AddForm, DelForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Declare the application
app = Flask(__name__)

# the base file path
basedir = os.path.dirname(__file__)

# the various configurations of the application
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db definations
db = SQLAlchemy(app)
Migrate(app, db)

# The model for the database


class Puppy(db.Model):
    __tablename__ = 'puppies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Puppy name is {self.name}"

# view functions
@app.route('/')
def index():
    url = 'index'
    return render_template('index.html', url=url)


@app.route('/add', methods=['GET', 'POST'])
def add_pup():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    url = 'add_pup'
    return render_template('add.html', form=form, url=url)


@app.route('/list')
def list_pup():
    puppies = Puppy.query.all()
    url = 'list_pup'
    return render_template('list.html', puppies=puppies, url=url)


@app.route('/delete', methods=['GET', 'POST'])
def del_pup():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    url = 'del_pup'
    return render_template('delete.html', form=form, url=url)


if __name__ == '__main__':
    app.run(debug=True)
