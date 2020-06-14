from flask import render_template,url_for,flash,redirect
from flaskblog.models import User,Post
from flaskblog.forms import RegistrationForm,LoginForm
from flaskblog import app

posts = [
    { 
        'author':'Leo Leung',
        'title':'Blog Post 1',
        'content':'life is good',
        'date_posted': 'April 28,2018',
    },
    { 
        'author':'Leo Leung',
        'title':'Blog Post 2',
        'content':'life is bad',
        'date_posted': 'May 1,2020',
    },
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)


@app.route('/about')
def about():
    return render_template('about.html',title="About")

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',
            form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Log in Unsuccessful. Please check username and password','danger')
    return render_template('login.html',title='Login',form=form)


