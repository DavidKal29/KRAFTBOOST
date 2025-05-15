from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self,id,nombre,apellidos,email,username,password,rol):
        self.id=id
        self.nombre=nombre
        self.apellidos=apellidos
        self.email=email
        self.username=username
        self.password=password
        self.rol=rol

    @classmethod
    def checkPassword(cls,hashed_password,password):
        return check_password_hash(hashed_password,password)
    


