from werkzeug.security import generate_password_hash
from models.entities.User import User

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
            cursor.execute(sql,user.email,)
            row=cursor.fetchone()

            #Si hay resultados, creamos el objeto logged_user y lo devolvemos
            if row:
                id=row[0]
                nombre=row[1]
                apellidos=row[2]
                email=row[3]
                username=row[4]
                password=User.checkPassword(row[5],user.password)
                rol=row[6]

                logged_user=User(id,nombre,apellidos,email,username,password,rol)
                
                cursor.close()
             
                return logged_user
            
            #Sino, retornamos None
            else:
                cursor.close()
                return None
        
        #Cualquier otro error, devolvemos None
        except Exception as error:
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

            cursor.execute('SELECT id,nombre,apellidos,email,username,password,rol FROM usuarios WHERE email=%s',(user.email,))
            row=cursor.fetchone()


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
            
            else:
                cursor.close()
                return None

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
            print(error)
            return None
    


