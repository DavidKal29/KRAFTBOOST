from models.entities.Product import Product

class ModelProduct():
    
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



    
