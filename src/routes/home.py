from flask import Blueprint,render_template,current_app

home_bp=Blueprint('home',__name__)

@home_bp.route('/')
def home():
    return 'Bienvenido a la páginca de inicio. EL HOME :)'