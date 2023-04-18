from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.discovery import Discovery
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# login and registration
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/new')
def new_user():
    return render_template('new_user_registration.html')

@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_registration_form(request.form):
        return redirect('/user/new')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "hometown": request.form['hometown'],
        "profession": request.form['profession'],
        "education": request.form['education'],
        "favorite_dino": request.form['favorite_dino'],
        "about_user": request.form['about_user'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.check_email(request.form)
    if not user:
        flash("Invalid Credentials", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Credentials", 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')


# user profile page
@app.route('/user/profile/<int:id>')
def user_profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('user_profile.html', user = User.check_id(data))
