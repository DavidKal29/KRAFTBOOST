from flask import Blueprint,redirect,url_for,render_template
from flask_login import login_required
from formularios_WTF.forms import Account


profile_bp=Blueprint('profile',__name__,url_prefix='/profile')


@profile_bp.route('/',methods=['GET','POST'])
@login_required
def profile():
    return redirect(url_for('profile.account'))


@profile_bp.route('/account',methods=['GET','POST'])
@login_required
def account():

    form=Account()
    
    
    return render_template('profile/account.html',form=form)