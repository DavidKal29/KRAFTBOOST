from flask import Blueprint,render_template,current_app
from models.ModelProduct import ModelProduct
from models.ModelCategory import ModelCategory

home_bp=Blueprint('home',__name__)

@home_bp.route('/')
def home():
    #Obtenemos la db de app
    db=current_app.config['db']

    #Creamos las diferentes variables con los datos de la db
    productos_nuevos=ModelProduct.mostrar_productos(db,'id')

    top_ventas=ModelProduct.mostrar_productos(db,'ventas')

    categorias=ModelCategory.mostrar_categorias(db)


    return render_template('home.html',productos_nuevos=productos_nuevos,top_ventas=top_ventas,categorias=categorias)