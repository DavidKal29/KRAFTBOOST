from flask import Blueprint,redirect,url_for,render_template,abort,flash,current_app,request
from flask_login import current_user
from formularios_WTF.forms import Account,ProductForm
from models.entities.User import User
from models.ModelUser import ModelUser
from models.ModelOrder import ModelOrder
from models.ModelProduct import ModelProduct
from models.ModelBrand import ModelBrand
from models.ModelCategory import ModelCategory
from models.entities.Product import Product
from werkzeug.exceptions import HTTPException


admin_bp=Blueprint('admin',__name__,url_prefix='/admin')

#Método para ver si el usuario es admin
def admin_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if not current_user.rol=='admin':
        print('Abortamos al 401')
        abort(401)

    else:
        return True
    

#Ruta incial del perfil del admin
@admin_bp.route('/',methods=['GET','POST'])
def admin():
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            #Redirijimos a la cuenta del admin
            return redirect(url_for('admin.account'))
        
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin')
        print(error)
        abort(404)



#Rutas de Datos de cuenta del admin
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

            #Obtenemos los datos del current user
            datos=User(current_user.id,current_user.nombre,current_user.apellidos,current_user.email,current_user.username,None,None)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                
                #Obtenemos todos lod datos del formulario
                nombre=request.form.get('nombre')
                apellidos=request.form.get('apellidos')
                email=request.form.get('email').strip().lower()
                username=request.form.get('username').strip().replace(' ','')

                #Limpiamos el nombre
                nombre=' '.join(nombre.strip().split())
                nombre=nombre.title()

                #Limpiamos los apellidos
                apellidos=' '.join(apellidos.strip().split())
                apellidos=apellidos.title()
                
                
                print(nombre,apellidos,email,username)

                #Creamos el objeto con los nuevos datos
                datos_nuevos=User(current_user.id,nombre,apellidos,email,username,None,None)

                #Intentamos cambiar los datos de cuenta
                datos_cambiados=ModelUser.setAccount(db,datos_nuevos)

                #Si los datos han sido cambiados
                if datos_cambiados:
                    if datos_cambiados=='Datos iguales':
                        print('Los datos son iguales')
                        flash('Los datos son iguales')

                    else:
                        flash('Datos cambiados con éxito')

                    return redirect(url_for('admin.account'))

                #Sino indicamos el error
                else:
                    flash('Email o Username ya están en uso')
                    return render_template('admin/account.html',form=form,datos=datos)

            #Sino      
            else:
                return render_template('admin/account.html',form=form,datos=datos)
    
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
    
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR EN /admin/account')
        print(error)
        abort(404)





#Ruta para ver a todos los usuarios
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

            #Devolvemos los usuarios del admin
            return render_template('admin/users.html',users=users)            
    
    #Si cae en 401
    except HTTPException as http_err:
        raise http_err

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/users')
        print(error)
        abort(404)


