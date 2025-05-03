from flask import Blueprint,redirect,request,url_for,current_app,render_template
from models.ModelProduct import ModelProduct
import math

shop_bp=Blueprint('shop',__name__)



   



#Al redirijir a shop, usaré shop.shop que es basicamente 
# el name del bluerpint y el nombre de la funcion de la ruta
@shop_bp.route('/shop', methods=['GET','POST'])
def shop():
    if request.method=='GET':
        #Marcamos los parámetros validos
        parametros_validos=['page','marca','categoria','precio']
        

        #Obtenemos el db de la app
        db=current_app.config['db']

        #Obtenemos todos los productos
        total=current_app.config['total_productos']

        #Obtenemos todas las marcas y categorias
        marcas=current_app.config['marcas']
        categorias=current_app.config['categorias']
        precios=current_app.config['precios']



        #Obtenemos los parametros de filtrado
        marca=request.args.get('marca')
        categoria=request.args.get('categoria')
        precio=request.args.get('precio')


        #Creamos un diccionario y vemos si estos valores existen en la url
        parametros={}
        
        #Variable que mirará si alguien puso algo raro en los filtros desde las rutas
        bugs=False


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
        # y si hay redirijimos a page=1 con los parametros válidos
        for i in request.args.keys():
            if i not in parametros_validos or len(request.args.getlist(i))>1:
                return redirect(url_for('shop.shop',page=1,**parametros))
            
            
        #Si hay bugs en los parametros validos redirijimos a page 1 con los parametros que si sean validos
        if bugs:
            return redirect(url_for('shop.shop',page=1,**parametros))
        
        

        print('Los parametros:',parametros)

        
        #Si no hay page, redirijimos a page 1
        if not request.args.get('page'):
            return redirect(url_for('shop.shop', page=1,**parametros))
        
        
       
        #Definimos el numero de paginas
        productos_por_pagina=12
        
        #Defino la pagina maxima(total de paginas), y redondeo al mayor por si da decimal
        pagina_maxima=math.ceil(total/productos_por_pagina)

        
        #Intento obtener el page en forma de int
        try:
            page=int(request.args['page'])

        #Caerá aquí si el page contiene letras
        except Exception as error:
            print(error)
            return redirect(url_for('shop.shop',page=1, **parametros))


         
        #Si el page es mayor a la pagina maxima, redirije a la pagina maxima
        if page>pagina_maxima:
            return redirect(url_for('shop.shop',page=pagina_maxima, **parametros))
        
        #Si es menor a 1, lo lleva a 1
        elif page<1:
            return redirect(url_for('shop.shop',page=1, **parametros))
        

        #Si porfin todo sale bien
        else:
            #Obtenemos los productos con los filtros de la paginacion
            productos=ModelProduct.mostrar_productos_paginacion(db,page,productos_por_pagina)

            return render_template('shop.html',
                                   paginas=pagina_maxima,productos=productos,
                                   page=page, parametros=parametros,
                                   marcas=marcas,categorias=categorias,precios=precios)
    
    
    elif request.method=='POST':
        #Obtenemos los parametros de los select
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
        return redirect(url_for('shop.shop',page=page,**parametros))


    