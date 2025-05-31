from flask import Blueprint,redirect,url_for,abort
from flask_login import logout_user,login_required
logout_bp=Blueprint('logout',__name__)

#Ruta de logout
@logout_bp.route('/logout')
@login_required
def logout():
    try:
        #Cerramos sesion
        logout_user()
        
        #Redirijimos a inicio
        return redirect(url_for('home.home'))
    
    #Cualquier otro error, 404
    except Exception as error:
        print('ERROR DETECTADO EN /logout')
        print(error)
        abort(404)