#Ruta para editar al usuario
@admin_bp.route('/edit_user/<id>',methods=['GET','POST'])
def edit_user(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:    

            if str(id)==str(current_user.id):
                print('El id es igual al del admin')
                return redirect(url_for('admin.account'))
            
            print('El id no es igual')

            #Obtenemos el cursor de la db y el formulario de datos de cuenta
            db=current_app.config['db']
            form=Account()

            #Obtenemos al usuario
            datos=ModelUser.getUser(db,id)

            #Si no hay datos, mandamos al 404
            if not datos:
                abort(404)

            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                
                #Obtenemos todos lod datos del formulario
                nombre=request.form.get('nombre')
                apellidos=request.form.get('apellidos')
                email=request.form.get('email').strip().lower()
                username=request.form.get('username').strip().replace(' ','')

                #Limpiamos el nombre
                nombre=' '.join(nombre.strip().split())
                nombre=nombre.title()

                #Limpiamos los apellidos
                apellidos=' '.join(apellidos.strip().split())
                apellidos=apellidos.title()

                print(nombre,apellidos,email,username)

                datos_nuevos=User(id,nombre,apellidos,email,username,None,None)


                #Intentamos cambiar los datos de cuenta
                datos_cambiados=ModelUser.setAccount(db,datos_nuevos)

                #Si los datos han sido cambiados
                if datos_cambiados:
                    if datos_cambiados=='Datos iguales':
                        print('Los datos son iguales')
                        flash('Los datos son iguales')

                    else:
                        flash('Datos cambiados con éxito')

                    return redirect(url_for('admin.edit_user',id=id))

                #Sino indicamos el error
                else:
                    flash('Email o Username ya están en uso')
                    return render_template('admin/editUser.html',form=form,datos=datos)


            #Sino      
            else:
                return render_template('admin/editUser.html',form=form,datos=datos)
            

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/edit_user')
        print(error)
        abort(404)


#Ruta para borrar a los usuarios
@admin_bp.route('/delete_user/<id>',methods=['GET'])
def delete_user(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:

            if str(id)==str(current_user.id):
                print('El id es igual al del admin')
                return redirect(url_for('admin.account'))
            
            print('El id no es igual')
            
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
            

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/delete_user')
        print(error)
        abort(404)



#Ruta para ver los pedidos en general
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


    #Si cae en 401
    except HTTPException as http_err:
        raise http_err 
           

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/orders')
        print(error)
        abort(404)


#Ruta para ver los pedidos de un usuario
@admin_bp.route('/ordersUser/<id>',methods=['GET'])
def ordersUser(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:    
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Intentamos obtener al usuario
            usuario_existe=ModelUser.get_by_id(db,id)

            #Si existe
            if usuario_existe:

                #Obtenemos los pedidos
                pedidos=ModelOrder.showAllOrders(db,id)
                return render_template('admin/userOrders.html',pedidos=pedidos)   

            #Sino mandamos al 404
            else:
                abort(404)   


    #Si cae en 401
    except HTTPException as http_err:
        raise http_err 
           

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/ordersUser')
        print(error)
        abort(404)



#Ruta para ver los detalles de un pedido
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

            print('El pedido existe mira',pedido)

            #Si existe el pedido
            if pedido:
                #Obtenemos los productos comprados en el pedido
                productos=ModelOrder.getOrderProducts(db,id)

                print('El productos existen mira',productos)

                #Obtenemos la ruta desde donde ha llegado la peticion para redirijir ahi
                referrer=request.referrer

                return render_template('admin/order.html',pedido=pedido,productos=productos,referrer=referrer)
            
            #Sino, mandamos 404
            else:
                abort(404)

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
            
    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/order')
        print(error)
        abort(404)


#Ruta para borrar los pedidos
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
                return redirect(request.referrer or url_for('admin.orders'))
            
            #Sino, mandamos al 404
            else:
                abort(404)

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/delete_order')
        print(error)
        abort(404)


#Ruta para activar/desactivar el enviado del producto
@admin_bp.route('/setEnviadoOrder/<id>',methods=['GET'])
def setEnviadoOrder(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Activamos/Desactivamos el producto
            seteado=ModelOrder.setEnviadoOrder(db,id)

            #Si el producto fue seteado
            if seteado:
                #Mandamos a los pedidos en general, o a los pedidos del usuario en concreto
                return redirect(request.referrer or url_for('admin.orders'))
            
            #Sino, mandamos al 404
            else:
                abort(404)

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/setEnviadoOrder')
        print(error)
        abort(404)




#Importamos el metodo para manejar la paginacion, filtros y buscador del producto
from utils.PaginationProductsManager import productos_paginacion

#Ruta para obtener los productos para el admin
@admin_bp.route('/products',methods=['GET','POST'])
def products():
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            return productos_paginacion('admin.products','admin/products.html',admin=True)
         

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/products')
        print(error)
        abort(404)




#Ruta para activar/desactivar los productos
@admin_bp.route('/setActiveProduct/<id>',methods=['GET'])
def setActiveProduct(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Seteeamos el producto
            seteado=ModelProduct.setActiveProduct(db,id)

            #Si el producto fue seteado
            if seteado:

                #Mandamos a los productos o a la ruta desde la que hicimos la peticion
                return redirect(request.referrer or url_for('admin.products'))
            
            #Sino, mandamos al 404
            else:
                abort(404)

    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/setActiveProduct')
        print(error)
        abort(404)



#Ruta para editar el producto
@admin_bp.route('/edit_product/<id>',methods=['GET','POST'])
def edit_product(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            
            #Obtenemos el cursor de la db y el formulario de los productos
            db=current_app.config['db']
            form=ProductForm()

            #Obtenemos las marcas y categorias
            marcas=ModelBrand.mostrar_marcas(db)
            categorias=ModelCategory.mostrar_categorias(db)


            #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                
                #Obtenemos todos los datos del formulario
                nombre=request.form.get('nombre')
                marca=int(request.form.get('marca'))             
                categoria=int(request.form.get('categoria'))
                precio=request.form.get('precio')
                stock=request.form.get('stock')
                descripcion=request.form.get('descripcion').strip()

                #Limpiamos el nombre
                nombre=' '.join(nombre.strip().split())
                nombre=nombre.title()

                #Limpiamos la descripcion
                descripcion=' '.join(descripcion.strip().split())
                
                print(nombre,marca,categoria,precio,stock,descripcion)

                #Creamos el producto
                producto=Product(id,nombre,precio,marca,categoria,descripcion,0,stock)

                #Intentamos actualizarlo
                actualizado=ModelProduct.setProduct(db,producto)

                #Sino fue actualizado mandamso el error
                if not actualizado:
                    flash('Error al actualizar el producto')

                #Si salio bien todo, mensaje de exito
                else:
                    if actualizado=='Datos iguales':
                        print('Los datos son iguales')
                        flash('Los datos son iguales')

                    else:
                        flash('Datos cambiados con éxito')

                #Mandamos a la apgina de edicion del producto
                return redirect(url_for('admin.edit_product',id=id))

            else:

                #Obtenemos el producto
                producto=ModelProduct.getProduct(db,id)

                #Si se encuentra el producto
                if producto:

                    #Recorremos la marca, y la que sea del producto, 
                    # la establecemos en el select marca del formulario
                    for marca in marcas:
                        if marca.nombre==producto.nombre_marca:
                            form.marca.data=int(marca.id)
                            print('Tipo de marca.id:',type(marca.id))

                    #Recorremos la categoria, y la que sea del producto, 
                    # la establecemos en el select categoria del formulario
                    for categoria in categorias:
                        if categoria.nombre==producto.nombre_categoria:
                            form.categoria.data=int(categoria.id)
                            print('Tipo de categoria.id:',type(categoria.id))

                    #Ponemos la descripcion en el textarea de la descripcion
                    form.descripcion.data=producto.descripcion

                    return render_template('admin/product.html',form=form,producto=producto)
                
                else:
                    abort(404)


    #Si cae en 401
    except HTTPException as http_err:
        raise http_err
       

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN /admin/edit_product')
        print(error)
        abort(404)
