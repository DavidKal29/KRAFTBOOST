from flask import Blueprint,redirect,url_for,render_template,request,current_app
from models.ModelUser import ModelUser
from models.entities.User import User

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

    if request.method=='GET':
        return render_template('auth/register.html')
    
    elif request.method=='POST':
        nombre=request.form.get('nombre')
        apellidos=request.form.get('apellidos')
        email=request.form.get('email')
        username=request.form.get('username')
        telefono=request.form.get('telefono')
        fecha_nacimiento=request.form.get('fecha_nacimiento')
        password=request.form.get('password')

        print(nombre,apellidos,email,username,telefono,fecha_nacimiento,password)


        user=User(None,nombre,apellidos,email,username,telefono,fecha_nacimiento,password,rol='client')



        ModelUser.register(db,user)


        return render_template('auth/register.html')


        


