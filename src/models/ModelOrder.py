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
            
            sql='''
                SELECT p.nombre,p.imagen,dp.cantidad,dp.precio FROM productos p
                INNER JOIN detalles_pedido dp
                ON p.id=dp.id_producto
                WHERE dp.id_pedido=%s
            '''

            cursor.execute(sql,(id_pedido,))

            row=cursor.fetchall()
            
            #Si hay resultados, recorremos los productos, 
            # los metemos en una lista y devolvemos esa lista
            if row:

                productos=[]

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