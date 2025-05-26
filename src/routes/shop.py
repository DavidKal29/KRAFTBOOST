from flask import Blueprint,redirect,request,url_for,current_app,render_template,abort
from models.ModelProduct import ModelProduct
import math
import unidecode

shop_bp=Blueprint('shop',__name__)

#Importamos el metodo para manejar la paginacion, filtros y buscador del producto
from utils.PaginationProductsManager import productos_paginacion

#Ruta de la tienda
@shop_bp.route('/shop', methods=['GET','POST'])
def shop():
    try:
        return productos_paginacion('shop.shop','shop.html',admin=None)
        
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /shop')
        print(error)
        abort(404)