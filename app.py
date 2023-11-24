from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators
from flask_migrate import Migrate
from flask_login import UserMixin



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Content Security Policy headers
csp_headers = {
    'default-src': '\'self\'',        # Allow resources from the same origin (self)
    'script-src': '\'self\'',         # Allow inline scripts and scripts from the same origin
}


# Defining the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # Defining the relationship with Comment model
    post_comments = db.relationship('Comment', backref='post_association', cascade='all, delete-orphan', lazy=True)


# Defining a form for creating posts
class PostForm(FlaskForm):
    title = StringField('Title', render_kw={"placeholder": "Enter the title"}, validators=[validators.DataRequired()])
    content = TextAreaField('Content', render_kw={"placeholder": "Enter the content"}, validators=[validators.DataRequired()])
    submit = SubmitField('Create Post')

#Defining the comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

#Defining a form for creating comments
class CommentForm(FlaskForm):
    content = TextAreaField('Comment', render_kw={"placeholder": "Enter your comment"}, validators=[validators.DataRequired()])
    submit = SubmitField('Submit Comment')

# Routes for creating posts, deleting posts, viewing posts, etc.
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    form = CommentForm()
    if post:
        if form.validate_on_submit():
            content = form.content.data
            new_comment = Comment(content=content, post=post)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added successfully!', 'success')
        return render_template('post.html', post=post, form=form)
    else:
        return 'Post not found', 404

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)

    if form.validate_on_submit():
        content = form.content.data
        new_comment = Comment(content=content, post=post)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')

    return redirect(url_for('post', post_id=post_id))


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('create.html', form=form)


@app.after_request
def add_csp_headers(response):
    # Add Content Security Policy headers to the response
    for header, value in csp_headers.items():
        response.headers[header] = value
    return response


@app.route('/clear')
def clear():
    db.session.query(Comment).delete()
    db.session.commit()
    db.session.query(Post).delete()
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)