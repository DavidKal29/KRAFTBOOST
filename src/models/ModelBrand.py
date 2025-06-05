from models.entities.Brand import Brand

class ModelBrand():
    
    #Función para devolver todas las marcas
    @classmethod
    def mostrar_marcas(cls,db):
        try:
            #Se abre un cursor con la conexion a la db y se crea la consulta sql
            cursor=db.connection.cursor()
            sql='SELECT * FROM marcas'
            
            #Se ejecuta la consulta, y apuntamos una variable al resultado de la consultilla
            cursor.execute(sql)
            resultados=cursor.fetchall()

            #Si la consulta devuelve datos, creamos una lista, recorremos los datos 
            # y creamos un objeto con cada marca, metiendolo en la lista
            if resultados:
                marcas=[]

                for resultado in resultados:
                    id=resultado[0]
                    nombre=resultado[1]

                    marcas.append(Brand(id,nombre))

                cursor.close()
                return marcas
                
            #Si no hay resultados, retornamos None    
            else:
                cursor.close()
                return None
        
        
        #Si hay errores, devolvemos None tambien
        except Exception as error:
            print(error)
            return None
        
        finally:
            if cursor:
                cursor.close()