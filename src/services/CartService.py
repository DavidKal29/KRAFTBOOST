from models.entities.CartProduct import CartProduct

class CartService:

    @classmethod
    def showAllProductsInCart(cls,db,id_usuario):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos el stock y el precio del producto requerido
            sql='''
                SELECT p.id, p.nombre, p.imagen, c.cantidad, c.precio FROM carrito c
                INNER JOIN productos p
                ON c.id_producto=p.id
                WHERE id_usuario=%s
            '''
            cursor.execute(sql,(id_usuario,))
          
            row=cursor.fetchall()

            #Si hay resultados
            if row:
                productos_carrito=[]

                for product in row:
                    id=product[0]
                    nombre=product[1]
                    imagen=product[2]
                    cantidad=product[3]
                    precio=product[4]
                
                    productos_carrito.append(CartProduct(id,nombre,imagen,cantidad,precio))

                return productos_carrito

            #Sino, devolvemos None
            else:
                print('Usuario sin productos en el carrito')
                return None

        #Si hay errores, devolvemos None
        except Exception as error:
            print(error)
            print('Usuario sin productos + error en la consola')
            return None
        




    @classmethod
    def addProductCart(cls,db,id_usuario,id_producto):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos el stock y el precio del producto requerido
            sql='SELECT stock,precio FROM productos WHERE id=%s'
            cursor.execute(sql,(id_producto,))

            row=cursor.fetchone()

            #Si hay resultados
            if row:
                stock=row[0]
                precio=row[1]

                #Si el stock es 0, no permitimos añadir al carrito
                if stock==0:
                    print('Sin stock')
                    return None
                
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
                    db.connection.commit()

                else:
                
                    #Sino, insertamos en la tabla carrito, el id del usuario,producto,cantidad del producto y precio total
                    sql='INSERT INTO carrito (id_usuario,id_producto,cantidad,precio) VALUES (%s,%s,%s,%s)'
                    cursor.execute(sql,(id_usuario,id_producto,1,precio))
                    db.connection.commit()

                #Quitamos 1 al stock del producto requerido
                sql='UPDATE productos SET stock=stock-1 WHERE id=%s'
                cursor.execute(sql,(id_producto,))
                db.connection.commit()

                #Devolvemos true para indicar que todo salió bien
                return True
            
            #Sino, devolvemos None
            else:
                print('Producto erroneo')
                return None

        #Si hay errores, devolvemos None
        except Exception as error:
            print(error)
            print('Producto no añadido')
            return None
        
    
    @classmethod
    def removeOneProductCart(cls,db,id_usuario,id_producto):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos el stock y el precio del producto requerido
            sql='SELECT precio FROM productos WHERE id=%s'
            cursor.execute(sql,(id_producto,))

            row=cursor.fetchone()

            #Si el producto existe
            if row:
                precio=row[0]

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
                        db.connection.commit()

                    else:

                        #Sino restamos la cantidad y el precio de ese producto 
                        # en la tabla carrito asociado al usuario y al producto
                        sql='UPDATE carrito SET cantidad=cantidad-1, precio=precio-%s WHERE id_usuario=%s and id_producto=%s'
                        cursor.execute(sql,(precio,id_usuario,id_producto))
                        db.connection.commit()

                    #Añadimos 1 al stock del producto requerido
                    sql='UPDATE productos SET stock=stock+1 WHERE id=%s'
                    cursor.execute(sql,(id_producto,))
                    db.connection.commit()

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
            print('Producto no añadido')
            return None
        

    @classmethod
    def removeProductCart(cls,db,id_usuario,id_producto):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos el stock y el precio del producto requerido
            sql='SELECT precio FROM productos WHERE id=%s'
            cursor.execute(sql,(id_producto,))

            row=cursor.fetchone()

            #Si el producto existe
            if row:

                #Consultamos a ver si el producto ya fue añadido al carrito antes
                sql='SELECT cantidad FROM carrito WHERE id_usuario=%s and id_producto=%s'
                cursor.execute(sql,(id_usuario,id_producto))

                row2=cursor.fetchone()

                #Si el producto esta en carrito asociado al usuario
                if row2:
                    cantidad=row2[0]

                    sql='DELETE FROM carrito WHERE id_usuario=%s and id_producto=%s'
                    cursor.execute(sql,(id_usuario,id_producto))
                    db.connection.commit()

                    

                    #Añadimos 1 al stock del producto requerido
                    sql='UPDATE productos SET stock=stock+%s WHERE id=%s'
                    cursor.execute(sql,(cantidad,id_producto))
                    db.connection.commit()

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
            print('Producto no añadido')
            return None
        
    
        


