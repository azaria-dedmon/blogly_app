"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(10),
                     nullable=False,
                     unique=False)
    last_name = db.Column(db.String(10),
                          nullable=False,
                          unique=False)
    img = db.Column(db.Text)


    posts = db.relationship('Post', backref="users", cascade = "all, delete-orphan")


class Post(db.Model):
    """Blog posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(25),
                      nullable=False)
    content = db.Column(db.String(500),
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           default=db.func.current_timestamp())
    user_table = db.Column(db.Integer, 
                           db.ForeignKey('users.id',
                                         ondelete='CASCADE'))

    tags = db.relationship('Tag', secondary="post_tags", backref="posts")

class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    name = db.Column(db.String,
                        unique=True)
    
 

class Post_Tag(db.Model):

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'), primary_key=True)
    
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'), primary_key=True)

