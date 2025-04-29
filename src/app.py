from flask import Flask 
from os import getenv
from config import config
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)
app.config.from_object(config['development'])


if __name__=='__main':
    app.run()