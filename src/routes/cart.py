from flask import Blueprint,abort,redirect,url_for,render_template,request,current_app
from flask_login import current_user
from services.CartService import CartService

cart_bp=Blueprint('cart',__name__,url_prefix='/cart')

def client_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if not current_user.rol=='client':
        abort(401)

    else:
        return True


@cart_bp.route('/',methods=['GET'])
def cart():
    check=client_required()
    if check!=True:
        return check
    else:
        db=current_app.config['db']

        productos_carrito=CartService.showAllProductsInCart(db,current_user.id)

        subtotal=CartService.showSumario(db,current_user.id)

        if subtotal:
            subtotal=float(subtotal)
                
        return render_template('cart.html',productos_carrito=productos_carrito,subtotal=subtotal)


@cart_bp.route('/add_product/<id_producto>',methods=['GET'])
def add_product(id_producto):
    check=client_required()
    if check!=True:
        return check
    else:
        db=current_app.config['db']

        CartService.addProductCart(db,current_user.id,id_producto)
            
        return redirect(url_for('cart.cart'))


@cart_bp.route('/removeOneProduct/<id_producto>',methods=['GET'])
def removeOneProduct(id_producto):
    check=client_required()
    if check!=True:
        return check
    else:
        db=current_app.config['db']

        CartService.removeOneProductCart(db,current_user.id,id_producto)
            
        return redirect(url_for('cart.cart'))


@cart_bp.route('/removeProduct/<id_producto>',methods=['GET'])
def removeProduct(id_producto):
    check=client_required()
    if check!=True:
        return check
    else:
        db=current_app.config['db']

        CartService.removeProductCart(db,current_user.id,id_producto)
            
        return redirect(url_for('cart.cart'))