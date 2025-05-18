class CartService:

    @classmethod
    def addProduct(cls,db,id_usuario,id_producto):
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
                
                #Insertamos en la tabla carrito, el id del usuario,producto,cantidad del producto y precio total
                sql='INSERT INTO carrito (id_usuario,id_producto,cantidad,precio) VALUES (%s,%s,%s,%s)'
                cursor.execute(sql,(id_usuario,id_producto,1,precio))
                db.connection.commit()

                #Quitamos 1 al stock del producto requerido
                sql='UPDATE productos SET stock=stock-1 WHERE id=%s'
                cursor.execute(sql,(id_producto,))
                db.connection.commit()

                #Devolvemos true para indicar que todo salio bien
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
        


