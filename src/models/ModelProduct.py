from models.entities.Product import Product


class ModelProduct():


    #Función basica para mostrar productos en inicio
    @classmethod
    def mostrar_productos(cls,db,order):
        try:
            #Se abre un cursor con la conexion a la db y se crea la consulta sql
            cursor=db.connection.cursor()

            #En este caso, en home, se mostrarán productos mas venidos y 
            # mas nuevos por tanto, la variable order tendrá id o
            # ventas, para poder filtrar y sacar los productos requeridos
            if order=='id':
                sql='SELECT id,nombre,precio,imagen FROM productos ORDER BY id DESC LIMIT 8'
            elif order=='ventas':
                sql='SELECT id,nombre,precio,imagen FROM productos ORDER BY ventas DESC LIMIT 8'
            else:
                cursor.close()
                return None

            #Ejecutamos la consulta
            cursor.execute(sql)
            resultados=cursor.fetchall()
           
            #Si la consulta devuelve datos, creamos una lista, recorremos los datos 
            # y creamos un objeto con cada producto, metiendolos en la lista
            if resultados:
                productos=[]

                for resultado in resultados:
                    id=resultado[0]
                    nombre=resultado[1]
                    precio=resultado[2]
                    imagen=resultado[3]

                    productos.append(Product(id,nombre, precio, None, None, None, imagen))

                cursor.close()
                return productos
                
            #Si no hay resultados, retornamos None    
            else:
                cursor.close()
                return None
        
        
        #Si hay errores, devolvemos None tambien
        except Exception as error:
            print(error)
            return None

    
    #Metodo estatico para convertir la busqueda que es un string, 
    # en una lista de terminos para filtrar en la consulta
    @staticmethod
    def procesar_search(search,categorias):
        import unidecode

        #Quitar espacios, hacer todo en minusculas y quitar tildes
        search=search.strip()
        search=search.lower()
        search=' '.join(search.split())
        search=unidecode.unidecode(search)

        #Dividiremos el search en palabras que usaremos para 
        # buscar el nombre del producto utilizando likes
        terminos=search.split()
        print('Los terminos primeros',terminos)

        #Manejar terminos que tengan el numero y 
        # los kilos igual, tipo '20kilos' o '10kg'
        for i in range(len(terminos)):
            #Casos en los que kg va separado
            if ('kilo' in terminos[i] or 'kg' in terminos[i]) and terminos[i].isalpha():
                terminos[i]='kg'

            
            #Casos en los que kg va junto
            if ('kilo' in terminos[i] or 'kg' in terminos[i]) and not terminos[i].isalpha() and not terminos[i].isdigit():
                
                #Vamos recorriendo el termino, metiendo en 
                # una lista los numeros que saquemos de ahi
                numeros=[]
                numero=''
                
                for p in terminos[i]:
                    if p.isdigit() or p=='.':
                        numero+=p

                    else:
                        numeros.append(numero)
                        numero=''
                
                numeros.append(numero)

                for n in numeros:
                    terminos.append(n)
                    
                terminos[i]=''


        #Reemplazamos las comas por puntos, para los decimales
        terminos[i]=terminos[i].replace(',','.')
                
        #Comprobamos si un termino es un float o no
        for i in range(len(terminos)):
            try:
                valor=float(terminos[i])
                print(valor)
            
            except:
                #Si no es un float, tiene letras
                print('No es un float')
                
                #Vemos si el termino tiene carácteres molestos
                if not terminos[i].isalnum():
                    print('Contiene terminos raros')

                    #Creo una lista solo con caracteres normales y los junto con join
                    terminos[i]=''.join([p for p in terminos[i] if p.isalnum()])


        #Recorremos los terminos, para ver si se han puesto cosas, 
        # que deberian arrojar resultados pero por no ser escritos 
        # como estan en la db, se reemplazan.
        reglas={
            'rodilleras':['rodill'],
            'coderas':['cod'],
            'estructura':['maquina'],
            'gorilla':['gorila'],
            'inclinado':['inclinado'],
            'plano':['plano'],
            'banco':['banca'],
            'agarre':['agarre', 'ganch', 'agarra'],
            'banda':['liga','elastic'],
            'topes':['tope','cierre','seguro','seguridad'],
            'mancuerna':['pesa','mancu'],
            'kettlebell':['ruso', 'rusa','ketlebel']
        }

        
        #Recorrer todos los terminos
        for i in range(len(terminos)):
            #Recorrer el dicionario reglas
            for nuevo_valor, patrones in reglas.items():
                #Recorremos los diferentes patrones
                for patron in patrones:
                    #Si el patron esta dentro de un termino sustituimos
                    if patron in terminos[i]:
                        terminos[i]=nuevo_valor
                        break  
                
            
        #Aprovechamos las categorias para poner en singular lo que se busca      
        for i in range(len(terminos)):              
            for categoria in categorias:
                if terminos[i]==categoria.nombre.lower():
                    terminos[i]=categoria.nombre.lower()[:-1]


        

        #Si hay palabras inutiles que molestan a la hora de filtrar, las borramos
        for i in range(len(terminos)-1,-1,-1):
            if terminos[i] in ['','de', 'o', 'en', 'la', 'el', 'los', 'las', 'y', 'a', 'para', 'por', 'con', 'un', 'una', 'unos', 'unas']:
                del terminos[i]

                

        #Variable para ver si hay numeros o decimales
        hay_numeros=False
        

        #Recorrer los terminos, ver si es numero/decimal, 
        # y poner True la variable si es asi
        for i in range(len(terminos)):
            if terminos[i].isdigit():
                hay_numeros=True
                print('Es un digito')
            else:
                try:
                    termino_float=float(terminos[i])
                    print('Es un float')
                    hay_numeros=True
                except:
                    print('No es un numero')


        
        #Si hay numeros, borramos todos los terminos que sean kg, 
        # para evitar que al hacer la consulta, pille todos los 
        # productos que tengan kg
        if hay_numeros:
            for i in range(len(terminos)-1,-1,-1):
                if terminos[i]=='kg':
                    del terminos[i]

        
        print('Los terminos:',terminos)
                
        return terminos
    
    
    
        
    #Metodo para construir el where de la consulta para msotrar productos
    @classmethod
    def construir_where(cls,parametros,categorias):
        
        #Creamos la lista donde van las condiciones del where y 
        # la usaré para luego juntar todo con un join
        condiciones=[]

        #Si hay parametros va mirando cada posible parametro, y añade 
        # a la lista un string que se juntará con el join
        if parametros:

            if 'marca' in parametros:
                condiciones.append("id_marca={}".format(parametros['marca']))


            if 'categoria' in parametros:
                condiciones.append("id_categoria={}".format(parametros['categoria']))


            if 'precio' in parametros:

                #Divide el stirng por el precio minimo y maximo
                rangos=parametros['precio'].split('-')
                precio_min=rangos[0]
                precio_max=rangos[1]

                condiciones.append("precio>={} AND precio<={}".format(precio_min,precio_max))


            #Si alguien buscó algo en el buscador
            if 'search' in parametros:
    
                #Obtiene una lista de eso que buscó usando el metodo estatico para procesar el search
                terminos=cls.procesar_search(parametros['search'],categorias)

                #Creamos listas para los tipos de condiciones
                condiciones_palabras=[]
                condiciones_numeros=[]
                condiciones_marcas=[]
                condiciones_materiales=[]
                condiciones_kilos=[]


                #Recorre los terminos
                for termino in terminos:
                    #Si es un número, añade a las condiciones_numeros con el kg
                    if termino.isdigit():
                    
                        condiciones_numeros.append("nombre LIKE '%% {}kg%%'".format(termino))
                    

                    #Si no es un numero
                    else:
                        try:
                
                            #Intenta pasarlo a float para ver si es un decimal
                            termino=float(termino)
                                
                            #Si es un decimal se añade como si fuera un numero mas, con el kg
                            condiciones_numeros.append("nombre LIKE '%% {}kg%%'".format(termino))
        
                                
                        #Si falla es porque es una palabra   
                        except Exception as error:

                            if termino=='kg':
                                condiciones_kilos.append("nombre LIKE '%%{}%%'".format(termino))

                            #Si es alguna marca lo añade a las condiciones_marcas
                            elif termino in ['domyos','maniak','corength','e-series','kraftboost','tunturi']:
                                condiciones_marcas.append("nombre LIKE '%%{}%%'".format(termino))

                            elif termino in ['inclinado','plano','abierto','cuerda','metal','neutro','unilateral','estrecho','gironda','hierro','goma','metalico']:
                                condiciones_materiales.append("nombre LIKE '%%{}%%'".format(termino))

                            #Sino ya lo mete en condiciones_palabras    
                            else:
                                condiciones_palabras.append("nombre LIKE '%%{}%%'".format(termino))
                
                
                #Con cada lista, juntamos los strings con ors y dentro de parentesis, 
                # para que, cada grupo de condiciones si o si deban cumplirse
                if condiciones_palabras:
                    condiciones.append('({})'.format(' OR '.join(condiciones_palabras)))

                if condiciones_marcas:
                    condiciones.append('({})'.format(' OR '.join(condiciones_marcas)))

                if condiciones_materiales:
                    condiciones.append('({})'.format(' OR '.join(condiciones_materiales)))

                if condiciones_numeros:
                    condiciones.append('({})'.format(' OR '.join(condiciones_numeros)))
                
                if condiciones_kilos:
                    condiciones.append('({})'.format(' OR '.join(condiciones_kilos)))
            
            
            #si hay condiciones, mete un WHERE y luego, los 
            # strings separados por ands usando el join
            if condiciones:

                condiciones=' WHERE '+' AND '.join(condiciones)
                print('Las condiciones ya procesadas:',condiciones)
                
                return condiciones
                
            return ''
        
        return ''


    #Funcion para /shop para devolver el total de productos que se 
    # necesitará para hacer lo de la paginacion
    @classmethod
    def mostrar_contador_productos(cls,db,parametros,categorias):
        try:
            #Se abre un cursor con la conexion a la db
            cursor=db.connection.cursor()
        
            #Creamos la consulta base
            sql='SELECT COUNT(*) FROM productos'
            
            #Añado al sql, las condiciones del where
            condiciones=cls.construir_where(parametros, categorias)
            sql+=condiciones
            
            #Ejecutamos la consulta
            cursor.execute(sql)
            resultados=cursor.fetchall()

            #Si hay resultados obtendrémos el count
            if resultados:

                cursor.close()
                return resultados[0][0]
                 
            #Si no hay resultados, retornamos None    
            else:

                cursor.close()
                return None
        
        
        #Si hay errores, devolvemos None tambien
        except Exception as error:
            print(error)
            return None
    
        

    

    #Funcion para /shop, donde se mostraran los productos y se filtraran con LIMIT y OFFSET
    # para que se muestren asi con la paginación
    @classmethod
    def mostrar_productos_paginacion(cls,db,page,productos_por_pagina,orden,parametros,categorias):
        try:
            #Se abre un cursor con la conexion a la db
            cursor=db.connection.cursor()

            #El limit seran el numero de productos que apareceran
            # en este caso, los productos por pagina
            limit=productos_por_pagina

            #El offset es cuantos productos se saltará, pero claro, si page es 1, 
            # debe saltarse 0, por tanto restamos 1 a page
            offset=(page-1)*productos_por_pagina
            

            #Montamos la consulta base
            sql='SELECT id,nombre,precio,imagen FROM productos'

            #Añado al sql, las condiciones del where
            condiciones=cls.construir_where(parametros, categorias)
            sql+=condiciones


            #Mira el orden por cual filtrar
            if orden=='masRecientes':
                sql+=' ORDER BY id DESC'

            elif orden=='topVentas':
                sql+=' ORDER BY ventas DESC'


            #Añadimos al final el limit y el offset con /%s
            sql+=' LIMIT %s OFFSET %s'

            print(sql)

            values=(limit,offset)
            
            # #Ejecutamos la consulta
            cursor.execute(sql,values)
            resultados=cursor.fetchall()
           

            #Si la consulta devuelve datos, creamos una lista, recorremos los datos 
            # y creamos un objeto con cada producto, metiendolos en la lista
            if resultados:
                productos=[]

                for resultado in resultados:
                    id=resultado[0]
                    nombre=resultado[1]
                    precio=resultado[2]
                    imagen=resultado[3]

                    productos.append(Product(id,nombre, precio, None, None, None, imagen))

                cursor.close()
                return productos
                
            #Si no hay resultados, retornamos None    
            else:
                cursor.close()
                return None
        
        
        #Si hay errores, devolvemos None tambien
        except Exception as error:
            print(error)
            return None
        
    

    @classmethod
    def mostrar_producto_info(cls,db,id):

        try:
            #Abrimos como siempre el cursor
            cursor=db.connection.cursor()

            #Montamos una consulta con joins para obtener el nombre de la categoria y marca
            sql='''
                SELECT p.nombre as nombre_producto,p.precio,p.descripcion,p.imagen,
                m.nombre as nombre_marca,
                c.nombre as nombre_categoria
                FROM productos p
                INNER JOIN marcas m ON p.id_marca=m.id
                INNER JOIN categorias c ON p.id_categoria=c.id
                WHERE p.id=%s;
            '''

            #Ejecutamos
            cursor.execute(sql,(id,))
            resultado=cursor.fetchall()
           

            #SI hay resultado, metemos todos los campos devueltos en el objeto Product y retornamos eso
            if resultado:

                print('Er resultado:',resultado)
                
                nombre_producto=resultado[0][0]
                precio=resultado[0][1]
                descripcion=resultado[0][2]
                imagen=resultado[0][3]
                nombre_marca=resultado[0][4]
                nombre_categoria=resultado[0][5]


                producto=Product(id, nombre_producto, precio, nombre_marca, nombre_categoria, descripcion, imagen)

            
                cursor.close()
                return producto
                
            #Si no hay resultados, retornamos None    
            else:
                cursor.close()
                return None
        
        
        #Si hay errores, devolvemos None tambien
        except Exception as error:
            print(error)
            return None




