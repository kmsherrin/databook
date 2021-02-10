from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship('Post', backref='user', lazy="dynamic")
    likes = db.relationship('Like', backref='user', lazy="dynamic")
    comments = db.relationship('Comment', backref='user', lazy="dynamic")
    comments_reply = db.relationship('CommentReply', backref='user', lazy="dynamic")
    
    tags = db.relationship('Tag', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.image_file})'

    def get_reset_token(self, expires_seconds=500):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = Like(user_id=self.id, author_id=post.user_id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            Like.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return Like.query.filter(Like.user_id == self.id, Like.post_id == post.id).count() > 0
    
    def set_name(self, new_name):
        self.name = new_name
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, index=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    content = db.Column(db.Text, nullable=False)
    
    category = db.Column(db.String(100), nullable=False, default="General")

    edited = db.Column(db.Boolean, nullable=False, default=False)
    edited_date = db.Column(db.DateTime, nullable=True)

    version = db.Column(db.Integer, nullable=False, default=1)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    likes = db.relationship('Like', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', backref='post', lazy='dynamic')

    def __repr__(self):
            return f'Post({self.title}, {self.date_posted})'

    def number_of_likes(self):
        return Like.query.filter(Like.post_id == self.id).count()
    
    def get_author(self):
        return self.user.username

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    abstract = db.Column(db.Text, nullable=False)

    category = db.Column(db.String, nullable=False, default="General")

    #dataset_files = db.relationship('DatasetLocation', backref='dataset', lazy='dynamic')

class DatasetLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    href = db.Column(db.String, nullable=False)
    dataset_id = db.Column(db.Integer, nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def get_popular_tags(self):
        return Tag.query(func.count(self.id).label('freq')).group_by(self.tag).order_by(desc('freq')).limit(5)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, default=0)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    comment_replies = db.relationship('CommentReply', backref='comment', lazy='dynamic')

    def get_comment_replies(self):
        return CommentReply.query.filter(CommentReply.comment_id == self.id).all()

class CommentLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class CommentReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

