from flask import Blueprint,abort,redirect,url_for,render_template,request
from flask_login import current_user


cart_bp=Blueprint('cart',__name__,url_prefix='/cart')


@cart_bp.route('/',methods=['GET','POST'])
def cart():
    if current_user.is_authenticated:
        print('EL current user rol:',current_user.rol)
        if current_user.rol=='client':
            return render_template('cart.html')
        else:
            abort(401)
    
    return redirect(url_for('auth.login'))


@cart_bp.route('/add_product',methods=['GET'])
def add_product(id):
    if current_user.is_authenticated:
        print('EL current user rol:',current_user.rol)
        if current_user.rol=='client':
            
            print('Aqui ira el codigo para añadir el producto')
            
            return render_template('cart.html')
        else:
            abort(401)
    
    return redirect(url_for('auth.login'))