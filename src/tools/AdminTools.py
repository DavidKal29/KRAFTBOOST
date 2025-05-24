from models.entities.User import User
from models.ModelOrder import Order

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
        


    @classmethod
    def showAllOrders(cls,db):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta para obtener los pedidos
            sql='SELECT id,fecha_compra,numero_pedido,precio_total,enviado FROM pedidos ORDER BY id DESC'
            cursor.execute(sql)

            row=cursor.fetchall()
            
            #Si hay resultados, recorremos los pedidos, 
            # los metemos en una lista y devolvemos esa lista
            if row:
                orders=[]
                
                for o in row:
                    id=o[0]
                    fecha_compra=o[1]
                    numero_pedido=o[2]
                    precio_total=o[3]
                    enviado=o[4]

                    orders.append(Order(id,fecha_compra,numero_pedido,precio_total,enviado,0,0,0,0,0))

                cursor.close()

                return orders

            #Sino, retornamos None
            else:
                cursor.close()
                return None
        
        
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al obtener los pedidos')
            print(error)
            return None
        

    @classmethod
    def showFullOrder(cls,db,id):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta para obtener el pedido
            sql='SELECT * FROM pedidos WHERE id=%s'
            cursor.execute(sql,(id,))

            row=cursor.fetchone()
            
            #Si hay resultados, recorremos los pedidos, 
            # los metemos en una lista y devolvemos esa lista
            if row:
                id=row[0]
                fecha_compra=row[1]
                numero_pedido=row[2]
                precio_total=row[3]
                nombre_destinatario=row[5]
                domicilio=row[6]
                localidad=row[7]
                puerta=row[8]
                codigo_postal=row[9]
                enviado=row[10]

                print(id,fecha_compra,numero_pedido,precio_total,nombre_destinatario,domicilio,localidad,puerta,codigo_postal,enviado)

                print('Kekeojones')

                order=Order(id,fecha_compra,numero_pedido,precio_total,enviado,nombre_destinatario,domicilio,localidad,puerta,codigo_postal)

                cursor.close()

                return order

            #Sino, retornamos None
            else:
                cursor.close()
                return None
        
        
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al obtener el pedido')
            print(error)
            return None
        

    @classmethod
    def deleteOrder(cls,db,id_pedido):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Montamos y ejecutamos la instruccion que borrará los detalles del pedido
            sql='DELETE FROM detalles_pedido WHERE id_pedido=%s'
            cursor.execute(sql,(id_pedido,))
            db.connection.commit()

            
            #Montamos y ejecutamos la instruccion que borrará el pedido
            sql='DELETE FROM pedidos WHERE id=%s'
            cursor.execute(sql,(id_pedido,))
            db.connection.commit()

            return True
        
        
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al borrar el pedido')
            print(error)
            return None
        
        
