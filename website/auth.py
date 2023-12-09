from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Создание blueprint
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Поиск определенной записи в базе данных
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Успешный вход в систему!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Неверный пароль, попробуйте еще раз.', category='error')
        else:
            flash('Электронная почта не существует.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

    
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Электронная почта уже существует.', category='error')
        elif len(email) < 4:
            flash('Электронная почта должна содержать больше 3 символов.', category='error')
        elif len(first_name) < 2:
            flash('Имя должно содержать больше 1 символа.', category='error')
        elif password1 != password2:
            flash('Пароли не совпадают.', category='error')
        elif len(password1) < 7:
            flash('Пароль должен содержать не менее 7 символов.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Учетная запись создана!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
