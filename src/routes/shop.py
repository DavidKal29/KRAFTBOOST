from flask import Blueprint,render_template,current_app

shop_bp=Blueprint('shop',__name__)

@shop_bp.route('/shop')
def home():


    return 'Esta es la ruta de la tienda'