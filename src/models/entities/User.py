from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self,id,nombre,apellidos,email,username,password,rol,fecha_registro=None):
        self.id=id
        self.nombre=nombre
        self.apellidos=apellidos
        self.email=email
        self.username=username
        self.password=password
        self.rol=rol
        self.fecha_registro=fecha_registro

    @classmethod
    def checkPassword(cls,hashed_password,password):
        return check_password_hash(hashed_password,password)
    


