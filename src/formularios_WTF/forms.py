from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
import re


def validar_password(form, field):

    #Validamos que tenga al menos 1 minuscula, 1 mayuscula, 1 numero
    if not re.search(r'\d', field.data):
        raise ValidationError('Al menos 1 digito en la contraseña')

    if not re.search(r'[A-Z]', field.data):
        raise ValidationError('Al menos 1 mayúscula en la contraseña')

    if not re.search(r'[a-z]', field.data):
        raise ValidationError('Al menos 1 minúscula en la contraseña')

    

#Formulario de register
class Register(FlaskForm):

    nombre=StringField('Nombre',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=25,message='3-25 caracteres requeridos')
    ])

    apellidos=StringField('Apellidos',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=25,message='3-25 caracteres requeridos')
    ])

    email=EmailField('Correo electrónico',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=10,max=150,message='10-150 caracteres requeridos'),
        Email()
    ])

    username=StringField('Username',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=5,max=25,message='5-25 caracteres requeridos')
    ])

    password=PasswordField('Contraseña',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=8,max=100,message='8-100 caracteres requeridos'),
        validar_password
    ])

    confirm=PasswordField('Confirmar Contraseña',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=8,max=100,message='8-100 caracteres requeridos'),
        EqualTo('password',message='Contraseñas no coinciden')
        
    ])

    submit=SubmitField('Crear Cuenta')


