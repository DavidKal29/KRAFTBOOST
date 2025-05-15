from werkzeug.security import generate_password_hash

class ModelUser():

    #Método para registrar usuarios tanto clientes como admins
    @classmethod
    def register(cls,db,user):
        try:
            #Se abre el cursor de la db
            cursor=db.connection.cursor()
            
            #Montamos la instruccion sql para insertar a los usuarios
            sql='INSERT INTO users (nombre,apellidos,email,username,telefono,fecha_nacimiento,password,fecha_registro,rol) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            
            #Creamos la tupla con los valores que se insertaran por medio del %s
            values=(user.nombre, user.apellidos, user.email, user.username, user.telefono, user.fecha_nacimiento,generate_password_hash(user.password), user.fecha_registro, user.rol)

            #Ejecutamos el sql y commiteamos porque es un insert
            cursor.execute(sql,values)
            db.connection.commit()


        except Exception as error:
            print(error)
            return None
        
    


