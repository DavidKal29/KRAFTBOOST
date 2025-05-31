from flask import request,render_template,redirect,url_for,abort,current_app
import unidecode
import math
from models.ModelProduct import ModelProduct

def productos_paginacion(ruta,template,admin):
    try:
        if request.method=='GET':
            #Variable que mirará si alguien puso algo raro en los filtros desde las rutas
            bugs=False

            #Marcamos los parámetros validos
            parametros_validos=['page','marca','categoria','precio','orden','search']

            #Obtenemos el db de la app
            db=current_app.config['db']

            #Obtenemos las marcas, categorias y precios de app
            marcas=current_app.config['marcas']
            categorias=current_app.config['categorias']
            precios=current_app.config['precios']


            #Obtenemos los parametros de filtrado
            orden=request.args.get('orden')
            search=request.args.get('search')
            marca=request.args.get('marca')
            categoria=request.args.get('categoria')
            precio=request.args.get('precio')


            #Creamos un diccionario y vemos si estos valores existen en la url
            parametros={}


            #Si el search existe y no es vacio,lo añadimos y au
            if search=='':
                bugs=True
                search=None

            elif search:
                search=search.strip()
                search=search.lower()
                search=' '.join(search.split())
                search=unidecode.unidecode(search)
                parametros['search']=search
                    


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
                return redirect(url_for(ruta,page=page,orden=orden,**parametros))


            #Obtenemos el numero total de productos segun los parametros
            total=ModelProduct.mostrar_contador_productos(db,parametros,categorias,admin)


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
                return redirect(url_for(ruta,page=page,orden=orden,**parametros))

            #Si porfin todo sale bien
            else:
                #Obtenemos los productos con los filtros de la paginacion
                productos=ModelProduct.mostrar_productos_paginacion(db,page,productos_por_pagina,orden,parametros,categorias,admin)


            return render_template(template,
                                    paginas=pagina_maxima,productos=productos,
                                    page=page, parametros=parametros,
                                    marcas=marcas,categorias=categorias,precios=precios,orden=orden)



        elif request.method=='POST':
            #Lo mismo, creamos un diccionario y vemos si los parametros han sido seleccionados
            parametros={}

            #Obtenemos el search del formulario
            search=request.form.get('search')


            #Si está la metemos en los parametros
            if not  search:
                search=request.args.get('search')

            if search:
                #Quitar espacios, hacer todo en minusculas y quitar tildes
                search=search.strip()
                search=search.lower()
                search=' '.join(search.split())
                search=unidecode.unidecode(search)
                
                parametros['search']=search

                

            #Obtenemos los parametros de los select
            orden=request.form.get('select_orden')
            marca=request.form.get('select_marca')
            categoria=request.form.get('select_categoria')
            precio=request.form.get('select_precio')


            #Obtenemos el page
            page=request.args.get('page')


            #Validamos que no sean values 0
            if marca and marca!='0':
                parametros['marca']=marca

            if categoria and categoria!='0':
                parametros['categoria']=categoria

            if precio and precio!='0':
                parametros['precio']=precio

            print('Los parametrillos:',parametros)

            #Redirijimos con los parametros
            return redirect(url_for(ruta,page=page,orden=orden,**parametros))


    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN PaginationProductsManager.py')
        print(error)
        abort(404)