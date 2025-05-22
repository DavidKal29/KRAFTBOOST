from models.entities.CartProduct import CartProduct
from models.entities.Order import Order

class ModelOrder:

    @classmethod
    def showOrders(cls,db,id_usuario):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta para obtener los pedidos
            sql='SELECT id,fecha_compra,numero_pedido,precio_total,enviado FROM pedidos WHERE id_usuario=%s'
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