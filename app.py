import os
import uuid
import markdown
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# Run project
# export FLASK_ENV=development
# export FLASK_APP=app.py
# flask run

# Load environment variables from .env file
load_dotenv()

# Create a Flask Instance
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    posts = db.relationship('Post', backref='postsSet')

    def __repr__(self):
        return f"<User {self.name}>"


class Post(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"


class PostForm(FlaskForm):
    title = StringField("Post Title", validators=[DataRequired()])
    content = StringField(validators=[Length(max=1024)])
    submit = SubmitField("Submit")


@app.route("/")
def index():
    posts = Post.query.limit(3).all()
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/posts/<post_id>", methods=['GET'])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    html_content = markdown.markdown(post.content)
    return render_template("post.html", content=html_content)


@app.route("/posts", methods=['GET'])
def posts():
    posts = Post.query.limit(3).all()
    return render_template("posts.html", posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
