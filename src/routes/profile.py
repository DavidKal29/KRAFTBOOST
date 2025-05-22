from flask import Blueprint,redirect,url_for,render_template,abort,flash,current_app,request
from flask_login import current_user
from flask_login import login_required
from formularios_WTF.forms import Account,AddressForm
from models.ModelUser import ModelUser
from models.entities.Address import Address


profile_bp=Blueprint('profile',__name__,url_prefix='/profile')

def client_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if not current_user.rol=='client':
        abort(401)

    else:
        return True


@profile_bp.route('/',methods=['GET','POST'])
@login_required
def profile():
    return redirect(url_for('profile.account'))


@profile_bp.route('/account',methods=['GET','POST'])
@login_required
def account():

    form=Account()
    
    
    return render_template('profile/account.html',form=form)

@profile_bp.route('/address',methods=['GET','POST'])
@login_required
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
                    direccion_nueva=ModelUser.getAddress(db,current_user.id)

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
@login_required
def delete_address():
    try:
        check=client_required()
        if check!=True:
            return check
        
        else:
            
            #Obtenemos el cursor de la db y el formulario del register
            db=current_app.config['db']
            form=AddressForm()

            direccion_eliminada=ModelUser.deleteAddress(db,current_user.id)

            if direccion_eliminada:
                return redirect(url_for('profile.address'))
            
            else:
                flash('Error al borrar la dirección')
                return render_template('profile/address.html',form=form)

            
    
    #Cualquier error nos lleva a home
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)



    