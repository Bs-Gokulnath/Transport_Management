from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/signin_student', methods=['GET', 'POST'])
def signin_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if email already exists
        existing_student = Student.query.filter_by(email=email).first()
        if existing_student:
            return "Email already exists! Please use a different email."
        
        # Add student details to the database
        new_student = Student(name=name, email=email, password=password)
        db.session.add(new_student)
        db.session.commit()
        
        return redirect(url_for('login_student'))
    
    return render_template('signin_student.html')

@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if email and password match any student in the database
        student = Student.query.filter_by(email=email, password=password).first()
        if student:
            return f"Welcome, {student.name}!"
        
        return "Invalid email or password. Please try again."
    
    return render_template('login_student.html')


@app.route('/parent')
def parent():
    return render_template('parent.html')

@app.route('/signin_parent', methods=['GET', 'POST'])
def signin_parent():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        
        existing_parent = Parent.query.filter_by(email=email).first()
        if existing_parent:
            return "Email already exists! Please use a different email."
        
        
        new_parent = Parent(name=name, email=email, password=password)
        db.session.add(new_parent)
        db.session.commit()
        
        return redirect(url_for('login_parent'))
    
    return render_template('signin_parent.html')

@app.route('/login_parent', methods=['GET', 'POST'])
def login_parent():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        
        parent = Parent.query.filter_by(email=email, password=password).first()
        if parent:
            return f"Welcome, {parent.name}!"
        
        return "Invalid email or password. Please try again."
    
    return render_template('login_parent.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
