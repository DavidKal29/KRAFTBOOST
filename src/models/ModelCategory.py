from entities.Category import Category

class ModelCateogry():
    
    #Función para devolver todas las categorías
    @classmethod
    def mostrar_categorias(cls,db):
        try:
            #Se abre un cursor con la conexion a la db y se crea la consulta sql
            cursor=db.connection.cursor()
            sql='SELECT * FROM categorias'
            
            #Se ejecuta la consulta, y apuntamos una variable al resultado de la consultilla
            cursor.execute(sql)
            resultados=cursor.fetchall()

            #Si la consulta devuelve datos, creamos una lista, recorremos los datos 
            # y creamos un objeto con cada categoria, metiendolo en la lista
            if resultados:
                categorias=[]

                for resultado in resultados:
                    id=resultado[0]
                    nombre=resultado[1]
                    imagen=resultado[2]

                    categorias.append(Category(id,nombre,imagen))

                cursor.close()
                return categorias
                
            #Si no hay resultados, retornamos None    
            else:
                cursor.close()
                return None
        
        
        #Si hay errores, devolvemos None tambien
        except Exception as error:
            print(error)
            return None
