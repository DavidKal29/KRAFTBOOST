from flask import Blueprint,redirect,url_for,render_template

auth_bp=Blueprint('auth',__name__,url_prefix='/auth')


@auth_bp.route('/',methods=['GET','POST'])
def auth():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    return render_template('auth/login.html')

@auth_bp.route('/register',methods=['GET','POST'])
def register():
    return render_template('auth/register.html')


