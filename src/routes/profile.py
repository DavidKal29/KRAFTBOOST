from flask import Blueprint,redirect,url_for,render_template,abort,flash,current_app,request
from flask_login import current_user
from formularios_WTF.forms import Account,AddressForm
from models.ModelUser import ModelUser
from models.ModelProduct import ModelProduct
from models.entities.Address import Address
from models.entities.User import User


profile_bp=Blueprint('profile',__name__,url_prefix='/profile')

def client_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if not current_user.rol=='client':
        abort(401)

    else:
        return True


@profile_bp.route('/',methods=['GET','POST'])
def profile():
    return redirect(url_for('profile.account'))


@profile_bp.route('/account',methods=['GET','POST'])
def account():

    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            
            #Obtenemos el cursor de la db y el formulario del register
            db=current_app.config['db']
            form=Account()

            datos=User(current_user.id,current_user.nombre,current_user.apellidos,current_user.email,current_user.username,None,None)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                
                #Obtenemos todos lod datos del formulario de direccion de envio
                nombre=request.form.get('nombre')
                apellidos=request.form.get('apellidos')
                email=request.form.get('email')
                username=request.form.get('username')
            
                print(nombre,apellidos,email,username)

                datos_nuevos=User(current_user.id,nombre,apellidos,email,username,None,None)


                #Intentamos cambiar los datos de cuenta
                datos_cambiados=ModelUser.setAccount(db,datos_nuevos)

                #Si la direccion se ha asignado correctamente
                if datos_cambiados:
                    print('Datos cambaidos con exitillo')

                    

                    return redirect(url_for('profile.account'))

                #Sino indicamos el error
                else:
                    flash('Error al cambiar los datos de cuenta')
                    return render_template('profile/account.html',form=form,datos=datos)


            #Sino      
            else:
                return render_template('profile/account.html',form=form,datos=datos)
    
    
    #Cualquier error nos lleva a home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
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

            eliminado=ModelUser.deleteAccount(db,current_user.id)

            if eliminado:
                return redirect(url_for('home.home'))
            
            else:
                flash('Error al borrar al usuario')
                return redirect(url_for('profile.account'))

            
    
    #Cualquier error nos lleva a home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)




@profile_bp.route('/address',methods=['GET','POST'])
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

                    return redirect(url_for('profile.address'))

                #Sino indicamos el error
                else:
                    flash('Error al cambiar la dirección de Envío')
                    return render_template('profile/address.html',form=form,direccion_antigua=direccion_antigua)

            #Sino      
            else:
                return render_template('profile/address.html',form=form,direccion_antigua=direccion_antigua)
    
    #Cualquier error nos lleva a home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
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

            direccion_eliminada=ModelUser.deleteAddress(db,current_user.id)

            if direccion_eliminada:
                return redirect(url_for('profile.address'))
            
            else:
                flash('Error al borrar la dirección')
                return redirect(url_for('profile.address'))

            
    
    #Cualquier error nos lleva a home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
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

            agregado=ModelProduct.addFavorites(db,current_user.id,id)

            
            if agregado:
                if agregado==True:
                    flash('Producto añadido a Favoritos')
                
                else: 
                    flash(agregado)

                return redirect(url_for('product.product',id=id))
            
            else:
                flash('Error al añadir producto')
                return redirect(url_for('product.product',id=id))
            

    #Cualquier error nos lleva a home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)



@profile_bp.route('/deleteFavorites/<id>',methods=['GET'])
def deleteFavorites(id):
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            borrado=ModelProduct.deleteFavorites(db,current_user.id,id)

            if borrado:

                if '/product' in request.referrer:
                    flash('Producto quitado de Favoritos')
                    return redirect(url_for('product.product',id=id))
                
                else:
                    return redirect(url_for('profile.favorites'))
            
            else:
                flash('Error al borrar producto de Favoritos')
                return redirect(url_for('product.product',id=id))
            

    #Cualquier error nos lleva a home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)







@profile_bp.route('/favorites',methods=['GET'])
def favorites():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            productos=ModelProduct.mostrar_favoritos(db,current_user.id)

            return render_template('profile/favorites.html',productos=productos)
            

    #Cualquier error nos lleva a home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)






    