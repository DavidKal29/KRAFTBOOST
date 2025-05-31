from flask import Blueprint,render_template,current_app,abort
from models.ModelProduct import ModelProduct
from models.ModelCategory import ModelCategory

home_bp=Blueprint('home',__name__)

#Ruta del home
@home_bp.route('/')
def home():
    try:
        #Obtenemos la db de app
        db=current_app.config['db']

        #Obtenemos los productos nuevos
        productos_nuevos=ModelProduct.mostrar_productos(db,'id')

        #Obtenemos los top ventas
        top_ventas=ModelProduct.mostrar_productos(db,'ventas')

        #Obtenemos las categorias
        categorias=ModelCategory.mostrar_categorias(db)

        #Devolvemos el home
        return render_template('home.html',productos_nuevos=productos_nuevos,top_ventas=top_ventas,categorias=categorias)
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /home')
        print(error)
        abort(404)
