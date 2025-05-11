from flask import Blueprint,redirect,request,url_for,current_app,render_template
from models.ModelProduct import ModelProduct


product_bp=Blueprint('product',__name__)


@product_bp.route('/product/<id>')
def product(id):

    db=current_app.config['db']

    producto=ModelProduct.mostrar_producto_info(db,id)

    return render_template('product.html',id=id,producto=producto)