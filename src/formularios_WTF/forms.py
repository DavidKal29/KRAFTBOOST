from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError,NumberRange
import re

#validador de password
def validar_password(form, field):

    #Validamos que tenga al menos 1 minuscula, 1 mayuscula, 1 numero
    if not re.search(r'\d', field.data):
        raise ValidationError('Al menos 1 digito en la contraseña')

    if not re.search(r'[A-Z]', field.data):
        raise ValidationError('Al menos 1 mayúscula en la contraseña')

    if not re.search(r'[a-z]', field.data):
        raise ValidationError('Al menos 1 minúscula en la contraseña')
    
#Validador de fechas
def validar_year(form, field):
    from datetime import datetime

    year_actual=datetime.now().year

    if field.data<year_actual:
        raise ValidationError('Año de expiración inválido')
    
def validar_mes(form, field):
    from datetime import datetime

    year_actual=datetime.now().year
    mes_actual=datetime.now().month

    if form.year.data<=year_actual and field.data<mes_actual:
        raise ValidationError('Mes de expiración inválido')
    

#Validador de digitos
def validar_digitos(form,field):
    if not field.data.isdigit():
        raise ValidationError('Este campo solo puede tener digitos')

    

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


#Formulario de login
class Login(FlaskForm):

    email=EmailField('Correo electrónico',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=10,max=150,message='10-150 caracteres requeridos'),
        Email()
    ])

    password=PasswordField('Contraseña',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=8,max=100,message='8-100 caracteres requeridos')
    ])

    submit=SubmitField('Iniciar Sesión')


#Formulario de enviar email para recuperar contraseña
class EmailRecuperacion(FlaskForm):

    email=EmailField('Correo electrónico',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=10,max=150,message='10-150 caracteres requeridos'),
        Email()
    ])

    submit=SubmitField('Enviar Email')


#Formulario de enviar email para recuperar contraseña
class ChangePassword(FlaskForm):

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
    

    submit=SubmitField('Cambiar Contraseña')


#Formulario para enviar direccion de email
class AddressForm(FlaskForm):
    nombre_destinatario=StringField('Nombre del Destinatario',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=2,max=100,message='2-100 caracteres requeridos')
    ])

    domicilio=StringField('Domcilio',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=50,message='3-50 caracteres requeridos')
    ])

    localidad=StringField('Localidad',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=25,message='3-25 caracteres requeridos')
    ])

    puerta=StringField('Puerta',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=1,max=10,message='1-10 caracteres requeridos')
    ])

    codigo_postal=StringField('Código Postal',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=4,max=10,message='4-10 caracteres requeridos'),
        validar_digitos
    ])


    submit=SubmitField('Continuar')




#Formulario para el pago
class Payment(FlaskForm):
    nombre_titular=StringField('Nombre del Titular',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=2,max=100,message='2-100 caracteres requeridos')
    ])

    numero_tarjeta=StringField('Número de Tarjeta',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=13,max=19,message='13-19 caracteres requeridos'),
        validar_digitos
    ])

    cvv=StringField('CVV',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=4,message='3-4 caracteres requeridos'),
        validar_digitos
    ])

    year=IntegerField('Año',validators=[
        DataRequired(message="Este campo es obligatorio"),
        validar_year
    ])

    mes=IntegerField('Mes',validators=[
        DataRequired(message="Este campo es obligatorio"),
        NumberRange(min=1,max=12),
        validar_mes
    ])


    submit=SubmitField('Efectuar pago')

    
    