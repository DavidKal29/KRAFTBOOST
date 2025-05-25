from models.entities.CartProduct import CartProduct
from models.entities.Order import Order

class ModelOrder:

    @classmethod
    def showOrders(cls,db,id_usuario):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta para obtener los pedidos
            sql='SELECT id,fecha_compra,numero_pedido,precio_total,enviado FROM pedidos WHERE id_usuario=%s ORDER BY id DESC'
            cursor.execute(sql,(id_usuario,))

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
            print('Error al obtener el email')
            print(error)
            return None
        

    
    @classmethod
    def getOrderProducts(cls,db,id_pedido):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            print(1)

            print('el id delpedido:',id_pedido)
            
            sql='''
                SELECT p.nombre,p.imagen,dp.cantidad,dp.precio FROM productos p
                INNER JOIN detalles_pedido dp
                ON p.id=dp.id_producto
                WHERE dp.id_pedido=%s
            '''

            cursor.execute(sql,(id_pedido,))

            row=cursor.fetchall()
            print(row)
            
            #Si hay resultados, recorremos los productos, 
            # los metemos en una lista y devolvemos esa lista
            if row:

                productos=[]

                print(4)

                for p in row:
                    nombre=p[0]
                    imagen=p[1]
                    cantidad=p[2]
                    precio=p[3]

                    productos.append(CartProduct(0,nombre,imagen,cantidad,precio))

                
                cursor.close()

                return productos


            #Sino, retornamos None
            else:
                cursor.close()
                return None
        
        
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al obtener el email')
            print(error)
            return None
        


    
    
    @classmethod
    def showFullOrder(cls,db,id_usuario,num):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta para obtener el pedido
            sql='SELECT * FROM pedidos WHERE numero_pedido=%s and id_usuario=%s'
            cursor.execute(sql,(num,id_usuario))

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

                order=Order(id,fecha_compra,numero_pedido,precio_total,enviado,nombre_destinatario,domicilio,localidad,puerta,codigo_postal)

                cursor.close()

                return order

            #Sino, retornamos None
            else:
                cursor.close()
                return None
        
        
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al obtener el email')
            print(error)
            return None
        


    
    @classmethod
    def deleteOrder(cls,db,id_usuario,id_pedido):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Montamos y ejecutamos la instruccion que borrará los detalles del pedido
            sql='DELETE FROM detalles_pedido WHERE id_pedido=%s'
            cursor.execute(sql,(id_pedido,))
            db.connection.commit()

            
            #Montamos y ejecutamos la instruccion que borrará el pedido
            sql='DELETE FROM pedidos WHERE id_usuario=%s and id=%s'
            cursor.execute(sql,(id_usuario,id_pedido))
            db.connection.commit()

            return True
        
        
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al obtener el email')
            print(error)
            return None
        


##########################################################################################
#Metodos del modo admin
    @classmethod
    def showAllOrders(cls,db,id_usuario=None):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta para obtener los pedidos
            sql='''
                SELECT p.id,p.fecha_compra,p.numero_pedido,p.precio_total,p.enviado,u.username FROM pedidos p
                INNER JOIN usuarios u
                ON p.id_usuario=u.id
            '''

            if id_usuario:
                sql+=' WHERE id_usuario=%s ORDER BY id DESC'
                cursor.execute(sql,(id_usuario,))


            else:
                sql+=' ORDER BY id DESC'
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
                    username=o[5]

                    orders.append(Order(id,fecha_compra,numero_pedido,precio_total,enviado,0,0,0,0,0,username))

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
    def showFullOrderAdmin(cls,db,id):
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
    def deleteOrderAdmin(cls,db,id_pedido):
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
        

    @classmethod
    def setEnviadoOrder(cls,db,id):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            
            #Montamos y ejecutamos la instruccion que cambiara el estado de enviado del pedido
            sql='UPDATE pedidos SET enviado=NOT enviado WHERE id=%s'
            cursor.execute(sql,(id,))
            db.connection.commit()

            return True
        
        
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al activar el producto')
            print(error)
            return None
        
