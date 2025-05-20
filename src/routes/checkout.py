from flask import Blueprint,abort,redirect,url_for,render_template,current_app,request,flash
from flask_login import current_user

from formularios_WTF.forms import AddressForm,Payment
from models.entities.Address import Address
from models.ModelUser import ModelUser

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
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db y el formulario del register
            db=current_app.config['db']
            form=AddressForm()

            direccion_antigua=ModelUser.getAddress(db,current_user.id)

            print(1)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                print('cAISTE EN EL POST')
                
                #Obtenemos todos lod datos del formulario de direccion de envio
                nombre_destinatario=request.form.get('nombre_destinatario')
                domicilio=request.form.get('domicilio')
                localidad=request.form.get('localidad')
                puerta=request.form.get('puerta')
                codigo_postal=request.form.get('codigo_postal')

                print(2)

                print(nombre_destinatario,domicilio,localidad,puerta,codigo_postal)

                #Creamos la direccion con los datos
                direccion=Address(nombre_destinatario,domicilio,localidad,puerta,codigo_postal,current_user.id)
                print(3)

                #Intentamos cambiar la direccion del usuario
                direccion_asignada=ModelUser.setAddress(db,direccion)
                print(4)
                
                #Si la direccion se ha asignado correctamente
                if direccion_asignada:
                    print('Direccion asignada con exitillo')
                    
                    return redirect(url_for('checkout.payment'))

                #Sino indicamos el error
                else:
                    print(5)
                    

                    flash('Error al determinar la dirección de Envío')
                    return render_template('checkout/address.html',form=form,direccion_antigua=direccion_antigua)
                
                
            else:
                print(6)
                print('cAISTE EN EL GET')
                return render_template('checkout/address.html',form=form,direccion_antigua=direccion_antigua)
    
    #Cualquier error nos lleva a home
    except Exception as error:
        print(88888)
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        return redirect(url_for('home.home'))
    


@checkout_bp.route('/payment',methods=['GET','POST'])
def payment():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db y el formulario del register
            db=current_app.config['db']
            form=Payment()

            print(1)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                print('cAISTE EN EL POST')
                
                
                return redirect(url_for('checkout.success'))
                
                
            else:
                print(6)
                print('cAISTE EN EL GET')
                return render_template('checkout/payment.html',form=form)
    
    #Cualquier error nos lleva a home
    except Exception as error:
        print(88888)
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        return redirect(url_for('home.home'))


@checkout_bp.route('/success',methods=['GET','POST'])
def success():
    check=client_required()
    if check!=True:
        return check
    
    else:

        return render_template('checkout/success.html')
        


