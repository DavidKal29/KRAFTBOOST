from entities.Product import Product

class ModelProduct():
    
    #Función para mostrar los productos
    @classmethod
    def mostrar_productos(cls,db,order):
        try:
            #Se abre un cursor con la conexion a la db y se crea la consulta sql
            cursor=db.connection.cursor()
            sql='SELECT id,nombre,precio,imagen FROM productos ORDER BY %s DESC LIMIT 8'
            
            #En este caso, en home, se mostrarán productos mas venidos y 
            # mas nuevos por tanto, la variable order tendrá el id o el número
            # de ventas, para poder filtrar y sacar los productos requeridos
            cursor.execute(sql,order)
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
