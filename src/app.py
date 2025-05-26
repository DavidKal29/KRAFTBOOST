from flask import Flask,render_template
from flask_login import LoginManager
from flask_mail import Mail
from os import getenv
from config import config
from dotenv import load_dotenv
from flask_mysqldb import MySQL

#Modelos
from models.ModelBrand import ModelBrand
from models.ModelCategory import ModelCategory
from models.ModelUser import ModelUser

#Blueprints
from routes.home import home_bp
from routes.shop import shop_bp
from routes.page_product import product_bp
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.cart import cart_bp
from routes.checkout import checkout_bp
from routes.logout import logout_bp
from routes.admin import admin_bp


load_dotenv()

#Creamos la app de flask
app=Flask(__name__)

#Establecemos la configuración de la app
app.config.from_object(config['development'])

#Conexión de la base de datos
db=MySQL(app)

#Conexión al email
mail=Mail(app)

#Añadimos la db al config de app
app.config['db']=db

#Añadimos el mail al config de app
app.config['mail']=mail


#Creamos el login manager
login_manager=LoginManager(app)

#Creamos la función que se encarge de cargar al usuario a través de su id
@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)


#Registro de blueprints
app.register_blueprint(home_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(product_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(admin_bp)


#Pagina 404
def error_404(error):
    return render_template('404.html')

#Registramos en el manejador de errores el 404 en flask
app.register_error_handler(404,error_404)

#Pagina 401
def error_401(error):
    return render_template('401.html')

#Registramos en el manejador de errores el 401 en flask
app.register_error_handler(401,error_401)


#Utilizamos el contexto de la app porque estamos haciendo una consulta fuera de las rutas
with app.app_context():
    #Obtenemos el numero de productos totales
    try: 
        cursor=db.connection.cursor()

        #Obtenemos de los models, listas con estos objetos
        marcas=ModelBrand.mostrar_marcas(db)
        categorias=ModelCategory.mostrar_categorias(db)
        
        cursor.close()

        #Creamos los precios que habrán para filtrar
        precios={
            "0.99-5":"1€ - 5€",
            "4.99-10":"5€ - 10€",
            "9.99-15":"10€ - 15€",
            "14.99-20":"15€ - 20€",
            "19.99-25":"20€ - 25€",
            "24.99-30":"25€ - 30€",
            "29.99-35":"30€ - 35€",
            "34.99-50":"35€ - 50€",
            "49.99-100":"50€ - 100€",
            "99.99-200":"100€ - 200€",
            "199.99-400":"200€ - 400€"
        }

        


        #Lo guardamos en config para que desde los bp se pueda acceder
        app.config['marcas']=marcas
        app.config['categorias']=categorias
        app.config['precios']=precios


    except Exception as error:
        print('Error a la hora de obtener el numero de productos:',error)




if __name__=='__main__':
    app.run()