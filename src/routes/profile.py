from flask import Blueprint,redirect,url_for,render_template,abort,flash,current_app,request
from flask_login import current_user
from formularios_WTF.forms import Account,AddressForm
from models.ModelUser import ModelUser
from models.ModelProduct import ModelProduct
from models.entities.Address import Address
from models.entities.User import User
from models.entities.Order import Order
from models.ModelOrder import ModelOrder
from werkzeug.exceptions import HTTPException


profile_bp=Blueprint('profile',__name__,url_prefix='/profile')

def client_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if not current_user.rol=='client':
        abort(401)

    else:
        return True


#Ruta raiz
@profile_bp.route('/',methods=['GET','POST'])
def profile():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Redirijimos a la cuenta del cliente
            return redirect(url_for('profile.account'))
        
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin')
        print(error)
        abort(404)



#Rutas de Datos de cuenta
@profile_bp.route('/account',methods=['GET','POST'])
def account():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            
            #Obtenemos el cursor de la db y el formulario de datos de cuenta
            db=current_app.config['db']
            form=Account()

            datos=User(current_user.id,current_user.nombre,current_user.apellidos,current_user.email,current_user.username,None,None)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                
                #Obtenemos todos lod datos del formulario
                nombre=request.form.get('nombre')
                apellidos=request.form.get('apellidos')
                email=request.form.get('email')
                username=request.form.get('username')
            
                print(nombre,apellidos,email,username)

                datos_nuevos=User(current_user.id,nombre,apellidos,email,username,None,None)


                #Intentamos cambiar los datos de cuenta
                datos_cambiados=ModelUser.setAccount(db,datos_nuevos)

                #Si los datos han sido cambiados
                if datos_cambiados:
                    print('Datos cambaidos con exitillo')
                    flash('Datos cambiados con éxito')

                    return redirect(url_for('profile.account'))

                #Sino indicamos el error
                else:
                    flash('Error al cambiar los datos de cuenta')
                    return render_template('profile/account.html',form=form,datos=datos)


            #Sino      
            else:
                return render_template('profile/account.html',form=form,datos=datos)
    
    
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/account')
        print(error)
        abort(404)


@profile_bp.route('/delete_account',methods=['GET'])
def delete_account():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Eliminamos la cuenta
            eliminado=ModelUser.deleteAccount(db,current_user.id)

            #Si el usuario fue elimiando, redirijimos a inicio
            if eliminado:
                return redirect(url_for('home.home'))
            
            #Sino indicamos el error
            else:
                flash('Error al borrar al usuario')
                return redirect(url_for('profile.account'))

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/delete_account')
        print(error)
        abort(404)




#Rutas de Direccion de Envio

@profile_bp.route('/address',methods=['GET','POST'])
def address():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            
            #Obtenemos el cursor de la db y el formulario
            db=current_app.config['db']
            form=AddressForm()

            direccion_antigua=ModelUser.getAddress(db,current_user.id)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                
                #Obtenemos todos los datos del formulario de direccion de envio
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
                    flash('Datos cambiados con éxito')

                    return redirect(url_for('profile.address'))

                #Sino indicamos el error
                else:
                    flash('Error al cambiar la dirección de Envío')
                    return render_template('profile/address.html',form=form,direccion_antigua=direccion_antigua)

            #Sino      
            else:
                return render_template('profile/address.html',form=form,direccion_antigua=direccion_antigua)
    
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/address')
        print(error)
        abort(404)




@profile_bp.route('/delete_address',methods=['GET'])
def delete_address():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Borramos la direccion
            direccion_eliminada=ModelUser.deleteAddress(db,current_user.id)

            #Si fue borrada, mostramos el fomulario vacio
            if direccion_eliminada:
                flash('Dirección borrada con éxito')
                return redirect(url_for('profile.address'))
            
            #Sino, indicamos el error
            else:
                flash('Error al borrar la dirección')
                return redirect(url_for('profile.address'))
      
    
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/delete_address')
        print(error)
        abort(404)




#Ruta de Favoritos
@profile_bp.route('/favorites',methods=['GET'])
def favorites():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Obtenemos los productos favoritos
            productos=ModelProduct.mostrar_favoritos(db,current_user.id)

            return render_template('profile/favorites.html',productos=productos)
            

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/favorites')
        print(error)
        abort(404)



@profile_bp.route('/addFavorites/<id>',methods=['GET'])
def addFavorites(id):
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Agregamos a favoritos
            agregado=ModelProduct.addFavorites(db,current_user.id,id)

            #Si el producto fue añadido a favoritos
            if agregado:
                #Si es true, mostramos el mensaje de añadido
                if agregado==True:
                    return redirect(url_for('profile.favorites'))
                
                #Sino, mostramos el mensaje de error que nos llega del metodo addFavorites
                else: 
                    flash(agregado)

                return redirect(url_for('product.product',id=id))
            
            #Sino mostramos el mensaje de error
            else:
                return redirect(url_for('product.product',id=id))
            

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/addFavorites')
        print(error)
        abort(404)




@profile_bp.route('/deleteFavorites/<id>',methods=['GET'])
def deleteFavorites(id):
    try:
        print('El id',id)
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Borramos de favoritos el producto
            borrado=ModelProduct.deleteFavorites(db,current_user.id,id)

            #Si el producto fue borrado
            if borrado:

                #Si estamos en la pagina del producto, msotramos el mensaje de borrado
                if request.referrer and '/product' in request.referrer:
                    flash('Producto quitado de Favoritos')
                    return redirect(url_for('product.product',id=id))
                
                #Sino mostramos de nuevo la pagina de favoritos(Veremos que el producto ya no está)
                else:
                    return redirect(url_for('profile.favorites'))
            
            #Sino mostramos el error de borrado en el producto en sí
            else:
                flash('Error al borrar producto de Favoritos')
                return redirect(url_for('product.product',id=id))
            

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/deleteFavorites')
        print(error)
        abort(404)


#Ruta de Pedidos
@profile_bp.route('/orders',methods=['GET'])
def orders():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Obtenemos los pedidos
            pedidos=ModelOrder.showOrders(db,current_user.id)

            return render_template('profile/orders.html',pedidos=pedidos)
            

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/orders')
        print(error)
        abort(404)



@profile_bp.route('/order/<num>',methods=['GET'])
def order(num):
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Obtenemos el pedido
            pedido=ModelOrder.showFullOrder(db,current_user.id,num)

            #Si existe el pedido
            if pedido:
                #Obtenemos los productos comprados en el pedido
                productos=ModelOrder.getOrderProducts(db,pedido.id)

                return render_template('profile/order.html',pedido=pedido,productos=productos)
            
            #Sino, mandamos 404
            else:
                abort(404)
            

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/order')
        print(error)
        abort(404)


@profile_bp.route('/delete_order/<id>',methods=['GET'])
def delete_order(id):
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Eliminamos el producto
            eliminado=ModelOrder.deleteOrder(db,current_user.id,id)

            #Si el producto fue eliminado
            if eliminado:
                #Mandamos a los pedidos
                return redirect(url_for('profile.orders'))
            
            #Sino, mandamos al 404
            else:
                abort(404)
            

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /profile/delete_order')
        print(error)
        abort(404)









    