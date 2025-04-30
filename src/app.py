from flask import Flask
from os import getenv
from config import config
from dotenv import load_dotenv
from flask_mysqldb import MySQL

#Blueprints
from routes.home import home_bp



load_dotenv()

#Creamos la app de flask
app=Flask(__name__)

#Establecemos la configuración de la app
app.config.from_object(config['development'])

#Conexión de la base de datos
db=MySQL(app)


#Registro de blueprints
app.register_blueprint(home_bp)


if __name__=='__main__':
    app.run()