from flask import Blueprint,redirect,url_for,render_template,request,current_app,flash,abort
from flask_login import login_user,current_user
from models.ModelUser import ModelUser
from models.entities.User import User

#Enviador de Correos
from utils.MailSender import MailSender

#Manejador de Tokens
from utils.TokenManager import TokenManager

#Formularios WTF
from formularios_WTF.forms import Register,Login,EmailRecuperacion,ChangePassword

auth_bp=Blueprint('auth',__name__,url_prefix='/auth')


#Ruta de /auth
@auth_bp.route('/',methods=['GET','POST'])
def auth():
    try:
        #Retornamos a login
        return redirect(url_for('auth.login'))
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /auth')
        print(error)
        abort(404)


#Ruta de login
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
                #Si si contraseña está bien
                if logged_user.password:
                    #Lo logueamos y llevamos a perfil dependiendo del rol
                    login_user(logged_user)

                    #Si es admin lo lleva a admin
                    if logged_user.rol=='admin':
                        return redirect(url_for('admin.admin'))
                    
                    #Si es cliente, lo lleva al perfil
                    if logged_user.rol=='client':
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
                #Si es admin lo lleva a admin
                    if current_user.rol=='admin':
                        return redirect(url_for('admin.admin'))
                    
                    #Si es cliente, lo lleva al perfil
                    if current_user.rol=='client':
                        return redirect(url_for('profile.profile'))
            #Sino
            else:
                #Redirijir a login otra vez
                return render_template('auth/login.html',form=form)
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /auth/login')
        print(error)
        abort(404)
    


#Ruta de register
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
            #Si estamos logueados
            if current_user.is_authenticated:
                #Si es admin lo lleva a admin
                    if current_user.rol=='admin':
                        return redirect(url_for('admin.admin'))
                    
                    #Si es cliente, lo lleva al perfil
                    if current_user.rol=='client':
                        return redirect(url_for('profile.profile'))
            
            #Sino
            else:
                #Redirijir a register
                return render_template('auth/register.html',form=form)
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /auth/register')
        print(error)
        abort(404)
    

#Ruta de olvidaste contraseña
@auth_bp.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    try:
        #Obtenemos el cursor de la db, y el formulario para enviar email
        db=current_app.config['db']
        form=EmailRecuperacion()
        print('EL request host:',request.host_url)

        #Si el metodo es post y se valida el formulario
        if form.validate() and request.method=='POST':
            
            #Obtenemos el email y el password
            email=request.form.get('email')
            
            print(email)

            #Validamos el email para ver si existe en la db
            validation=ModelUser.validate_email(db,email)

            #Si hay validacion avisa que se envió el correo
            if validation:

                #Pasamos el email, tiempo de exp y el secret key(el None es el step, que en este caso no hace falta)
                token=TokenManager.create_token(email,2,current_app.config['JWT_SECRET_KEY_RESET_PASSWORD'],None)

                #Enviamos el email
                MailSender.reset_password_message(current_app,email,request.host_url,token)

                #Mensaje de éxito
                flash('Correo Enviado con Éxito')

                #Devolvemos el template con la confirmacion
                return render_template('auth/forgot_password.html',form=form)
            
            #Sino, avisa que el correo no existe
            else:
                flash('Correo No Encontrado en los Registros')
                return render_template('auth/forgot_password.html',form=form)
                
            
        #Si cae en get 
        else:
            #Si estamos logueados
            if current_user.is_authenticated:
                #Si es admin lo lleva a admin
                    if current_user.rol=='admin':
                        return redirect(url_for('admin.admin'))
                    
                    #Si es cliente, lo lleva al perfil
                    if current_user.rol=='client':
                        return redirect(url_for('profile.profile'))
            #Sino
            else:
                #Redirijir a forgot password otra vez
                return render_template('auth/forgot_password.html',form=form)
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /auth/forgot_password')
        print(error)
        abort(404)
    

#Ruta cambiar contraseña
@auth_bp.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    try:
    
        #Obtenemos el cursor de la db, y el formulario de reset password
        db=current_app.config['db']
        form=ChangePassword()

        #Decodeamos el token para ver si es valido
        token_decode=TokenManager.validate_token(token,current_app.config['JWT_SECRET_KEY_RESET_PASSWORD'])

        #Si el token no es valido, mandamos a la página de error de token
        if not token_decode:
            print(4)
            return render_template('token_error.html')
        

        #Si el metodo es post y se valida el formulario
        if form.validate() and request.method=='POST':
            
            #Obtenemos los passwords
            password=request.form.get('password')
            confirm=request.form.get('confirm')

            print(password,confirm)

            #Hacemos el cambio de password y lo asociamos a una variable para ver si se cambió
            validation=ModelUser.change_password(db,token_decode['email'],password)

            #Si todo salio bien mandamos el mensaje de éxito
            if validation:

                if validation=='Contraseñas iguales':
                    print('La nueva Contraseña no puede ser igual a la anterior')
                    flash('La nueva Contraseña no puede ser igual a la anterior')
                    return render_template('auth/reset_password.html',form=form,token=token)
                
                else:
                    print('Contraseña cambiada éxito')
                    flash('Contraseña cambiada éxito')
                    return render_template('auth/reset_password.html',form=form,token=token)


            #Sino, mandamos el mensaje de error
            else:
            
                print('Error al cambiar contraseña')
                flash('Error al cambiar contraseña')
                return render_template('auth/reset_password.html',form=form,token=token)
                     
        #Si cae en get 
        else:
            
            #Si estamos logueados
            if current_user.is_authenticated:
                #Si es admin lo lleva a admin
                    if current_user.rol=='admin':
                        return redirect(url_for('admin.admin'))
                    
                    #Si es cliente, lo lleva al perfil
                    if current_user.rol=='client':
                        return redirect(url_for('profile.profile'))
            #Sino
            else:
                
                #Redirijir a forgot password otra vez
                return render_template('auth/reset_password.html',form=form,token=token)
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO /auth/reset_password')
        print(error)
        abort(404)


            
    
    

        


