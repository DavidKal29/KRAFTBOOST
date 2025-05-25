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
import unidecode
import math


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


@admin_bp.route('/ordersUser/<id>',methods=['GET'])
def ordersUser(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:    
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            usuario_existe=ModelUser.get_by_id(db,id)

            if usuario_existe:

                #Obtenemos los pedidos
                pedidos=ModelOrder.showAllOrders(db,id)
                return render_template('admin/userOrders.html',pedidos=pedidos)   

            else:
                abort(404)         
           

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



@admin_bp.route('/setEnviadoOrder/<id>',methods=['GET'])
def setEnviadoOrder(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Activamos el producto
            activado=ModelOrder.setEnviadoOrder(db,id)

            #Si el producto fue activado
            if activado:
                #Mandamos a los productos
                return redirect(request.referrer or url_for('admin.orders'))
            
            #Sino, mandamos al 404
            else:
                abort(404)
            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)



@admin_bp.route('/products',methods=['GET','POST'])
def products():
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:    
            if request.method=='GET':
                #Variable que mirará si alguien puso algo raro en los filtros desde las rutas
                bugs=False
                
                #Marcamos los parámetros validos
                parametros_validos=['page','marca','categoria','precio','orden','search']
                
                #Obtenemos el db de la app
                db=current_app.config['db']

                #Obtenemos las marcas, categorias y precios de app
                marcas=current_app.config['marcas']
                categorias=current_app.config['categorias']
                precios=current_app.config['precios']


                #Obtenemos los parametros de filtrado
                orden=request.args.get('orden')
                search=request.args.get('search')
                marca=request.args.get('marca')
                categoria=request.args.get('categoria')
                precio=request.args.get('precio')


                #Creamos un diccionario y vemos si estos valores existen en la url
                parametros={}
                

                #Si el search existe y no es vacio,lo añadimos y au
                if search=='':
                    bugs=True
                    search=None

                elif search:
                    search=search.strip()
                    search=search.lower()
                    search=' '.join(search.split())
                    search=unidecode.unidecode(search)
                    parametros['search']=search
                        
                


                #Si la marca existe, es un numero y esta en el rango de len(marcas), 
                # se añade a parametros, sino se activa a True los bugs
                if marca:
                    if not marca.isdigit():
                        bugs=True
                    
                    elif int(marca)>len(marcas) or int(marca)<1:
                        bugs=True
                    
                    else:
                        parametros['marca']=int(marca)
                
                #Si la categoria existe, es un numero y esta en el rango de len(categorias), 
                # se añade a parametros, sino se activa a True los bugs
                if categoria:
                    if not categoria.isdigit():
                        bugs=True
                    
                    elif int(categoria)>len(categorias) or int(categoria)<1:
                        bugs=True
                    
                    else:
                        parametros['categoria']=int(categoria)

                #Si precio existe y esta en los rangos correctos se añade a paramtros sino bugs True
                if precio:
                    if precio in precios:
                        parametros['precio']=precio
                    else:
                        bugs=True

                
                #Miramos si no hay parametros que no deberian estar o hay parametros duplicados 
                for i in request.args.keys():
                    if i not in parametros_validos or len(request.args.getlist(i))>1:
                        bugs=True
                

                #Si el orden no existe, es un numero, o tiene un valor invalido, filtramos por los mas recientes
                if not orden or not orden.isalpha() or orden not in ['masRecientes','topVentas']:
                    orden='masRecientes'
                    bugs=True

                
                #Si no hay page, redirijimos a page 1
                if not request.args.get('page'):
                    bugs=True
                    page=1
                
                
                #Definimos el numero de paginas
                productos_por_pagina=12

                #Intento obtener el page en forma de int
                try:
                    page=int(request.args['page'])

                #Caerá aquí si el page contiene letras
                except Exception as error:
                    print(error)
                    page=1
                    bugs=True

                #Comprobamos por primera vez si no hay bugs
                if bugs:
                    return redirect(url_for('admin.products',page=page,orden=orden,**parametros))
                
                
                #Obtenemos el numero total de productos segun los parametros
                total=ModelProduct.mostrar_contador_productos(db,parametros,categorias,admin=True)
                
                
                #Si el numero total es un numero establecemos la pagina 
                # maxima a ese numero entre los productos por pagina 
                # redondeando al mayor por si da 1.5 o cosas asi, sino 1
                if total:
                    pagina_maxima=math.ceil(total/productos_por_pagina)
                else:
                    pagina_maxima=1

                    
                #Si el page es mayor a la pagina maxima, redirije a la pagina maxima
                if page>pagina_maxima:
                    page=pagina_maxima
                    bugs=True
                    
                #Si es menor a 1, lo lleva a 1
                elif page<1:
                    page=1
                    bugs=True
                    

                #Comprobamos por segunda vez si hay bugs
                if bugs:
                    return redirect(url_for('admin.products',page=page,orden=orden,**parametros))

                #Si porfin todo sale bien
                else:
                    #Obtenemos los productos con los filtros de la paginacion
                    productos=ModelProduct.mostrar_productos_paginacion(db,page,productos_por_pagina,orden,parametros,categorias,admin=True)
                

                return render_template('admin/products.html',
                                        paginas=pagina_maxima,productos=productos,
                                        page=page, parametros=parametros,
                                        marcas=marcas,categorias=categorias,precios=precios,orden=orden)
                
            
            
            elif request.method=='POST':
                #Lo mismo, creamos un diccionario y vemos si los parametros han sido seleccionados
                parametros={}
                
                #Obtenemos el search del formulario
                search=request.form.get('search')


                #Si está la metemos en los parametros
                if not  search:
                    search=request.args.get('search')

                if search:
                    #Quitar espacios, hacer todo en minusculas y quitar tildes
                    search=search.strip()
                    search=search.lower()
                    search=' '.join(search.split())
                    search=unidecode.unidecode(search)
                    
                    parametros['search']=search

                    

                #Obtenemos los parametros de los select
                orden=request.form.get('select_orden')
                marca=request.form.get('select_marca')
                categoria=request.form.get('select_categoria')
                precio=request.form.get('select_precio')

                
                #Obtenemos el page
                page=request.args.get('page')

                
                #Validamos que no sean values 0
                if marca and marca!='0':
                    parametros['marca']=marca
                
                if categoria and categoria!='0':
                    parametros['categoria']=categoria

                if precio and precio!='0':
                    parametros['precio']=precio

                print('Los parametrillos:',parametros)

                #Redirijimos con los parametros
                return redirect(url_for('admin.products',page=page,orden=orden,**parametros))        
            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)





