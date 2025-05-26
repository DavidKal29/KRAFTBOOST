from flask import Blueprint,abort,redirect,url_for,render_template,request,current_app,flash
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


@cart_bp.route('/', methods=['GET'])
def cart():
    check=client_required()
    if check!=True:
        return check

    else:
        #Obtenemos la db
        db=current_app.config['db']

        #Capturamos los parámetros opcionales de la query
        action=request.args.get('action')
        id_producto=request.args.get('id_producto')

        #Dependiendo de la accion hacemos una cosa u otra
        if action and id_producto:
            if action=='add':
                agregado=CartService.addProductCart(db,current_user.id,id_producto)

                #Dependiendo de la respuesta, manda un mensaje u otro
                if agregado:
                    if agregado=='Sin stock':
                        flash('Sin Stock')
                    else:
                        if '/product/' in request.referrer:
                            flash('Añadido al carrito')
                
                else:
                    flash('Error al añadir al carrito')

                #Si venimos de la apgina del product, que nos redirija ahi
                if '/product/' in request.referrer:
                    return redirect(request.referrer)

            elif action=='remove_one':
                CartService.removeOneProductCart(db,current_user.id,id_producto)
            elif action=='remove_all':
                CartService.removeProductCart(db,current_user.id,id_producto)

            

        #Cargamos el carrito actualizado
        productos=CartService.showAllProductsInCart(db,current_user.id)
        subtotal =CartService.showSumario(db,current_user.id)

        if subtotal:
            subtotal=float(subtotal)
        
        else:
            subtotal=0

        return render_template('cart.html',productos=productos,subtotal=subtotal)


