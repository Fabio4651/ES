import os
from flask import Flask, jsonify, render_template, request, session, make_response, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_session import Session 
from markupsafe import escape
import json
import uuid
from os.path import join, dirname, realpath

#UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img/')
UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

"""REMOVE make_response AFTER USING IT ITS NO NEEDED"""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#The secret key shhh 
app.config['SECRET_KEY'] = '_1#y6G"F7Q2z\n\succ/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)

class Artigos(db.Model):
    __tablename__ = 'artigos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25))
    quant = db.Column(db.Integer)
    imgpath = db.Column(db.String(80))
    description = db.Column(db.Text)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20))
    password = db.Column(db.String(20))

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.form['data'])
        querydata = Users.query.filter_by(id = data['id'], password = data['pass']).first()
        session['username'] = querydata.nome
        check = {'check': 'true'}
        return jsonify(check)
    return 'hi'

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear()
    check = {'check': 'true'}
    return jsonify(check)

@app.route('/artigos')
def artigos():
    if 'username' in session:
        return render_template('artigos.html')
    return render_template('login.html')

@app.route('/users')
def users():
    if 'username' in session:
        return render_template('users.html')
    return render_template('login.html')

@app.route('/teste')
def teste():
    if 'username' in session:
        return render_template('teste.html')
    return render_template('login.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/artigos", methods=["POST"])
def artigo_set():
    data = json.loads(request.form['data'])

    if 'file' not in request.files:
        print('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        print('No selected file')
        return redirect(request.url)

    filename = file.filename
    newfile = str(uuid.uuid4())
    filetype = filename.rsplit('.', 1)[1].lower()
    fullpath = UPLOAD_FOLDER+newfile+"."+filetype

    try:
        insert = Artigos(nome=data['nome'], quant=data['quant'], imgpath=fullpath, description=data['desc'])
        db.session.add(insert)
    except Exception:
        print('Error: unable to insert items')    

    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfile+"."+filetype))
    except Exception:
        print('Error: unable to save file')

    db.session.commit()
    res = make_response(jsonify({"message": "OK"}), 200)
    return res

@app.route('/listartigos')
def v_timestamp():
    data = Artigos.query.all()
    return render_template('listartigos.html', data=data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)