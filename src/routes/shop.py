from flask import Blueprint,redirect,request,url_for,current_app,render_template
from models.ModelProduct import ModelProduct
import math

shop_bp=Blueprint('shop',__name__)


#Al redirijir a shop, usaré shop.shop que es basicamente 
# el name del bluerpint y el nombre de la funcion de la ruta
@shop_bp.route('/shop', methods=['GET','POST'])
def shop():
    if request.method=='GET':
        #Variable que mirará si alguien puso algo raro en los filtros desde las rutas
        bugs=False
        
        #Marcamos los parámetros validos
        parametros_validos=['page','marca','categoria','precio','orden']
        
        #Obtenemos el db de la app
        db=current_app.config['db']

        #Obtenemos las marcas, categorias y precios
        marcas=current_app.config['marcas']
        categorias=current_app.config['categorias']
        precios=current_app.config['precios']


        #Obtenemos los parametros de filtrado
        orden=request.args.get('orden')
        marca=request.args.get('marca')
        categoria=request.args.get('categoria')
        precio=request.args.get('precio')


        #Creamos un diccionario y vemos si estos valores existen en la url
        parametros={}
        

        #Si la marca existe, es un numero y esta en el rango de len(marcas), 
        # se añade a parametros, sino se activa a True los bugs
        if marca:
            if not marca.isdigit():
                bugs=True
            
            elif int(marca)>len(marcas) or int(marca)<1:
                bugs=True
            
            else:
                parametros['marca']=int(marca)
        
        #Si la categoria existe, es un numero y esta en el rango de len(categorias), 
        # se añade a parametros, sino se activa a True los bugs
        if categoria:
            if not categoria.isdigit():
                bugs=True
            
            elif int(categoria)>len(categorias) or int(categoria)<1:
                bugs=True
            
            else:
                parametros['categoria']=int(categoria)

        #Si precio existe y esta en los rangos correctos se añade a paramtros sino bugs True
        if precio:
            if precio in precios:
                parametros['precio']=precio
            else:
                bugs=True

        
        #Miramos si no hay parametros que no deberian estar o hay parametros duplicados 
        for i in request.args.keys():
            if i not in parametros_validos or len(request.args.getlist(i))>1:
                bugs=True
        

        #Si el orden no existe, es un numero, o tiene un valor invalido, filtramos por los mas recientes
        if not orden or not orden.isalpha() or orden not in ['masRecientes','topVentas']:
            orden='masRecientes'
            bugs=True

        
        #Si no hay page, redirijimos a page 1
        if not request.args.get('page'):
            bugs=True
            page=1
        
        
        #Definimos el numero de paginas
        productos_por_pagina=12

        #Intento obtener el page en forma de int
        try:
            page=int(request.args['page'])

        #Caerá aquí si el page contiene letras
        except Exception as error:
            print(error)
            page=1
            bugs=True

        #Comprobamos por primera vez si no hay bugs
        if bugs:
            return redirect(url_for('shop.shop',page=page,orden=orden,**parametros))
        
        
        #Obtenemos el numero total de productos segun los parametros
        total=ModelProduct.mostrar_contador_productos(db,parametros)
        
        

        #Si el numero total es un numero establecemos la pagina 
        # maxima a ese numero entre los productos por pagina 
        # redondeando al mayor por si da 1.5 o cosas asi, sino 1
        if total:
            pagina_maxima=math.ceil(total/productos_por_pagina)
        else:
            pagina_maxima=1

            
        #Si el page es mayor a la pagina maxima, redirije a la pagina maxima
        if page>pagina_maxima:
            page=pagina_maxima
            bugs=True
            
        #Si es menor a 1, lo lleva a 1
        elif page<1:
            page=1
            bugs=True
            

        #Comprobamos por segunda vez si hay bugs
        if bugs:
            return redirect(url_for('shop.shop',page=page,orden=orden,**parametros))

        #Si porfin todo sale bien
        else:
            #Obtenemos los productos con los filtros de la paginacion
            productos=ModelProduct.mostrar_productos_paginacion(db,page,productos_por_pagina,orden,parametros)
        

        return render_template('shop.html',
                                paginas=pagina_maxima,productos=productos,
                                page=page, parametros=parametros,
                                marcas=marcas,categorias=categorias,precios=precios,orden=orden)
        
    
    
    elif request.method=='POST':
        search=request.form.get('search')
        print('El search:',search)


        #Obtenemos los parametros de los select
        orden=request.form.get('select_orden')
        marca=request.form.get('select_marca')
        categoria=request.form.get('select_categoria')
        precio=request.form.get('select_precio')
        
        #Obtenemos el page
        page=request.args.get('page')

        #Lo mismo, creamos un diccionario y vemos si los parametros han sido seleccionados
        parametros={}

        #Validamos que no sean values 0
        if marca!='0':
            parametros['marca']=marca
        
        if categoria!='0':
            parametros['categoria']=categoria

        if precio!='0':
            parametros['precio']=precio


        #Redirijimos con los parametros
        return redirect(url_for('shop.shop',page=page,orden=orden,**parametros))