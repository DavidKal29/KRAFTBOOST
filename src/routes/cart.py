from flask import Blueprint,abort,redirect,url_for,render_template,request,current_app,flash
from flask_login import current_user
from services.CartService import CartService
from werkzeug.exceptions import HTTPException

cart_bp=Blueprint('cart',__name__,url_prefix='/cart')

def client_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if not current_user.rol=='client':
        abort(401)

    else:
        return True


#Ruta del carrito
@cart_bp.route('/', methods=['GET'])
def cart():
    try:
        check=client_required()
        if check!=True:
            return check

        else:
            #Obtenemos la db
            db=current_app.config['db']

            #Capturamos los parámetros opcionales de la ruta
            action=request.args.get('action')
            id_producto=request.args.get('id_producto')

            #Dependiendo de la accion hacemos una cosa u otra
            if action and id_producto:
                if action=='add':
                    CartService.addProductCart(db,current_user.id,id_producto)

                elif action=='remove_one':
                    CartService.removeOneProductCart(db,current_user.id,id_producto)
                elif action=='remove_all':
                    CartService.removeProductCart(db,current_user.id,id_producto)
        

            #Cargamos el carrito actualizado con los productos y el subtotal
            productos=CartService.showAllProductsInCart(db,current_user.id)
            subtotal=CartService.showSumario(db,current_user.id)

            #Si el subtotal existe, lo pasamos a float(para el IVA)
            if subtotal:
                subtotal=float(subtotal)
            
            #Sino, es 0
            else:
                subtotal=0

            return render_template('cart.html',productos=productos,subtotal=subtotal)
        
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /cart')
        print(error)
        abort(404)


