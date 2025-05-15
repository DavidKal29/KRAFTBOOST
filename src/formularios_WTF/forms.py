from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField,TelField,DateField
from wtforms.validators import DataRequired,Length,EqualTo,Email

#Formulario de register
class Register(FlaskForm):

    nombre=StringField('Nombre',validators=[
        DataRequired(),
        Length(min=3,max=25,message='3-25 chars required')
    ])

    apellidos=StringField('Apellidos',validators=[
        DataRequired(),
        Length(min=3,max=25,message='3-25 chars required')
    ])

    email=EmailField('Correo electrónico',validators=[
        DataRequired(),
        Length(min=10,max=150,message='10-150 chars required'),
        Email()
    ])

    username=StringField('Username',validators=[
        DataRequired(),
        Length(min=5,max=25,message='5-25 chars required')
    ])

    password=PasswordField('Contraseña',validators=[
        DataRequired(),
        Length(min=5,max=255)
    ])

    confirm=PasswordField('Confirmar',validators=[
        DataRequired(),
        Length(min=5,max=255),
        EqualTo('password',message='The passwords not equal')
    ])

    submit=SubmitField('Crear Cuenta')