from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Email

    

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
    ])

    confirm=PasswordField('Confirmar Contraseña',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=8,max=100,message='8-100 caracteres requeridos'),
        EqualTo('password',message='Contraseñas no coinciden')
        
    ])

    submit=SubmitField('Crear Cuenta')


