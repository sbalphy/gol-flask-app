from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from . import db
from .models import User

# implementação básica de login usando flask_login
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')
    
@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or not user.password == password:
        flash('Usuário ou senha inválidos')
        flash('DEV: usuário e senha são admin')
        return redirect(url_for('auth.login'))
    login_user(user)
    return redirect(url_for('dash.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))