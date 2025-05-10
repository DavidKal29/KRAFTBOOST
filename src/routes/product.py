from flask import Blueprint,redirect,request,url_for,current_app,render_template


product_bp=Blueprint('product',__name__)


@product_bp.route('/product/<id>')
def product(id):


    return render_template('product.html',id=id)