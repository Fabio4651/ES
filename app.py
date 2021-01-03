import os
from flask import Flask, jsonify, render_template, request, session, make_response, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_session import Session 
from markupsafe import escape
import json
import uuid
from os.path import join, dirname, realpath
from flask_uploads import IMAGES, UploadSet, configure_uploads
from pathlib import Path

#UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img/')
UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

"""REMOVE make_response AFTER USING IT ITS NO NEEDED"""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#The secret key shhh 
app.config['SECRET_KEY'] = '_1#y6G"F7Q2z\n\succ/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)

files = UploadSet('files', IMAGES)

app.config['UPLOADED_FILES_ALLOW'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOADED_FILES_DEST'] = 'static/upload'
configure_uploads(app, files)

class Artigos(db.Model):
    __tablename__ = 'artigos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25))
    quant = db.Column(db.Integer)
    imgpath = db.Column(db.String(80))
    description = db.Column(db.Text)

    def __init__(self,nome,quant,imgpath,description):
        self.nome=nome
        self.quant=quant
        self.imgpath=imgpath
        self.description=description
    
    def __repr__(self):
        return repr(id)

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

@app.route('/deleteartigo', methods=['POST'])
def deleteartigo():
    if 'username' in session:
        data=request.args.get('id_artigo')
        data_file=str(data)+'.jpg'
        print('teste'+data_file)
        Artigos.query.filter_by(id=data).delete()
        my_file = Path(os.path.join(app.config['UPLOADED_FILES_DEST'], data_file))
        if my_file.exists():
            os.remove(os.path.join(app.config['UPLOADED_FILES_DEST'], data_file))
        db.session.commit()
        return redirect(url_for('listartigos'))
    return redirect(url_for('index'))

@app.route('/artigos')
def artigos():
    r = Artigos.query.all()
    if 'username' in session:
        return render_template('artigos.html')
    return redirect(url_for('index'))

@app.route('/inserirartigos', methods=['POST'])
def inserirartigos():
    if 'username' in session:
        descending = Artigos.query.order_by(Artigos.id.desc())
        last_item = descending.first()
        last_id = last_item.id + 1
        a = Artigos.query.all()
        nome = request.form['nome']   
        quant = request.form['quant']
        description = request.form['desc']
        imgpath = request.files['img']
        if request.method == 'POST' and 'img' in request.files:
            filename = files.save(request.files['img'], name=str(last_id) + '.jpg')
        new_artigo = Artigos(nome=nome, quant=quant, description=description, imgpath='static/upload/' + str(last_id) + '.jpg')
        db.session.add(new_artigo)
        db.session.commit()
        return redirect(url_for('listartigos'))
    return redirect(url_for('index'))

@app.route('/users')
def users():
    if 'username' in session:
        return render_template('users.html')
    return redirect(url_for('index'))

@app.route('/teste')
def teste():
    if 'username' in session:
        return render_template('teste.html')
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/listartigos')
def listartigos():
    if 'username' in session:
        data = Artigos.query.all()
        return render_template('listartigos.html', data=data)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)