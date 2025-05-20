from werkzeug.security import generate_password_hash,check_password_hash
from models.entities.User import User
from models.entities.Address import Address

class ModelUser():

    #Metodo para iniciar sesion y poder acceder a perfil
    @classmethod
    def login(cls,db,user):
        try:
            #Se abe el cursor d ela db
            cursor=db.connection.cursor()

            #Se crea la consulta esql
            sql='SELECT * FROM usuarios WHERE email=%s'

            #Ejecutamos la cosulta
            cursor.execute(sql,(user.email,))
            row=cursor.fetchone()

            #Si hay resultados, creamos el objeto logged_user y lo devolvemos
            if row:
                print('Usuario encontrado')
                id=row[0]
                nombre=row[1]
                apellidos=row[2]
                email=row[3]
                username=row[4]
                password=User.checkPassword(row[5],user.password)
                rol=row[6]

                logged_user=User(id,nombre,apellidos,email,username,password,rol)

                print('El user logueado:',logged_user)

                cursor.close()
             
                return logged_user
            
            #Sino, retornamos None
            else:
                cursor.close()
                return None
        
        #Cualquier otro error, devolvemos None
        except Exception as error:
            print('Usuario no ha sido logueado')
            print(error)
            return None

    #Método para registrar usuarios tanto clientes como admins
    @classmethod
    def register(cls,db,user):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Montamos la instruccion sql para insertar a los usuarios
            sql='INSERT INTO usuarios (nombre,apellidos,email,username,password,rol) VALUES (%s,%s,%s,%s,%s,%s)'

            #Creamos la tupla con los valores que se insertaran por medio del %s
            values=(user.nombre, user.apellidos, user.email, user.username, generate_password_hash(user.password), user.rol)

            #Ejecutamos el sql y commiteamos porque es un insert
            cursor.execute(sql,values)
            db.connection.commit()

            print('Usuario metido con exito')

            #Obtenemos al usuario para poder iniciar sesión facilmente
            cursor.execute('SELECT id,nombre,apellidos,email,username,password,rol FROM usuarios WHERE email=%s',(user.email,))
            row=cursor.fetchone()

            #Si hay resultado metemos los datos obtenidos en el logged userr y lo devolvemos
            if row:
                id=row[0]
                nombre=row[1]
                apellidos=row[2]
                email=row[3]
                username=row[4]
                password=User.checkPassword(row[5],user.password)
                rol=row[6]

                user=User(id,nombre,apellidos,email,username,password,rol)

                cursor.close()
                return user
            
            #Sino, devolvemos None
            else:
                cursor.close()
                return None

        #Si hay errores, devolvemos None
        except Exception as error:
            print(error)
            print('Usuario no ha sido registrado')
            return None
        

    #Método para obtener el usuario por el id en el user loader
    @classmethod
    def get_by_id(cls,db,id):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta y la ejecutamos
            sql='SELECT * FROM usuarios WHERE id=%s'
            cursor.execute(sql,(id,))

            row=cursor.fetchone()
            
            #Si hay resultados, creamos el objeto user, sin el password, y lo devolvemos
            if row:
                id=row[0]
                nombre=row[1]
                apellidos=row[2]
                email=row[3]
                username=row[4]
                password=None
                rol=row[6]

                logged_user=User(id,nombre,apellidos,email,username,password,rol)
                
                cursor.close()
             
                return logged_user
            
            #Si no hay resultado, devolvemos None
            else:
                cursor.close()
                return None

        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al obtener el id')
            print(error)
            return None
    

    #Método para validar el email que se introduce al recuerar contraseña
    @classmethod
    def validate_email(cls,db,email):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la consulta y la ejecutamos
            sql='SELECT email FROM usuarios WHERE email=%s'
            cursor.execute(sql,(email,))

            #Variable para ver si el email existe o no
            validation=False

            row=cursor.fetchone()
            
            #Si hay resultados, cambiamos validation a True
            if row:
                print('Email encontrado')
                validation=True

                cursor.close()

                return validation
            
            #Si no hay resultado, devolvemos None
            else:
                print('Email no encontrado')

                cursor.close()
                
                return validation

        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al obtener el email')
            print(error)
            return None


    #Método para cambiar la contraseña 
    @classmethod
    def change_password(cls,db,email,new_password):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos la contraseña antigua
            sql='SELECT password FROM usuarios WHERE email=%s'
            cursor.execute(sql,(email,))

            #Obtenemos el row
            row=cursor.fetchone()

            #Si hay resultados, obtenemos el password antiguo
            if row:
                old_password=row[0]
            
            #Si la contraseña antigua y la nueva son iguales, no 
            # cambiamos anda y mandamos el mensaje de que son iguales
            if check_password_hash(old_password, new_password):
                return 'Contraseñas iguales'
            
            #Encriptamos la contraseña para mandarla encriptada a la db
            new_password=generate_password_hash(new_password)
            
            #Montamos el update, ejecutamos y commiteamos
            sql='UPDATE usuarios SET password=%s WHERE email=%s'
            cursor.execute(sql,(new_password,email))
            db.connection.commit()

            #Devolvemos true si todo sale bien
            return True

            
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al cambiar password')
            print(error)
            return None
    

    #Metodo para obtener la direccion de envio
    @classmethod
    def getAddress(cls,db,id):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos los datos de direccion
            sql='SELECT nombre_destinatario,domicilio,localidad,puerta,codigo_postal FROM domicilios WHERE id_usuario=%s'
            cursor.execute(sql,(id,))

            #Obtenemos el row
            row=cursor.fetchone()

            #Si hay resultados, devolvemos la direccion con sus datos
            if row:
                nombre_destinatario=row[0]
                domicilio=row[1]
                localidad=row[2]
                puerta=row[3]
                codigo_postal=row[4]
                id_usuario=id

                direccion=Address(nombre_destinatario,domicilio,localidad,puerta,codigo_postal,id_usuario)

                cursor.close()

                return direccion
            
            #Sino devolvemos None
            else:
                cursor.close()
                return None
                   
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al cambiar password')
            print(error)
            return None

    
    #Metodo para cambiar la direccion de envio
    @classmethod
    def setAddress(cls,db,address):
        try:

            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            #Obtenemos la contraseña antigua
            sql='SELECT domicilio FROM domicilios WHERE id_usuario=%s'
            cursor.execute(sql,(address.id_usuario,))

            #Obtenemos el row
            row=cursor.fetchone()

            #Si hay resultados
            if row:
            
                #Actualizamos la dirección antigua
                sql='UPDATE domicilios SET nombre_destinatario=%s,domicilio=%s,localidad=%s,puerta=%s,codigo_postal=%s WHERE id_usuario=%s'
                cursor.execute(sql,(address.nombre_destinatario,address.domicilio,address.localidad,address.puerta,address.codigo_postal,address.id_usuario))
                db.connection.commit()
            
            else:
                #Insertamos la nueva dirección con los datos
                sql='INSERT INTO domicilios (nombre_destinatario,domicilio,localidad,puerta,codigo_postal,id_usuario) VALUES(%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql,(address.nombre_destinatario,address.domicilio,address.localidad,address.puerta,address.codigo_postal,address.id_usuario))
                db.connection.commit()
            

            #Devolvemos true si todo sale bien
            return True

            
        #Cualquier error distitno, None también        
        except Exception as error:
            print('Error al cambiar password')
            print(error)
            return None
        



