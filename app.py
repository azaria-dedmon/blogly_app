"""Blogly application."""

from flask import Flask, render_template, session, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def redirect_users():
    """List users"""
    users = User.query.all()
    return render_template("user_listing.html", users=users)

@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("user_listing.html", users=users)

@app.route("/users/new")
def add_users():
    return render_template("new_user.html")

@app.route("/users/new", methods=['POST'])
def process_users():
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    img = request.form["img"]

    user = User(first_name=first_name, last_name=last_name, img=img)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=['POST'])
def process_user_edit(user_id):
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    img = request.form["img"]

    user = User.query.get(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.img = img
    db.session.commit()
    
    return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')


