from flask import Blueprint,abort,redirect,url_for,render_template,current_app,request,flash
from flask_login import current_user

from formularios_WTF.forms import AddressForm,Payment
from models.entities.Address import Address
from models.ModelUser import ModelUser
from models.ModelOrder import ModelOrder
from services.CartService import CartService

from utils.TokenManager import TokenManager
from utils.MailSender import MailSender

from werkzeug.exceptions import HTTPException

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
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Redirijimos al checkout token, donde se creara el token 
            return redirect(url_for('checkout.checkout_token'))
        
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin')
        print(error)
        abort(404)


@checkout_bp.route('/checkout_token',methods=['GET'])
def checkout_token():
    try:
        check=client_required()
        if check!=True:
            return check
            
        else:
            #Obtenemos el cursor de la db y el formulario del register
            db=current_app.config['db']

            cursor=db.connection.cursor()

            sql='SELECT COUNT(*) FROM carrito WHERE id_usuario=%s'
            cursor.execute(sql,(current_user.id,))

            cantidad_productos=cursor.fetchone()[0]

            if cantidad_productos:
                token=TokenManager.create_token(current_user.email,5,current_app.config['JWT_SECRET_KEY_RESET_CART'],'address')

                return redirect(url_for('checkout.address',token=token))

            else:
                abort(404)

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /checkout/checkout_token')
        print(error)
        abort(404)



@checkout_bp.route('/address/<token>',methods=['GET','POST'])
def address(token):
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            token_decode=TokenManager.validate_token(token,current_app.config['JWT_SECRET_KEY_RESET_CART'])
            
            if not token_decode:
                return render_template('token_error.html')
            
            if token_decode['step']!='address':
                abort(404)
            
            #Obtenemos el cursor de la db y el formulario del register
            db=current_app.config['db']
            form=AddressForm()

            print(token_decode)
            
            direccion_antigua=ModelUser.getAddress(db,current_user.id)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                
                #Obtenemos todos lod datos del formulario de direccion de envio
                nombre_destinatario=request.form.get('nombre_destinatario')
                domicilio=request.form.get('domicilio')
                localidad=request.form.get('localidad')
                puerta=request.form.get('puerta')
                codigo_postal=request.form.get('codigo_postal')

                print(nombre_destinatario,domicilio,localidad,puerta,codigo_postal)

                #Creamos la direccion con los datos
                direccion=Address(nombre_destinatario,domicilio,localidad,puerta,codigo_postal,current_user.id)

                #Intentamos cambiar la direccion del usuario
                direccion_asignada=ModelUser.setAddress(db,direccion)

                #Si la direccion se ha asignado correctamente
                if direccion_asignada:
                    print('Direccion asignada con exitillo')

                    new_token=TokenManager.create_token(current_user.email,5,current_app.config['JWT_SECRET_KEY_RESET_CART'],'payment')
                    
                    return redirect(url_for('checkout.payment',token=new_token))

                #Sino indicamos el error
                else:
    
                    flash('Error al determinar la dirección de Envío')
                    return render_template('checkout/address.html',form=form,direccion_antigua=direccion_antigua,token=token)

            #Sino      
            else:
                return render_template('checkout/address.html',form=form,direccion_antigua=direccion_antigua,token=token)
    
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /checkout/address/token')
        print(error)
        abort(404)
    


@checkout_bp.route('/payment/<token>',methods=['GET','POST'])
def payment(token):
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            token_decode=TokenManager.validate_token(token,current_app.config['JWT_SECRET_KEY_RESET_CART'])
            if not token_decode:
                return render_template('token_error.html')
            
            if token_decode['step']!='payment':
                abort(404)
            
            #Obtenemos el cursor de la db y el formulario
            db=current_app.config['db']
            form=Payment()

            
            print(token_decode)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                crear_pedido=CartService.makePedido(db,current_user.id)

                #SI se nos devuelve el numero del pedido, el pedido ha sido creado
                if crear_pedido:
                    print('Pedido creado')
                    
                    numero_pedido=crear_pedido
                    
                    #Enviamos el email con los detalles
                    pedido=ModelOrder.showFullOrder(db,current_user.id,numero_pedido)

                    print('El pedido:',pedido)

                    #Si existe el pedido
                    if pedido:
                        #Obtenemos los productos comprados en el pedido
                        productos=ModelOrder.getOrderProducts(db,pedido.id)
                        print('Los productos:',productos)


                        #Enviamos un email que confirma nuestro pedido
                        MailSender.confirmOrder(current_app,current_user.email,current_user.username,pedido,productos,request.host_url)
                    
                    else:
                        flash('No se ha podido enviar el correo')

                    new_token=TokenManager.create_token(current_user.email,1,current_app.config['JWT_SECRET_KEY_RESET_CART'],'success')
                    return redirect(url_for('checkout.success',token=new_token))

                else:
                    flash('Error al tramitar el pago')
                    return render_template('checkout/payment.html',form=form,token=token)

            #Sino      
            else:
                return render_template('checkout/payment.html',form=form,token=token)
    
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /checkout/payment')
        print(error)
        abort(404)


@checkout_bp.route('/success/<token>',methods=['GET','POST'])
def success(token):
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            token_decode=TokenManager.validate_token(token,current_app.config['JWT_SECRET_KEY_RESET_CART'])
            
            if not token_decode:
                return render_template('token_error.html')
            
            if token_decode['step']!='success':
                abort(404)

            return render_template('checkout/success.html')
    
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /checkout/success')
        print(error)
        abort(404)


