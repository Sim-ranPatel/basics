from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm



from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired , Length, Email, EqualTo


# import necessary packages
from sqlalchemy import text
from sqlalchemy.engine import result

app = Flask(__name__)
# db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'dafasfa'

class MyForm(FlaskForm): 
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=20)]) 
    username = StringField('UserName', validators=[InputRequired()]) 
    email = StringField('Email', validators=[InputRequired(),  Email()]) 
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)]) 
    confirmpassword = PasswordField('ConfirmPassword', validators=[InputRequired(), EqualTo('password')]) 

class Todo(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(200), nullable=False)
    description= db.Column(db.String(500), nullable=False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}  {self.title}"
    
class User(db.Model):
    user_id= db.Column(db.Integer, primary_key=True)
    user_name= db.Column(db.String(200), nullable=False)
    email= db.Column(db.String(200), nullable=False)
    password= db.Column(db.String(200), nullable=False)

    # def __repr__(self) -> str:
    #     return f"{self.user_id}  {self.user_name}"    

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
    elif request.method == "GET":
        title = request.args.get('title')
        desc = request.args.get('desc')
    if(title != None or desc != None):
        todo = Todo(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html',allTodo = allTodo)
    # return "HELLO WORLD"

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    return "product page"

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
    elif request.method == "GET":
        title = request.args.get('title')
        desc = request.args.get('desc')    
    if(title != None or desc != None): 
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo = todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/login', methods=["GET", "POST"])
def login():
    # if request.method == "POST":
    return render_template('login.html')  # Serve the login page

# @app.route('/register', methods=["GET", "POST"])
# def register():
#     print("equest.method",request.method)
#     return render_template('register.html')  # Serve the login page

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     print("_____________________")
#     form = MyForm() 
#     if form.validate_on_submit(): 
#         name = form.name.data 
#         username = form.username.data 
#         email = form.email.data 
#         password = form.password.data 
#         confirmpassword = form.confirmpassword.data 

#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('register'))
#     return render_template('register.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Here, you can handle the registration logic (e.g., save to database)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, port=9000)