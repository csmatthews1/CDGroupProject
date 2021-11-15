from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app.models.video import Video
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

app.secret_key = 'iringvneii;ai;jfngri;albjdbd niueeuhrfi'

@app.route('/signin')
def signin():
    return render_template('login.html')


@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/signin')
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash('Invalid email or password', 'login')
        return redirect('/signin')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invlid email or password','login')
        return redirect('/signin')

    session['user_id'] = user_in_db.id
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')