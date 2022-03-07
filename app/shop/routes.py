from flask import Blueprint, json, render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user

from app.models import Cart, Product
from .forms import CreateProductForm

import os
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

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


@shop.route('/stripe/createCheckoutSession', methods=['POST'])
def createStripeCheckout():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                "price": "price_1KGuYsDTfh3G5wtDNvF9UBgu",
                "quantity": 1
            }],
            mode='subscription',
            success_url='http://localhost:3000/',
            cancel_url='http://localhost:3000/cart'
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)

@shop.route('/api/getCart', methods=['POST'])
def getCart():
    data = request.json
    user_id = data['user_id']
    cart = Cart.query.filter_by(user_id=user_id)
    return jsonify([Product.query.filter_by(id=instance.product_id).first().to_dict() for instance in cart])
        

@shop.route('/api/addToCart', methods=['POST'])
def addToCart():
    data = request.json
    print(data)
    product_id = data['product_id']
    user_id = data['user_id']
    newCartItem = Cart(user_id, product_id)
    db.session.add(newCartItem)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': f'You have successfully added item {product_id} to your cart'
    })

@shop.route('/api/removeFromCart', methods=['POST'])
def removeFromCart():
    data = request.json
    user_id = data['user_id']
    product_id = data['product_id']
    cartItem = Cart.query.filter_by(user_id=user_id).filter_by(product_id=product_id).first()
    if cartItem:
        db.session.delete(cartItem)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'You have successfully removed item {product_id} to your cart'
            })
    return jsonify({
        'status': 'error',
        'message': f'User {user_id} does not have product {product_id} in their cart'
        })

@shop.route('/api/emptyCart', methods=['POST'])
def emptyCart():
    data = request.json
    user_id = data['user_id']
    cart = Cart.query.filter_by(user_id=user_id).all()
    if cart:
        db.session.delete(cart)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f"You have successfully removed all items from {user_id}'s cart to your cart"
            })
    return jsonify({
        'status': 'error',
        'message': f"There are no items in {user_id}'s cart to remove."
        })



