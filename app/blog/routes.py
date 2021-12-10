from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from .forms import CreatePostForm

from app.models import Post

# create instance of blueprint
blog = Blueprint('blog', __name__, template_folder='blog_templates')

from app.models import db

@blog.route('/')
def blogHome():
    posts = Post.query.all()
    return render_template('blog.html', posts = posts)

@blog.route('/posts/create', methods = ["GET","POST"])
@login_required
def createPost():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            
            title = form.title.data
            image = form.image.data
            content = form.content.data

            # create instance new post
            post = Post(title, image, content, current_user.id)
            # add instance to databse
            db.session.add(post)
            # commit to databse
            db.session.commit()

            return redirect(url_for('home'))
    return render_template('createpost.html', form = form)