from flask import Blueprint,redirect,url_for,render_template,abort,flash,current_app,request
from flask_login import current_user
from formularios_WTF.forms import Account
from models.entities.User import User
from models.ModelUser import ModelUser
from models.ModelOrder import ModelOrder


admin_bp=Blueprint('admin',__name__,url_prefix='/admin')

#Método para ver si el usuario es admin
def admin_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if not current_user.rol=='admin':
        abort(401)

    else:
        return True
    

@admin_bp.route('/',methods=['GET','POST'])
def admin():
    return redirect(url_for('admin.account'))


#Rutas de Datos de cuenta
@admin_bp.route('/account',methods=['GET','POST'])
def account():
    try:
        check=admin_required()
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

                    return redirect(url_for('admin.account'))

                #Sino indicamos el error
                else:
                    flash('Error al cambiar los datos de cuenta')
                    return render_template('admin/account.html',form=form,datos=datos)


            #Sino      
            else:
                return render_template('admin/account.html',form=form,datos=datos)
    
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)



@admin_bp.route('/delete_account',methods=['GET'])
def delete_account():
    try:
        check=admin_required()
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
                return redirect(url_for('admin.account'))

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)


@admin_bp.route('/panel',methods=['GET'])
def panel():
    return redirect(url_for('admin.users'))


@admin_bp.route('/users',methods=['GET'])
def users():
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:    
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Obtenemos los usuarios
            users=ModelUser.getUsers(db,current_user.id)

    
            return render_template('admin/users.html',users=users)            
           

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)


@admin_bp.route('/edit_user/<id>',methods=['GET','POST'])
def edit_user(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:    
            #Obtenemos el cursor de la db y el formulario de datos de cuenta
            db=current_app.config['db']
            form=Account()


            datos=ModelUser.getUser(db,id)

            if not datos:
                abort(404)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                
                #Obtenemos todos lod datos del formulario
                nombre=request.form.get('nombre')
                apellidos=request.form.get('apellidos')
                email=request.form.get('email')
                username=request.form.get('username')
            
                print(nombre,apellidos,email,username)

                datos_nuevos=User(id,nombre,apellidos,email,username,None,None)


                #Intentamos cambiar los datos de cuenta
                datos_cambiados=ModelUser.setAccount(db,datos_nuevos)

                #Si los datos han sido cambiados
                if datos_cambiados:
                    print('Datos cambiados con exitillo')
                    flash('Datos cambiados')

                    return redirect(url_for('admin.edit_user',id=id))

                #Sino indicamos el error
                else:
                    flash('Error al cambiar los datos de cuenta')
                    return render_template('admin/editUser.html',form=form,datos=datos)


            #Sino      
            else:
                return render_template('admin/editUser.html',form=form,datos=datos)

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)


@admin_bp.route('/delete_user/<id>',methods=['GET'])
def delete_user(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Eliminamos al usuario
            eliminado=ModelUser.deleteAccount(db,id)

            #Si el usuario fue elimiando, redirijimos a los usuarios
            if eliminado:
                return redirect(url_for('admin.users'))
            
            #Sino indicamos el error
            else:
                return redirect(url_for('admin.edit_user',id=id))

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)






@admin_bp.route('/orders',methods=['GET'])
def orders():
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:    
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Obtenemos los pedidos

            pedidos=ModelOrder.showAllOrders(db)

    
            return render_template('admin/orders.html',pedidos=pedidos)            
           

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)



@admin_bp.route('/order/<id>',methods=['GET'])
def order(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Obtenemos el pedido
            pedido=ModelOrder.showFullOrderAdmin(db,id)

            #Si existe el pedido
            if pedido:
                #Obtenemos los productos comprados en el pedido
                productos=ModelOrder.getOrderProducts(db,id)

                return render_template('admin/order.html',pedido=pedido,productos=productos)
            
            #Sino, mandamos 404
            else:
                abort(404)
            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)


@admin_bp.route('/delete_order/<id>',methods=['GET'])
def delete_order(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Eliminamos el producto
            eliminado=ModelOrder.deleteOrderAdmin(db,id)

            #Si el producto fue eliminado
            if eliminado:
                #Mandamos a los pedidos
                return redirect(url_for('admin.orders'))
            
            #Sino, mandamos al 404
            else:
                abort(404)
            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)