@admin_bp.route('/setActiveProduct/<id>',methods=['GET'])
def setActiveProduct(id):
    try:
        check=admin_required()
        if check!=True:
            return check
        
        else:
            #Obtenemos el cursor de la db
            db=current_app.config['db']

            #Activamos el producto
            activado=ModelProduct.setActiveProduct(db,id)

            #Si el producto fue activado
            if activado:
                #Mandamos a los productos
                return redirect(request.referrer or url_for('admin.products'))
            
            #Sino, mandamos al 404
            else:
                abort(404)
            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)



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


            # #Si el metodo es post y se valida el formulario
            if form.validate() and request.method=='POST':
                
                #Obtenemos todos lod datos del formulario
                nombre=request.form.get('nombre')
                marca=int(request.form.get('marca'))             
                categoria=int(request.form.get('categoria'))
                precio=request.form.get('precio')
                stock=request.form.get('stock')
                descripcion=request.form.get('descripcion')
                
            
                print(nombre,marca,categoria,precio,stock,descripcion)

                producto=Product(id,nombre,precio,marca,categoria,descripcion,0,stock)

                actualizado=ModelProduct.setProduct(db,producto)

                if not actualizado:
                    flash('Error al actualizar el producto')

                else:
                    flash('Actualizado con éxito')

                return redirect(url_for('admin.edit_product',id=id))

            else:

                #Obtenemos el producto
                producto=ModelProduct.getProduct(db,id)

                if producto:

                    for marca in marcas:
                        if marca.nombre==producto.nombre_marca:
                            form.marca.data=int(marca.id)
                            print('Tipo de marca.id:',type(marca.id))

                    for categoria in categorias:
                        if categoria.nombre==producto.nombre_categoria:
                            form.categoria.data=int(categoria.id)
                            print('Tipo de categoria.id:',type(categoria.id))

                    form.descripcion.data=producto.descripcion

                    return render_template('admin/product.html',form=form,producto=producto)
                
                else:
                    abort(404)

            

    #Cualquier error nos lleva a 404
    except Exception as error:
        print('ERROR DETECTADO EN LA CONSOLA')
        print(error)
        abort(404)
