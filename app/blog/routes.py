from flask import Blueprint
from flask import render_template

# create instance of blueprint
blog = Blueprint('blog', __name__, template_folder='blog_templates')

@blog.route('/blog/main')
def blogHome():
    return render_template('blog.html')