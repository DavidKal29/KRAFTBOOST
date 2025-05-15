from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self,id,nombre,apellidos,email,username,telefono,fecha_nacimiento,password,rol):
        self.id=id
        self.nombre=nombre
        self.apellidos=apellidos
        self.email=email
        self.username=username
        self.telefono=telefono
        self.fecha_nacimiento=fecha_nacimiento
        self.password=password
        self.rol=rol

    @classmethod
    def checkPassword(cls,hashed_password,password):
        return check_password_hash(hashed_password,password)
    


