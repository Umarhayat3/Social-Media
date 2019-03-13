# Social-Media/models.py

# IMPORTS: db from __init__.py
from config import db, json


# Class:  Bellow is the declaration of classes
class User(db.Model):
    """
    This is a user class.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)

    # :Back Reference to Post, Comment and React Classes
    post = db.relationship('Post', backref='user')
    comment = db.relationship('Comment', backref='user')
    react = db.relationship('React', backref='user')

    def profile(self):
        dct = {"profile": {
            "User Name": self.user_name,
            "Name": str(self.first_name+self.last_name),
            "Email": self.email},
            "Post": [{"content": p.content, "comments": [c.content for c in p.comment],
                      "reactions":[r.reaction for r in p.react]} for p in self.post]}

        return json.dumps(dct)


class Post(db.Model):
    """This Class is the post class that handle user's Posted Content."""
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    content = db.Column(db.String(64))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # :Back Reference to Comment and React classes
    comment = db.relationship('Comment', backref='post')
    react = db.relationship('React', backref='post')

    def info(self):
        dct = {"content": self.content, "comments": [c.content for c in self.comment],
                      "reactions":[r.reaction for r in self.react]}
        return json.dumps(dct)


class Comment(db.Model):
    """"This class handle comments on a post"""
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(64))

    def detail(self):
        dct = {"content": self.content}
        return json.dumps(dct)


class React(db.Model):
    """"This class handle Reaction on a post"""
    __tablename__ = 'reaction'
    reaction_id = db.Column(db.Integer, primary_key=True, unique=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reaction = db.Column(db.Boolean)


