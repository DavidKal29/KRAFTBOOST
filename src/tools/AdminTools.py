from models.entities.User import User

class AdminTools:

    @classmethod
    def getUsers(cls,db,id_admin):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta para obtener los pedidos
            sql='SELECT id,nombre,apellidos,email,username,fecha_registro FROM usuarios WHERE id!=%s ORDER BY id DESC'
            cursor.execute(sql,(id_admin,))

            row=cursor.fetchall()
            
            #Si hay resultados, recorremos los pedidos, 
            # los metemos en una lista y devolvemos esa lista
            if row:
                users=[]
                
                for user in row:
                    id=user[0]
                    nombre=user[1]
                    apellidos=user[2]
                    email=user[3]
                    username=user[4]
                    fecha_registro=user[5]

                    users.append(User(id,nombre,apellidos,email,username,None,None,fecha_registro))    
                    

                cursor.close()

                return users

            #Sino, retornamos None
            else:
                cursor.close()
                return None
        
        
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al obtener los usuarios')
            print(error)
            return None
        


    @classmethod
    def getUser(cls,db,id_user):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta para obtener los pedidos
            sql='SELECT nombre,apellidos,email,username FROM usuarios WHERE id=%s'
            cursor.execute(sql,(id_user,))

            row=cursor.fetchone()
            
            #Si hay resultados, recorremos los pedidos, 
            # los metemos en una lista y devolvemos esa lista
            if row:
                nombre=row[0]
                apellidos=row[1]
                email=row[2]
                username=row[3]

                cursor.close()

                return User(id_user,nombre,apellidos,email,username,None,None)

            #Sino, retornamos None
            else:
                cursor.close()
                return None
        
        
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al obtener al usuario')
            print(error)
            return None
        
