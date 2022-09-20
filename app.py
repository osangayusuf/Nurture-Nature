from crypt import methods
from datetime import datetime
import email
from email.policy import default
from enum import unique
from flask import Flask, render_template, redirect,url_for, flash, request
from forms import RegistrationForm, LoginForm, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


app = Flask(__name__, template_folder="templates")

# Initializing LoginManaer to control user login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# instance of Sqqlalchemy
db = SQLAlchemy(app)
# --------- App Configurations -------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)

# to create user database
class User(UserMixin, db.Model):
    # __tablename__= 'Users'
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # generte hash for entered password
    def create_password(self, password_entered):
        self.password = generate_password_hash(password_entered)

    # confirm if matched password matches password in database
    def check_password_match(self, password_entered):
        return check_password_hash(self.password, password_entered)

# defining the home route
@app.route('/')
def home():
    return render_template('index.html')

#  defining our peripheral routes
#  the register route
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    
    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                user = User(
                    username = form.username.data,
                    email = form.email.data,
                    phone = form.phone.data
                )
                user.create_password(form.password.data)
                if User.query.filter_by(email=user.email).first():
                    raise ValidationError('Email already in use')
                else:
                    db.session.add(user)
                    db.session.commit()
                    print('created user')
                    login_user(user)
                    return redirect(url_for('home'))
            except:
                print('Error creating user')
    except:
        print('Error...')
 
    return render_template('forms/sign_up.html', form=form)

# the login route 
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # checks if entered email is registered
        user = User.query.filter_by(email=form.email.data).first()
        # check if the entered email is registered and entered password is corrrect
        if user is not None and user.check_password_match(form.password.data): #if both return true..
            login_user(user, form.remember_me.data)
            return redirect(url_for('home'))
        elif user is None:
            print('User doesnt exist...')
        else:
            flash('Invalid credentials...\nUsername or password incorrect')
            print("Error logging user in....")

    return render_template('forms/login.html', form=form)

# logout 
@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('login'))


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')    


# runs our flask app
if __name__=='__main__':
    app.run(debug=True)