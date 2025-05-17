from flask import Blueprint,redirect,url_for,render_template,request,current_app,flash
from flask_login import login_user,current_user
from models.ModelUser import ModelUser
from models.entities.User import User

#Enviador de Correos
from utils.MailSender import MailSender

#Formularios WTF
from formularios_WTF.forms import Register,Login,EmailRecuperacion

auth_bp=Blueprint('auth',__name__,url_prefix='/auth')


@auth_bp.route('/',methods=['GET','POST'])
def auth():
    return redirect(url_for('auth.login'))



@auth_bp.route('/login',methods=['GET','POST'])
def login():
    try:
        #Obtenemos el cursor de la db, y el formulario de login
        db=current_app.config['db']
        form=Login()

        #Si el metodo es post y se valida el formulario
        if form.validate() and request.method=='POST':
            
            #Obtenemos el email y el password
            email=request.form.get('email')
            password=request.form.get('password')
            
            print(email,password)

            #Creamos al usuario con User, solo con email y password
            user=User(None,None,None,email,None,password,None)

            #Intentamos encontrar al usuario con ModelUser.login
            logged_user=ModelUser.login(db,user)

            #Si el usuario fue encontrado
            if logged_user:
                #Si si contraseña está bine
                if logged_user.password:
                    #Lo logueamos y llevamos a perfil
                    login_user(logged_user)
                    return redirect(url_for('profile.profile'))
                #Sino
                else:
                    #Contraseña incorrecta, lo llevamos a login
                    flash('Email o Contraseña Incorrectos')
                    return render_template('auth/login.html',form=form)
            #Sino        
            else:
                #EMail incorrecto, lo llevamos a login otra vez
                flash('Email o Contraseña Incorrectos')
                return render_template('auth/login.html',form=form)
            

        #Si cae en get 
        else:
            #Si estamos logueados
            if current_user.is_authenticated:
                #Redirijir a perfil
                return redirect(url_for('profile.profile'))
            #Sino
            else:
                #Redirijir a login otra vez
                return render_template('auth/login.html',form=form)
    
    #Cualquier otro error, al home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        return redirect(url_for('home.home'))
    



@auth_bp.route('/register',methods=['GET','POST'])
def register():
    try:
        #Obtenemos el cursor de la db y el formulario del register
        db=current_app.config['db']
        form=Register()

        #Si el metodo es post y se valida el formulario
        if form.validate() and request.method=='POST':
            
            #Obtenemos todos lod datos del formulario de register
            nombre=request.form.get('nombre')
            apellidos=request.form.get('apellidos')
            email=request.form.get('email')
            username=request.form.get('username')
            password=request.form.get('password')

            print(nombre,apellidos,email,username,password)

            #Creamos al user con esos datos
            user=User(None,nombre,apellidos,email,username,password,rol='client')

            #Intentamos registrar al user con ModelUser.regisster
            registered_user=ModelUser.register(db,user)

            print('El user:',registered_user)

            #Si el usuario se registró con éxito
            if registered_user:
                
                #Enviamos el correo de bienvenida
                MailSender.welcome_message(current_app,registered_user.username,registered_user.email)

                #Logueamos al usuario obtenido de la db directamente
                login_user(registered_user)
                return redirect(url_for('profile.profile'))

            #Sino
            else:
                #Si no deja registrar, debe haber un error de duplicate seguramente
                flash('Email o Username ya están en uso')
                return render_template('auth/register.html',form=form)
            
            
        else:
            #SI estamos logueados
            if current_user.is_authenticated:
                #Redirijir a perfil
                return redirect(url_for('profile.profile'))
            
            #Sino
            else:
                #Redirijir a register
                return render_template('auth/register.html',form=form)
    
    #Cualquier error nos lleva a home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        return redirect(url_for('home.home'))
    


@auth_bp.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    try:
        #Obtenemos el cursor de la db, y el formulario de login
        db=current_app.config['db']
        form=EmailRecuperacion()

        #Si el metodo es post y se valida el formulario
        if form.validate() and request.method=='POST':
            
            #Obtenemos el email y el password
            email=request.form.get('email')
            
            print(email)

            #Validamos el email para ver si existe en la db
            validation=ModelUser.validate_email(db,email)

            #Si hay validacion avisa que se envió el correo
            if validation:
                flash('Correo Enviado con Éxito')
                return render_template('auth/forgot_password.html',form=form)
            
            #Sino, avisa que el correo no existe
            else:
                flash('Correo No Encontrado en los Registros')
                return render_template('auth/forgot_password.html',form=form)
                
            
        #Si cae en get 
        else:
            #Si estamos logueados
            if current_user.is_authenticated:
                #Redirijir a perfil
                return redirect(url_for('profile.profile'))
            #Sino
            else:
                #Redirijir a forgot password otra vez
                return render_template('auth/forgot_password.html',form=form)
    
    #Cualquier otro error, al home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        return redirect(url_for('home.home'))

            
    
    

        


