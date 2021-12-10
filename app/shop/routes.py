from flask import Blueprint, render_template, redirect, url_for, jsonify

from app.models import Product

# create instance of blueprint
shop = Blueprint('shop', __name__, template_folder='shop_templates')

from app.models import db

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