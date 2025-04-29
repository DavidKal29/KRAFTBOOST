from flask import Flask 
from os import getenv
from config import config
from dotenv import load_dotenv
from flask_mysqldb import MySQL

load_dotenv()

app=Flask(__name__)

#Establecemos la configuración de la app
app.config.from_object(config['development'])

#Conexión de la base de datos
db=MySQL(app)


if __name__=='__main':
    app.run()