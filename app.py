"""Blogly application."""

from flask import Flask, render_template, session, redirect, request
from models import db, connect_db, User, Post, Tag, Post_Tag
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
    
    posts = user.posts
    return render_template("user_detail.html", user=user, posts=posts)


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


@app.route("/users/<int:user_id>/posts/new")
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def process_add_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist('tag-name')
    user = User.query.get_or_404(user_id)   

    post = Post(title=title, content=content, user_table=user.id)

    db.session.add(post)
    db.session.commit()

    for tag in tags:
        tag = Post_Tag(post_id=post.id, tag_id=tag.id)

        db.session.add(tag)
        db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.users
 
    return render_template("show_post.html", post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.users
    tags = Tag.query.all()
    return render_template("edit_post.html", user=user, post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def process_post_edit(post_id):
    title = request.form["title"]
    content = request.form["content"]
    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.users

    delete_post = Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()

    return render_template("get_tag.html", tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tags = Tag.query.get_or_404(tag_id)

    return render_template("show_tag.html", tags=tags)


@app.route('/tags/new')
def make_new_tag():

    return render_template("add_tag.html")


@app.route('/tags/new', methods=['POST'])
def process_make_new_tag():
    tag = request.form['tag-name']

    tag_name = Tag(name=tag)

    db.session.add(tag_name)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit_tag.html", tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def process_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag_name = request.form['tag-name']

    tag.name = tag_name

    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    delete_tag_name = Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect('/tags')