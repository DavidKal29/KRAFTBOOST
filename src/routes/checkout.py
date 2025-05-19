from flask import Blueprint,abort,redirect,url_for
from flask_login import current_user

checkout_bp=Blueprint('checkout',__name__,url_prefix='/checkout')

def client_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if not current_user.rol=='client':
        abort(401)

    else:
        return True
    

@checkout_bp.route('/',methods=['GET'])
def checkout():

    return redirect(url_for('checkout.address'))

@checkout_bp.route('/address',methods=['GET','POST'])
def address():
    check=client_required()
    if check!=True:
        return check
    
    else:
        return 'Aqui irá el formulario de direccion'
    
@checkout_bp.route('/payment',methods=['GET','POST'])
def payment():
    check=client_required()
    if check!=True:
        return check
    
    else:
        return 'Aqui irá el formulario de pago'
        


