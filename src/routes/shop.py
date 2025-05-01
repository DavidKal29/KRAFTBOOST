from flask import Blueprint,redirect,request,url_for,current_app,render_template
from models.ModelProduct import ModelProduct
import math

shop_bp=Blueprint('shop',__name__)

#Al redirijir a shop, usaré shop.shop que es basicamente 
# el name del bluerpint y el nombre de la funcion de la ruta
@shop_bp.route('/shop')
def shop():

    #Si no hay page, redirijimos a page 1
    if not request.args.get('page'):
        return redirect(url_for('shop.shop', page=1))
    
    #Obtenemos el db de la app
    db=current_app.config['db']

    #Obtenemos el numero de productos
    try:
        
        cursor=db.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM productos')
        
        total=cursor.fetchone()
        total=total[0]
        
        cursor.close()
    except Exception as error:
        print(error)


    #Definimos el numero de paginas
    productos_por_pagina=12
    
    #Redondeo al maximo por si hay decimales
    pagina_maxima=math.ceil(total/productos_por_pagina)

    #Obtengo el page
    page=int(request.args['page'])

    #Si se pasa, lo lleva al maximo permitido
    if page>pagina_maxima:
        return redirect(url_for('shop.shop', page=pagina_maxima))
    
    #Si no llega, lo lleva al minimo
    elif page<1:
        return redirect(url_for('shop.shop', page=1))
    
    else:
        #Obtenemos los productos con los filtros de la paginacion
        productos=ModelProduct.mostrar_productos_paginacion(db,page,productos_por_pagina)

        return render_template('shop.html')