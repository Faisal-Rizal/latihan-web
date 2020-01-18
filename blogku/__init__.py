from flask import Flask, render_template, url_for, flash, redirect
from forms import Registrasi_F, Login_F
app=Flask(__name__)
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app.config['SECRET_KEY']='88ee2d49ccaeff0ac5d36abf5a5ebcbb'
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite;///site.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY']='6bf3b088650fb9a71bca99428bbce448'
posts=[
{
	'penulis':'Gamaria Mandar',
	'title':"Blog Post 1",
	'konten':'ini adalah post pertama saya',
	'tgl_post':'September 20, 2019'
},
{
	'penulis':'Abdul Haris',
	'title':"Blog Post 2",
	'konten':'ini adalah post saya yang kedua',
	'tgl_post':'September 21, 2019'
},
]

@app.route("/home")
def home():
	return render_template("home.html" , title='Home', posts=posts)

@app.route("/about")
def about():
	return render_template("about.html" , title='About', posts=posts)

@app.route("/login", methods=['GET','POST'])
def login():
	form = Login_F()
	if form.validate_on_submit():
		if form.email.data =='gamar@blog.com' and form.password.data =='admin':
			flash('login sukses!','success')
			return redirect('home')
		else:
			flash('login gagal..!, periksa username dan password', 'danger')
			return redirect(url_for('login'))
	return render_template("login.html" , title='Login', form=form)

@app.route("/registrasi", methods=['GET','POST'])
def registrasi():
	form = Registrasi_F()
	if form.validate_on_submit():
		flash(f'Akun {form.username.data} berhasil ditambahkan!', 'success')
		return redirect(url_for('home'))
	return render_template("registrasi.html" , title="Registrasi", form=form)

db = SQLAlchemy(app)
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('post', backref='penulis', lazy=True)
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.password}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	konten = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	def __repr__(self):
		return f"Post('{self.title}', '{self.tgl_post}', '{self.konten}')"

if __name__=="__main__":
	app.run (debug=True)