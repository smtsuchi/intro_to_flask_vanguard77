from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user

from app.models import Product
from .forms import CreateProductForm

# create instance of blueprint
shop = Blueprint('shop', __name__, template_folder='shop_templates')

from app.models import db

@shop.route('/products/create', methods = ["GET","POST"])
@login_required
def createProduct():
    if current_user.is_admin:
        form = CreateProductForm()
        if request.method == "POST":
            if form.validate():
                
                name = form.name.data
                price = form.price.data
                image = form.image.data
                description = form.description.data

                # create instance new post
                product = Product(name, price, image, description)
                # add instance to databse
                db.session.add(product)
                # commit to databse
                db.session.commit()

                return redirect(url_for('home'))
        return render_template('createproduct.html', form = form)
    else:
        return redirect(url_for('blog.blogHome'))

@shop.route('/shop')
def allProducts():
    products = Product.query.all()
    return render_template('shop.html', products = products)

@shop.route('/shop/<int:id>')
def individualProduct(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return redirect(url_for('shop.allProducts'))
    return render_template('product.html', p = product)

    

@shop.route('/api/shop/products')
def allProductsAPI():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@shop.route('/api/shop/<int:id>')
def individualProductAPI(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify('none')
    return jsonify(product.to_dict())