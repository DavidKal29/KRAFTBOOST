from models.entities.Product import Product


class ModelProduct():


    #Metodo estatico para convertir la busqueda que es un string, 
    # en una lista de terminos para filtrar en la consulta
    @staticmethod
    def procesar_search(search):
        import unidecode

        #Limpiar otra vez el search por si las moscas
        
        #Quitar espacios, hacer todo en minusculas y quitar tildes
        search=search.strip()
        search=search.lower()
        search=' '.join(search.split())
        search=unidecode.unidecode(search)

        #Dividiremos el search en palabras que usaremos para 
        # buscar el nombre del producto utilizando likes
        terminos=search.split()

        #Si hay palabras escritas de otra manera, cambiarlas 
        # por palabras que esten en los nombres de los productos
        for i in range(len(terminos)):
            if 'kilo' in terminos[i]:
                terminos[i]='kg'
            
            if 'rodill' in terminos[i]:
                terminos[i]='rodilleras'
            
            if 'cod' in terminos[i]:
                terminos[i]='coderas'
            
            if 'tope' in terminos[i] or 'cierre' in terminos[i] or 'seguro' in terminos[i]:
                terminos[i]='topes'

            #Si alguna palabra tiene algo de peso o pesa, añadir terminos relaciondos con el peso
            if 'pesa' in terminos[i] or 'peso' in terminos[i]:
                terminos.append('mancuerna')


        #Si hay palabras inutiles que molestan a la hora de filtrar, las borramos
        for i in range(len(terminos)-1,-1,-1):
            if terminos[i] in ['de', 'en', 'la', 'el', 'los', 'las', 'y', 'a', 'para', 'por', 'con', 'un', 'una', 'unos', 'unas']:
                del terminos[i]

                

        #Si hay numeros, quitamos el termino kg, para que no 
        # muestre todos los productos con kg en su nombre
        hay_numeros=False
        
        for i in range(len(terminos)):
            if terminos[i].isdigit():
                hay_numeros=True
                break

        
        if hay_numeros:
            for i in range(len(terminos)):
                if terminos[i]=='kg':
                    del terminos[i]
                    break
                
        return terminos
    
    
    #Función para mostrar los productos
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
        



    #Funcion para /shop para devolver el total de productos que se 
    # necesitará para hacer lo de la paginacion
    @classmethod
    def mostrar_contador_productos(cls,db,parametros):
        try:
            #Se abre un cursor con la conexion a la db
            cursor=db.connection.cursor()
        
            #Creamos la consulta base
            sql='SELECT COUNT(*) FROM productos'

            #Creamos la lista que contendrá las condiciones
            condiciones=[]

            #Si hay parametros va mirando cada posible parametro, y añade 
            # a la lista un string que luego meteremos en la consulta
            if parametros:

                if 'marca' in parametros:
                    condiciones.append("id_marca={}".format(parametros['marca']))

                if 'categoria' in parametros:
                    condiciones.append("id_categoria={}".format(parametros['categoria']))

                if 'precio' in parametros:
                    #si es 5-10, quedaria 5 y 10
                    rangos=parametros['precio'].split('-')
                    precio_min=rangos[0]
                    precio_max=rangos[1]

                    condiciones.append("precio>={} AND precio<={}".format(precio_min,precio_max))

                
                if 'search' in parametros:
                    if len(parametros['search'])==1 and not parametros['search'].isdigit():
                        condiciones.append("nombre LIKE '{}%%'".format(parametros['search']))
                    
                    else:
                        terminos=cls.procesar_search(parametros['search'])

                        condiciones_normales=[]
                        condiciones_numeros=[]

                        for termino in terminos:
                            if termino.isdigit():
                                condiciones_numeros.append("nombre LIKE '%%{}%%'".format(termino))
                            
                            else:
                                condiciones_normales.append("nombre LIKE '%%{}%%'".format(termino))



                        if condiciones_normales:
                            condiciones.append(' OR '.join(condiciones_normales))

                        if condiciones_numeros:
                            condiciones.append(' OR '.join(condiciones_numeros))
                            

                    

            
            #si hay condiciones, mete un WHERE y luego, los 
            # strings separados por ands usando el join
            if condiciones:
                sql+=' WHERE '+' AND '.join(condiciones)


            #No meto el parametro orden porque da error al querer sacar un count


            #Ejecutamos la consulta
            cursor.execute(sql)
            resultados=cursor.fetchall()


            #Si hay resultados obtendrémos el count
            if resultados:
                cursor.close()
                return resultados[0][0]
                
            #Si no hay resultados, retornamos None    
            else:
                print(17)
                cursor.close()
                return None
        
        
        #Si hay errores, devolvemos None tambien
        except Exception as error:
            print(error)
            return None
    
        

    

    #Funcion para /shop, donde se mostraran los productos y se filtraran con LIMIT y OFFSET
    # para que se muestren asi con la paginacion
    @classmethod
    def mostrar_productos_paginacion(cls,db,page,productos_por_pagina,orden,parametros):
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

            
            #Creamos la lista donde van las condiciones del where
            condiciones=[]


            #Si hay parametros va mirando cada posible parametro, y añade 
            # a la lista un string que luego meteremos en la consulta
            if parametros:
                if 'marca' in parametros:
                    condiciones.append("id_marca={}".format(parametros['marca']))

                if 'categoria' in parametros:
                    condiciones.append("id_categoria={}".format(parametros['categoria']))

                if 'precio' in parametros:
                    rangos=parametros['precio'].split('-')
                    precio_min=rangos[0]
                    precio_max=rangos[1]

                    condiciones.append("precio>={} AND precio<={}".format(precio_min,precio_max))


                if 'search' in parametros:
                    if len(parametros['search'])==1 and not parametros['search'].isdigit():
                        condiciones.append("nombre LIKE '{}%%'".format(parametros['search']))
                    
                    else:
                        terminos=cls.procesar_search(parametros['search'])

                        condiciones_normales=[]
                        condiciones_numeros=[]

                        for termino in terminos:
                            if termino.isdigit():
                                condiciones_numeros.append("nombre LIKE '%%{}%%'".format(termino))
                            
                            else:
                                condiciones_normales.append("nombre LIKE '%%{}%%'".format(termino))



                        if condiciones_normales:
                            condiciones.append(' OR '.join(condiciones_normales))

                        if condiciones_numeros:
                            condiciones.append(' OR '.join(condiciones_numeros))

                        


                    
            #si hay condiciones, mete un WHERE y luego, los 
            # strings separados por ands usando el join
            if condiciones:
                sql+=' WHERE '+' AND '.join(condiciones)

            print('sql')

            #Mira el orden por el que filtrar
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



    
