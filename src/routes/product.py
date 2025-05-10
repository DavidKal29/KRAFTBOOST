from flask import Blueprint,redirect,request,url_for,current_app,render_template


product_bp=Blueprint('product',__name__)


@product_bp.route('/product/<id>')
def product(id):


    return 'Pagina del producto. Aqui el id:{}'.format(id)