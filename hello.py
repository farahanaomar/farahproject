from flask import Flask, render_template, url_for, request, flash,  redirect
from forms import registerForm, loginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required


app = Flask(__name__)
app.secret_key = "wakanda_forevah"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farahproject.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
login_manager=LoginManager(app)

# login session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return f'Unauthorized Access. Please register to access this Account page.'


# Database
class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), unique=True, nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=False)
    image_file= db.Column(db.String(20), nullable=False, default='default.jpg')
    # Password in String for now not integer
    password= db.Column(db.String(15), nullable=False)  
    date_created= db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return f'{self.username} : {self.email} : {self.date_created.strftime("%d/%m/%Y, %H:%M:%S")}'

    with app.app_context(): 
        db.create_all()

# route
@app.route("/hello")
def index():
    flash("What's your name?")
    return render_template("index.html", title="Hello Page")

@app.route("/greet", methods=["POST", "GET"])
def greet():
    flash("Hi " + str(request.form['name_input']) + ", great to see you ! Have a nice day :)")
    return render_template("index.html", title="Greet Page")

@app.route('/Account')
@login_required
def Account():
    return render_template("Account.html", title="Account Page")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('Account'))
    form= registerForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created succesfully for {form.username.data}', category='success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register Page", form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Account'))
    form= loginForm()
    if request.method == 'POST':
        user=User.query.filter_by(username=form.username.data).first()
        if form.username.data==user.username and form.password.data==user.password:
            login_user(user)
            flash(f'Logged in succesfully for {form.username.data}', category='success')
            return redirect(url_for('Account'))
        else:
            flash(f'Logged in failed for {form.username.data}', category='danger')
    return render_template("login.html", title="Login Page", form= form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)