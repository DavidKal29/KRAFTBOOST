from flask import Blueprint,redirect,url_for

auth_bp=Blueprint('auth',__name__,url_prefix='/auth')


@auth_bp.route('/',methods=['GET','POST'])
def auth():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    return 'Este es el login de auth'

@auth_bp.route('/register',methods=['GET','POST'])
def register():
    return 'Este es el register de auth'


