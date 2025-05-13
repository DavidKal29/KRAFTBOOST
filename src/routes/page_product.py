from flask import Blueprint,redirect,request,url_for,current_app,render_template,abort
from models.ModelProduct import ModelProduct


product_bp=Blueprint('product',__name__)


@product_bp.route('/product/<id>')
def product(id):

    db=current_app.config['db']

    try:
        #Intentamos pasar el id a entero para evitar que nos pongan strings en la ruta
        id=int(id)

        #Hacemos la consulta a través del método mostrar_producto_info
        producto=ModelProduct.mostrar_producto_info(db,id)

        #Si no hay producto, mandamos al 404
        if not producto:
            abort(404)
        
        #Si está, cargamos el html con los datos del producto
        else:

            return render_template('product.html',id=id,producto=producto)
    
    #Cualquier error siginifca que no existe tal producto, asique 404 tambien
    except Exception as err:
        print(err)
        abort(404)