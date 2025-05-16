from flask import Blueprint
from flask_login import login_required


profile_bp=Blueprint('profile',__name__,url_prefix='/profile')


@profile_bp.route('/',methods=['GET','POST'])
@login_required
def profile():
    return 'Este es el perfil temporal'