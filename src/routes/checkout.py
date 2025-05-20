from flask import Blueprint,abort,redirect,url_for,render_template
from flask_login import current_user

from formularios_WTF.forms import Address,Payment

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
        form=Address()

        return render_template('checkout/address.html',form=form)
    
@checkout_bp.route('/payment',methods=['GET','POST'])
def payment():
    check=client_required()
    if check!=True:
        return check
    
    else:
        form=Payment()

        return render_template('checkout/payment.html',form=form)


@checkout_bp.route('/success',methods=['GET','POST'])
def success():
    check=client_required()
    if check!=True:
        return check
    
    else:

        return render_template('checkout/success.html')
        


