from flask import Blueprint, render_template, redirect, url_for, request
from flask.json import jsonify
from flask_login import current_user, login_required

from app.apiauthhelper import token_required

from .forms import CreatePostForm, UpdatePostForm

from app.models import Post, Pokemon, Ability

# create instance of blueprint
blog = Blueprint('blog', __name__, template_folder='blog_templates')

from app.models import db

import requests as r

@blog.route('/')
def blogHome():
    posts = Post.query.all()
    return render_template('blog.html', posts = posts)

@blog.route('/pokebikes')
def pokeBikes():
    data = r.get('https://pokeapi.co/api/v2/item/bicycle/')
    my_data = data.json()
    bikes = [dict['name'] for dict in my_data['names']]
    my_img = my_data['sprites']['default']
    return render_template('pokebikes.html', bikes=bikes, my_img=my_img)

@blog.route('/blog/<int:id>')
def individualPost(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        return redirect(url_for('blog.blogHome'))
    return render_template('individualpost.html', p = post)

@blog.route('/posts/delete/<int:id>', methods = ["POST"])
@login_required
def deletePost(id):
    post = Post.query.filter_by(id=id).first()
    if post.user_id != current_user.id:
        return redirect(url_for('blog.blogHome'))
    
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.blogHome'))

@blog.route('/posts/update/<int:id>', methods = ["GET","POST"])
@login_required
def updatePost(id):
    post = Post.query.filter_by(id=id).first()
    if post.user_id != current_user.id:
        return redirect(url_for('blog.blogHome'))


    form = UpdatePostForm()
    if request.method == "POST":
        if form.validate():
            
            title = form.title.data
            image = form.image.data
            content = form.content.data

            if not title:
                title = post.title
            if not image:
                image = post.image
            if not content:
                content = post.content

            # Updating the Post object
            post.title = title
            post.image = image
            post.content = content

            # commit to databse
            db.session.commit()

            return redirect(url_for('blog.individualPost', id=id))
    return render_template('updatepost.html', form = form)

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

@blog.route('/search/pokemon', methods = ['POST'])
def searchPokemon():
    
    if request.method == "POST":
        my_pokemon = request.form['poke']
        data = r.get(f'https://pokeapi.co/api/v2/pokemon/{my_pokemon}')
        if data.status_code == 200:
            my_data = data.json()

            pokemon = {
                'name': '',
                'image': '',
                'abilities': []
            }

            for ability in my_data['abilities']:
                pokemon['abilities'].append(ability['ability']['name'])
            pokemon['name'] = my_data['name']
            pokemon['image'] = my_data['sprites']['other']['dream_world']['front_default']
            id = my_data['id']

            my_pokemon = Pokemon.query.filter_by(id=id)
            if not my_pokemon:
            # instantiate Pokemon and Ability
                my_pokemon = Pokemon(id, pokemon['name'], pokemon['image'])
                db.session.add(my_pokemon)
                if len(pokemon['abilities']) == 2:
                    ability2 = Ability(pokemon['abilities'][1], id)
                    ability1 = Ability(pokemon['abilities'][0], id)
                    db.session.add(ability2)
                    db.session.add(ability1)
                elif len(pokemon['abilities']) == 1:
                    ability1 = Ability(pokemon['abilities'][1], id)
                    db.session.add(ability1)
                db.session.commit()
                

            # grab information and pass to a template.
            return render_template('pokemon.html', pokemon = pokemon)
        else:
            pokemon = ''
            return render_template('pokemon.html', pokemon = pokemon)
    return {'hi': 'there'}




@blog.route('/api/posts')
def apiBlogPosts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])