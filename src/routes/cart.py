from flask import Blueprint,abort,redirect,url_for
from flask_login import current_user


cart_bp=Blueprint('cart',__name__)


@cart_bp.route('/cart',methods=['GET','POST'])
def cart():
    if current_user.is_authenticated:
        print('EL current user rol:',current_user.rol)
        if current_user.rol=='client':
            return 'Este es el carrito temporal'
        else:
            abort(401)
    
    return redirect(url_for('auth.login'))