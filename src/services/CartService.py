from models.entities.CartProduct import CartProduct
from models.ModelUser import ModelUser

class CartService:

    #Método para mostrar todos los productos en el carrito
    @classmethod
    def showAllProductsInCart(cls,db,id_usuario):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos los datos requeridos para mostrar en el carrito
            sql='''
                SELECT p.id, p.nombre, p.imagen, p.stock, c.cantidad, c.precio FROM carrito c
                INNER JOIN productos p
                ON c.id_producto=p.id
                WHERE id_usuario=%s
            '''
            cursor.execute(sql,(id_usuario,))
          
            row=cursor.fetchall()

            #Si hay resultados
            if row:

                #Creamos la lista de productos
                productos_carrito=[]

                #Recorremos los productos y los metemos en esa lista
                for product in row:
                    id=product[0]
                    nombre=product[1]
                    imagen=product[2]
                    stock=product[3]
                    cantidad=product[4]
                    precio=product[5]
                
                    productos_carrito.append(CartProduct(id,nombre,imagen,cantidad,precio,stock))

                cursor.close()
                #Devolvemos los productos
                return productos_carrito

            #Sino, devolvemos None
            else:
                print('Usuario sin productos en el carrito')
                return None

        #Si hay errores, devolvemos None
        except Exception as error:
            print(error)
            cursor.close()
            print('Usuario sin productos en el carrito')
            return None
        


    #Metodos para mostrar el sumario(subtotal)
    @classmethod
    def showSumario(cls,db,id_usuario):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos la suma del precio de todos los productos del carrito de un usuario
            sql='SELECT SUM(precio) FROM carrito WHERE id_usuario=%s'
            cursor.execute(sql,(id_usuario,))
          
            row=cursor.fetchone()

            cursor.close()

            #Si hay resultados devolvemos el subtotal
            if row:
                subtotal=row[0]

                return subtotal

            #Sino, devolvemos None
            else:
                print('Usuario sin productos en el carrito')
                return None

        #Si hay errores, devolvemos None
        except Exception as error:
            print(error)
            cursor.close()
            print('Usuario sin productos en el carrito')
            return None


    #Metodo para añadir productos al carrito
    @classmethod
    def addProductCart(cls,db,id_usuario,id_producto):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos el stock,precio y el estado del producto requerido
            sql='SELECT stock,precio,activo FROM productos WHERE id=%s'
            cursor.execute(sql,(id_producto,))

            row=cursor.fetchone()

            #Si hay resultados
            if row:
                stock=row[0]
                precio=row[1]
                activo=row[2]

                #Si no esta activo impedimos la compra
                if activo==0:
                    cursor.close()
                    return None
                
                #Si el stock es 0, no permitimos añadir al carrito
                if stock==0:
                    print('Sin stock')
                    cursor.close()
                    return 'Sin stock'
                
                #Consultamos a ver si el producto ya fue añadido al carrito antes
                sql='SELECT cantidad FROM carrito WHERE id_usuario=%s and id_producto=%s'
                cursor.execute(sql,(id_usuario,id_producto))

                row2=cursor.fetchone()

                #Si hay resultados
                if row2:

                    #Actualizamos la cantidad y el precio de ese producto en la tabla
                    # carrito asociado al usuario y al producto
                    sql='UPDATE carrito SET cantidad=cantidad+1, precio=precio+%s WHERE id_usuario=%s and id_producto=%s'
                    cursor.execute(sql,(precio,id_usuario,id_producto))

                else:
                
                    #Sino, insertamos en la tabla carrito, el id del usuario,producto,cantidad del producto y precio total
                    sql='INSERT INTO carrito (id_usuario,id_producto,cantidad,precio) VALUES (%s,%s,%s,%s)'
                    cursor.execute(sql,(id_usuario,id_producto,1,precio))
                    

                #Quitamos 1 al stock del producto requerido
                sql='UPDATE productos SET stock=stock-1 WHERE id=%s'
                cursor.execute(sql,(id_producto,))
                db.connection.commit()

                cursor.close()

                #Devolvemos true para indicar que todo salió bien
                return True
            
            #Sino, devolvemos None
            else:
                print('Producto erroneo')
                return None

        #Si hay errores, devolvemos None
        except Exception as error:
            print(error)
            cursor.close()
            print('Producto no añadido')
            return None
        
    
    #Metodo para quitar uno de cantidad al producto del carrito
    @classmethod
    def removeOneProductCart(cls,db,id_usuario,id_producto):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos el stock,precio y estado del producto requerido
            sql='SELECT precio,activo FROM productos WHERE id=%s'
            cursor.execute(sql,(id_producto,))

            row=cursor.fetchone()

            #Si el producto existe
            if row:
                precio=row[0]
                activo=row[1]

                #Si no está activo impedimos la compra
                if activo==0:
                    cursor.close()
                    return None

                #Consultamos a ver si el producto ya fue añadido al carrito antes
                sql='SELECT cantidad FROM carrito WHERE id_usuario=%s and id_producto=%s'
                cursor.execute(sql,(id_usuario,id_producto))

                row2=cursor.fetchone()

                #Si el producto esta en carrito asociado al usuario
                if row2:
                    cantidad=row2[0]

                    #Si la cantidad es una, borramos la fila de la tabla carrito
                    if cantidad==1:
                        sql='DELETE FROM carrito WHERE id_usuario=%s and id_producto=%s'
                        cursor.execute(sql,(id_usuario,id_producto))

                    else:

                        #Sino restamos la cantidad y el precio de ese producto 
                        # en la tabla carrito asociado al usuario y al producto
                        sql='UPDATE carrito SET cantidad=cantidad-1, precio=precio-%s WHERE id_usuario=%s and id_producto=%s'
                        cursor.execute(sql,(precio,id_usuario,id_producto))

                    #Añadimos 1 al stock del producto requerido
                    sql='UPDATE productos SET stock=stock+1 WHERE id=%s'
                    cursor.execute(sql,(id_producto,))
                    
                    #Commiteamos todo
                    db.connection.commit()

                    cursor.close()

                    #Devolvemos True para indicar que todo salio bien
                    return True

                #Sino, devolvemos None          
                else:
                    return None
                
            #Sino, devolvemos None
            else:
                print('Producto erroneo')
                return None

        #Si hay errores, devolvemos None
        except Exception as error:
            print(error)
            cursor.close()
            print('Producto no decrementado')
            return None
        

    #Metodo para quitar el producto del carrito
    @classmethod
    def removeProductCart(cls,db,id_usuario,id_producto):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos el stock y el precio del producto requerido
            sql='SELECT precio,activo FROM productos WHERE id=%s'
            cursor.execute(sql,(id_producto,))

            row=cursor.fetchone()

            #Si el producto existe
            if row:
                activo=row[1]

                #Si no esta activo impedimos la compra
                if activo==0:
                    cursor.close()
                    return None

                #Consultamos a ver si el producto ya fue añadido al carrito antes
                sql='SELECT cantidad FROM carrito WHERE id_usuario=%s and id_producto=%s'
                cursor.execute(sql,(id_usuario,id_producto))

                row2=cursor.fetchone()

                #Si el producto esta en carrito asociado al usuario
                if row2:
                    cantidad=row2[0]

                    sql='DELETE FROM carrito WHERE id_usuario=%s and id_producto=%s'
                    cursor.execute(sql,(id_usuario,id_producto))
                    

                    #Añadimos 1 al stock del producto requerido
                    sql='UPDATE productos SET stock=stock+%s WHERE id=%s'
                    cursor.execute(sql,(cantidad,id_producto))
                    db.connection.commit()
                    
                    cursor.close()
                    
                    #Devolvemos True para indicar que todo salio bien
                    return True

                #Sino, devolvemos None          
                else:
                    return None
                
            #Sino, devolvemos None
            else:
                print('Producto erroneo')
                return None

        #Si hay errores, devolvemos None
        except Exception as error:
            print(error)
            cursor.close()
            print('Producto no borrado')
            return None
    

    #Metodo estático para generar numero de pedido
    @staticmethod
    def generar_numero_pedido(id_pedido):
        import random

        #Es un numero de letras y numeros random mas el id del pedido al final
        nums='1234567890'
        letras='ABCDEFGHIJKLMNOPRSTUVWXYZ'
        numero=''

        for i in range(7):
            if i%2==0:
                numero+=letras[random.randint(0,len(letras)-1)]

            else:
                numero+=nums[random.randint(0,len(nums)-1)]

        numero+=str(id_pedido)

        return numero

    
    #Metodo para crear pedidos
    @classmethod
    def makePedido(cls,db,id):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos la suma de todo el carrito
            sql='SELECT SUM(precio) FROM carrito WHERE id_usuario=%s'
            cursor.execute(sql,(id,))

            #Asignamos el precio total al resultado
            precio_total=cursor.fetchone()[0]

            cursor.close()

            #Obtenemos la direccion de envio
            direccion=ModelUser.getAddress(db,id)

            #Si hay precio total y hay direccion
            if direccion and precio_total:

                #Abrimos un segundo cursor
                cursor=db.connection.cursor()
                
                #Creamos el pedido con los datos requeridos
                sql='INSERT INTO pedidos (precio_total,id_usuario,nombre_destinatario,domicilio,localidad,puerta,codigo_postal,enviado) VALUES (%s,%s,%s,%s,%s,%s,%s,False)'
                cursor.execute(sql,(precio_total,id,direccion.nombre_destinatario,direccion.domicilio,direccion.localidad,direccion.puerta,direccion.codigo_postal))
                
                #Obtenemos el id del pedido
                sql='SELECT id FROM pedidos ORDER BY fecha_compra DESC LIMIT 1'
                cursor.execute(sql)
                
                id_pedido=cursor.fetchone()[0]

                #Creamos el numero de pedido
                numero_pedido=cls.generar_numero_pedido(id_pedido)

                #Actualizamos el numero_pedido del pedido
                sql='UPDATE pedidos SET numero_pedido=%s WHERE id=%s'
                cursor.execute(sql,(numero_pedido,id_pedido))
                
                
                #Obtenemos todos los productos del carrito del usuario
                sql='SELECT id_producto,cantidad,precio FROM carrito WHERE id_usuario=%s'
                cursor.execute(sql,(id,))

                productos=cursor.fetchall()

                #Recorremos los productos
                for p in productos:
                    id_producto=p[0]
                    cantidad=p[1]
                    precio=p[2]

                    #Añadimos las ventas en los productos
                    sql='UPDATE productos SET ventas=ventas+%s WHERE id=%s'
                    cursor.execute(sql,(cantidad,id_producto))

                    #Por cada producto insertamos sus datos en detalles_pedido
                    sql='INSERT INTO detalles_pedido (id_pedido,id_producto,cantidad,precio) VALUES(%s,%s,%s,%s)'
                    cursor.execute(sql,(id_pedido,id_producto,cantidad,precio))
                

                
                #Finalmente, borramos el carrito
                sql='DELETE FROM carrito WHERE id_usuario=%s'
                cursor.execute(sql,(id,))
                db.connection.commit()


                cursor.close()

                print('El numero de pedido:',numero_pedido)

                return numero_pedido

            #Sino, devolvemos None
            else:
                print('Producto erroneo')
                return None

        #Si hay errores, devolvemos None
        except Exception as error:
            db.connection.rollback() #Deshacer todo lo cambiado si fallamos
            print(error)
            print('Pedido no realizado')
            return None


