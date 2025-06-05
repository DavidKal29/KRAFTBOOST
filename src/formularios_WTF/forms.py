from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField,IntegerField,DecimalField,TextAreaField,SelectField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError,NumberRange,InputRequired
import re
import unidecode

#validador de password
def validar_password(form, field):

    #Validamos que tenga al menos 1 minuscula, 1 mayuscula, 1 numero
    if not re.search(r'\d', field.data):
        raise ValidationError('Al menos 1 digito en la contraseña')

    if not re.search(r'[A-Z]', field.data):
        raise ValidationError('Al menos 1 mayúscula en la contraseña')

    if not re.search(r'[a-z]', field.data):
        raise ValidationError('Al menos 1 minúscula en la contraseña')
    
    if ' ' in field.data:
        raise ValidationError('La contraseña no puede contener espacios')
    

    
#Validador de fechas
def validar_year(form, field):
    from datetime import datetime

    year_actual=datetime.now().year

    if field.data<year_actual or field.data>2030:
        raise ValidationError('Año de expiración inválido')
    
def validar_mes(form, field):
    from datetime import datetime

    year_actual=datetime.now().year
    mes_actual=datetime.now().month

    if form.year.data<=year_actual and field.data<mes_actual:
        raise ValidationError('Mes de expiración inválido')
    

#Validador de letras
def validar_letras(form,field):
    texto=unidecode.unidecode(field.data)
    texto=texto.replace(' ','')

    if not texto.isalpha():
        raise ValidationError('Este campo solo puede tener letras')



#Validador de digitos
def validar_digitos(form,field):
    if not field.data.isdigit():
        raise ValidationError('Este campo solo puede tener dígitos')

    if field.data=='0':
        raise ValidationError('Este campo no puede ser cero')

    if field.data.lstrip('0')=='':
        raise ValidationError('No puede contener solo ceros')

    if field.data!=str(int(field.data)):
        raise ValidationError('No puede empezar con ceros innecesarios')
    


#Validador de alnum
def validar_alnum(form,field):
    texto=unidecode.unidecode(field.data)
    texto=texto.replace(' ','')
    if not texto.isalnum():
        raise ValidationError('Este campo solo puede tener alfanuméricos')
    

#Validar los domicilios
def validar_domicilio(form, field):
    texto=unidecode.unidecode(field.data)
    permitidos="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,#+-/ºª"
    
    for i in texto:
        if i not in permitidos:
            raise ValidationError('La dirección contiene caracteres no permitidos')
        

#Validar la descripcion de los productos
def validar_descripcion(form, field):
    texto=unidecode.unidecode(field.data)
    permitidos="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,;"
    
    for i in texto:
        if i not in permitidos:
            raise ValidationError('La descripción contiene caracteres no permitidos')

    

#Formulario de register
class Register(FlaskForm):

    nombre=StringField('Nombre',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=25,message='3-25 caracteres requeridos'),
        validar_letras
    ])

    apellidos=StringField('Apellidos',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=25,message='3-25 caracteres requeridos'),
        validar_letras
    ])

    email=EmailField('Correo electrónico',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=10,max=150,message='10-150 caracteres requeridos'),
        Email()
    ])

    username=StringField('Username',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=5,max=25,message='5-25 caracteres requeridos'),
        validar_alnum
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
        Length(min=2,max=100,message='2-100 caracteres requeridos'),
        validar_letras
    ])

    domicilio=StringField('Domcilio',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=50,message='3-50 caracteres requeridos'),
        validar_domicilio
    ])

    localidad=StringField('Localidad',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=25,message='3-25 caracteres requeridos'),
        validar_letras
    ])

    puerta=StringField('Puerta',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=1,max=3,message='1-3 caracteres requeridos'),
        validar_digitos
    ])

    codigo_postal=StringField('Código Postal',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=4,max=5,message='4-10 caracteres requeridos'),
        validar_digitos
    ])


    submit=SubmitField('Guardar Cambios')



#Formulario para el pago
class Payment(FlaskForm):
    nombre_titular=StringField('Nombre del Titular',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=2,max=100,message='2-100 caracteres requeridos'),
        validar_letras
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

    

#Formulario de cuenta
class Account(FlaskForm):

    nombre=StringField('Nombre',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=25,message='3-25 caracteres requeridos'),
        validar_letras
    ])

    apellidos=StringField('Apellidos',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=25,message='3-25 caracteres requeridos'),
        validar_letras
    ])

    email=EmailField('Correo electrónico',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=10,max=150,message='10-150 caracteres requeridos'),
        Email()
    ])

    username=StringField('Username',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=5,max=25,message='5-25 caracteres requeridos'),
        validar_alnum
    ])


    submit=SubmitField('Guardar Cambios')



#Formulario de producto
class ProductForm(FlaskForm):

    nombre=StringField('Nombre',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3,max=100,message='3-100 caracteres requeridos'),
        validar_alnum
    ])

    marca_choices=[(1,'Domyos'),(2,'Tunturi'),(3,'Kraftboost'),(4,'Corength'),(5,'Maniak'),(6,'E-series')]

    marca=SelectField('Marca',choices=marca_choices,coerce=int)

    categoria_choices=[(1,'Barras'),(2,'Bancos'),(3,'Discos'),(4,'Mancuernas'),(5,'Accesorios'),(6,'Bandas'),(7,'Kettlebells'),(8,'Estructuras')]
    
    categoria=SelectField('Categoría',choices=categoria_choices,coerce=int)

    precio=DecimalField('Precio',validators=[
        InputRequired(message="Este campo es obligatorio"),
        NumberRange(min=0.01, message="Debe ser positivo")
    ])

    stock=IntegerField('Stock',validators=[
        InputRequired(message="Este campo es obligatorio"),
        NumberRange(min=0)
    ])

    descripcion=TextAreaField('Descripcion',validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(max=255, message="Máximo 255 caracteres"),
        validar_descripcion
    ])


    submit=SubmitField('Guardar Cambios')