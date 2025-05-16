from flask import Blueprint,redirect,url_for,render_template,request,current_app,flash
from models.ModelUser import ModelUser
from models.entities.User import User

#Formularios WTF
from formularios_WTF.forms import Register

auth_bp=Blueprint('auth',__name__,url_prefix='/auth')


@auth_bp.route('/',methods=['GET','POST'])
def auth():
    return redirect(url_for('auth.login'))



@auth_bp.route('/login',methods=['GET','POST'])
def login():
    return render_template('auth/login.html')



@auth_bp.route('/register',methods=['GET','POST'])
def register():
    db=current_app.config['db']

    form=Register()

    if form.validate() and request.method=='POST':
        print('Caiste en el post')
        nombre=request.form.get('nombre')
        apellidos=request.form.get('apellidos')
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')

        print(nombre,apellidos,email,username,password)

        user=User(None,nombre,apellidos,email,username,password,rol='client')

        registered_user=ModelUser.register(db,user)

        print('El user:',registered_user)

        if registered_user:
            return render_template('auth/login.html')
 
        else:
            flash('Email o Username ya están en uso')
            return render_template('auth/register.html',form=form)
            

    else:
        print('Caiste en el get')
        return render_template('auth/register.html',form=form)
    

        


