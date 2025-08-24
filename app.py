from flask import Flask, request, render_template, url_for, redirect, session
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms.login_register import LoginForm, RegisterForm, EditForm, ProductForm
from models.user import User, Products, db

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == int(id)).first()

@app.route('/', methods=["GET", "POST"])
def index():
    db.create_all()
    return render_template('index.html', session = session)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter(User.email==form.email.data).all():
            return 'User already exists'
        user = User(email=form.email.data,
                    password=User.get_hashed_password(form.password.data),
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    birth_date=form.birth_date.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email==form.email.data).first()
        if user is not None and User.verify_password(user.password, form.password.data):
            login_user(user)
            session['logged_in'] = True
            return redirect(url_for('index', id=user.id))
        else:
            return "Invalid credentials"
    return render_template('login.html', form = form)

@app.route('/logout', methods=["GET"])
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/add', methods=["GET", "POST"])
def add():
    db.create_all()
    form = LoginForm()
    form2 = ProductForm()

    if form.validate_on_submit():
        user = User(email = form.email.data, 
                    password = form.password.data,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    birth_date = form.birth_date.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('dane', id=user.id))
    
    if form2.validate_on_submit():
        product = Products(name=form2.name.data, price=form2.price.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products'))

    return render_template('add.html', form=form, form2=form2)
    
@app.route('/dane/<int:id>', methods=["GET", "POST"])
def dane(id):
    user = User.query.filter_by(id=id).first()
    form = EditForm()
    return render_template('dane.html', user=user)

@app.route('/edit_user/<int:id>', methods=["GET", "POST"])
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    form = EditForm()
    if form.validate_on_submit():
        user.username = form.username.data
        db.session.commit()
        return redirect(url_for('dane', id=user.id))
    return render_template('edit_user.html', form=form)

@app.route('/products', methods=["GET", "POST"])
def products():
    sort_by = request.form.get('sort')
    print(sort_by)
    if sort_by == 'name':
        products = Products.query.order_by(Products.name.asc()).all()
    elif sort_by == 'price':
        products = Products.query.order_by(Products.price.desc()).all()
    else:
        products = Products.query.all()

    return render_template('products.html', products=products)

if __name__ == '__main__':  
    app.run()

