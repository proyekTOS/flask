from flask import Flask, render_template, request, redirect, url_for
import time
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def login():
	return render_template('login.html')

@app.route('/index')
def index():
	return render_template('index.html')
	
@app.route('/register')
def register():
	return render_template('register.html')
	
@app.route('/loginberhasil', methods = ['POST'])
def check():

	con = sql.connect("polling.db")
	
	cur = con.cursor()
	
	
	username=request.form['username']
	
	password=request.form['password']
	
	if request.form.get('login',None) != None:
		cur.execute("select COUNT(*) as hitung from user where username = ? and password = ?",[username,password])
		count = cur.fetchone()
		if(count[0]==1):
			return redirect(url_for("index"))
		else:
			return redirect(url_for("login"))

	if request.form.get('register',None) != None:
		email=request.form['email']
		cur.execute("select MAX(ID) as hitung from user")
		row = cur.fetchone()
		max = row[0]+1
		try:
			cur.execute("insert into user (id, email, username, password) values (?,?,?,?)",(max,email,username,password))
			con.commit()
			msg = "Record successfully added"
		except:
			con.rollback()
			msg = "error in insert operation"
		return redirect(url_for("login",msg = msg))
		 
		
if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0',5043)
