from flask import Blueprint,redirect,request,url_for,current_app,render_template,abort
from models.ModelProduct import ModelProduct
from flask_login import current_user


product_bp=Blueprint('product',__name__)

#Ruta del producto
@product_bp.route('/product/<id>')
def product(id):

    #Obtenemos la db de app.config
    db=current_app.config['db']

    try:
        #Intentamos pasar el id a entero para evitar que nos pongan strings en la ruta
        id=int(id)

        #Hacemos la consulta a través del método mostrar_producto_info
        producto=ModelProduct.mostrar_producto_info(db,id)

        #Vemos si está en favoritos el producto
        if current_user.is_authenticated:
            favorito=ModelProduct.checkFavorite(db,current_user.id,id)
        else:
            favorito=False

        #Si no hay producto, mandamos al 404
        if not producto:
            abort(404)
        
        #Si está, cargamos el html con los datos del producto
        else:

            return render_template('product.html',id=id,producto=producto,favorito=favorito)
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /product')
        print(error)
        abort(404)
