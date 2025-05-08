from flask import Flask
from os import getenv
from config import config
from dotenv import load_dotenv
from flask_mysqldb import MySQL

#Modelos
from models.ModelBrand import ModelBrand
from models.ModelCategory import ModelCategory

#Blueprints
from routes.home import home_bp
from routes.shop import shop_bp



load_dotenv()

#Creamos la app de flask
app=Flask(__name__)

#Establecemos la configuración de la app
app.config.from_object(config['development'])

#Conexión de la base de datos
db=MySQL(app)

#Añadimos la db al config de app
app.config['db']=db


#Registro de blueprints
app.register_blueprint(home_bp)
app.register_blueprint(shop_bp)

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
            "1-5":"1€ - 5€",
            "5-10":"5€ - 10€",
            "10-15":"10€ - 15€",
            "15-20":"15€ - 20€",
            "20-25":"20€ - 25€",
            "25-30":"25€ - 30€",
            "30-35":"30€ - 35€",
            "35-50":"35€ - 50€",
            "50-100":"50€ - 100€",
            "100-200":"100€ - 200€",
            "200-400":"200€ - 400€"
        }


        #Lo guardamos en config para que desde los bp se pueda acceder
        app.config['marcas']=marcas
        app.config['categorias']=categorias
        app.config['precios']=precios


    except Exception as error:
        print('Error a la hora de obtener el numero de productos:',error)




if __name__=='__main__':
    app.run()