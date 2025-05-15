from werkzeug.security import generate_password_hash
from models.entities.User import User

class ModelUser():

    #Método para registrar usuarios tanto clientes como admins
    @classmethod
    def register(cls,db,user):
        try:
            print(1)
            #Se abre el cursor de la db
            cursor=db.connection.cursor()

            print(2)
            
            #Montamos la instruccion sql para insertar a los usuarios
            sql='INSERT INTO usuarios (nombre,apellidos,email,username,password,rol) VALUES (%s,%s,%s,%s,%s,%s)'

            print(3)
            
            #Creamos la tupla con los valores que se insertaran por medio del %s
            values=(user.nombre, user.apellidos, user.email, user.username, generate_password_hash(user.password), user.rol)

            print(4)

            #Ejecutamos el sql y commiteamos porque es un insert
            cursor.execute(sql,values)
            print(5)
            db.connection.commit()
            print(6)

            print('Usuario metido con exito')
            print(7)


            cursor.execute('SELECT id,nombre,apellidos,email,username,password,rol FROM usuarios WHERE email=%s',(user.email,))
            print(8)

            row=cursor.fetchone()

            print(9)

            if row:
                print(10)
                id=row[0]
                nombre=row[1]
                apellidos=row[2]
                email=row[3]
                username=row[4]
                password=User.checkPassword(row[5],user.password)
                rol=row[6]

                user=User(id,nombre,apellidos,email,username,password,rol)

                cursor.close()

                print(11)
                return user
            else:
                print(12)
                cursor.close()
                print(13)
                return None

        except Exception as error:
            print(14)
            print(error)
            print('Usuario no ha sido registrado')
            return None
        
    


