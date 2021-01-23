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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/es'
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
    codigo = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(20))
    nome = db.Column(db.String(20))
    cargo = db.Column(db.String(20), nullable=False)
    img = db.Column(db.String(80))

    def __init__(self,codigo,password,nome,cargo,img):
        self.codigo=codigo
        self.password=password
        self.nome=nome
        self.cargo=cargo
        self.img=img
    
    def __repr__(self):
        return repr(id)

@app.route('/')
def index():
    if 'username' in session:
        #return 'Logged in as %s' % escape(session['username'])
        return redirect(url_for('main'))
    return render_template('login.html')

@app.route('/main')
def main():
    if 'username' in session:
        total_users = Users.query.count()
        total_artigos = Artigos.query.count()
        return render_template('index.html', total_users=total_users, total_artigos=total_artigos)
    return render_template('login.html')    

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.form['data'])
        querydata = Users.query.filter_by(codigo = data['codigo'], password = data['pass']).first()
        session['username'] = querydata.nome
        session['img'] = querydata.img
        session['cargo'] = querydata.cargo
        check = {'check': 'true'}
        return jsonify(check)
    return 'hi'

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear()
    check = {'check': 'true'}
    #return jsonify(check)
    return redirect(url_for('index'))

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
        filename = 'static/img/user.png'
        if request.method == 'POST' and imgpath:
            filename = 'static/upload/' + files.save(request.files['img'])
        new_artigo = Artigos(nome=nome, quant=quant, description=description, imgpath=filename)
        db.session.add(new_artigo)
        db.session.commit()
        return redirect(url_for('listartigos'))
    return redirect(url_for('index'))

@app.route("/updateartigo", methods=['POST'])
def updateartigo():
    if 'username' in session:
        data=request.args.get('id_artigo')
        update = Artigos.query.filter_by(id=data)

        return render_template('editarartigos.html', update=update)
    return redirect(url_for('index'))   

@app.route('/editartigo', methods=['POST'])
def editartigo():
    if 'username' in session:
        
        data = request.form['id']
        update = Artigos.query.filter_by(id=data).first()
        bd_img = update.imgpath
        img = request.files['img']

        if request.method == 'POST' and 'nome' in request.form:
            update.nome = request.form['nome'] 

        if request.method == 'POST' and 'quant' in request.form:    
            update.quant = request.form['quant']

        if request.method == 'POST' and 'desc' in request.form:
            update.description = request.form['desc']     

        update.imgpath = bd_img
        if request.method == 'POST' and img:
            update.imgpath = 'static/upload/' + files.save(request.files['img']) 

        db.session.commit()
        return redirect(url_for('listartigos'))
    return redirect(url_for('index'))    

@app.route('/users')
def users():
    if 'username' in session:
        return render_template('users.html')
    return redirect(url_for('index'))

@app.route('/criarusers')
def criarusers():
    u = Users.query.all()
    if 'username' in session:
        return render_template('criarusers.html')
    return redirect(url_for('index'))

@app.route('/inserirusers', methods=['POST'])
def inserirusers():
    if 'username' in session:
        nome = request.form['nome']   
        idagente = request.form['idagente']  
        password = request.form['password']
        cargo = request.form['cargo']
        img = request.files['img']
        filename = 'static/img/user.png'
        if request.method == 'POST' and img:
            filename = 'static/upload/' + files.save(request.files['img'])
        new_user = Users(nome=nome, codigo=idagente, password=password, cargo=cargo, img=filename)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('listusers'))
    return redirect(url_for('index'))

@app.route('/listusers')
def listusers():
    if 'username' in session:
        data = Users.query.all()
        return render_template('listusers.html', data=data)
    return redirect(url_for('index'))

@app.route('/updateusers', methods=['POST'])
def updateusers():
    if 'username' in session:
        data=request.args.get('id_user')
        print(str(data))
        update = Users.query.filter_by(id=data)

        return render_template('editusers.html', update=update)
    return redirect(url_for('index'))   

@app.route('/editusers', methods=['POST'])
def editusers():
    if 'username' in session:
        data = request.form['id']
        update = Users.query.filter_by(id=data).first()
        bd_img = update.img
        img = request.files['img']

        if request.method == 'POST' and 'nome' in request.form:
            update.nome = request.form['nome'] 

        if request.method == 'POST' and 'codigo' in request.form:    
            update.codigo = request.form['id_agente']

        if request.method == 'POST' and 'password' in request.form:
            update.password = request.form['password']     
       
        if request.method == 'POST' and 'cargo' in request.form:
             update.cargo = request.form['cargo']     

        update.img = bd_img
        if request.method == 'POST' and img:
            update.img = 'static/upload/' + files.save(request.files['img']) 

        db.session.commit()
        return redirect(url_for('listusers'))
    return redirect(url_for('index'))    

@app.route('/deleteuser', methods=['POST'])
def deleteuser():
    if 'username' in session:
        data=request.args.get('id_user')
        Users.query.filter_by(id=data).delete()
        db.session.commit()
        return redirect(url_for('listusers'))
    return redirect(url_for('index'))


@app.route('/teste')
def teste():
    if 'username' in session:
        return redirect(url_for('index'))
        #return render_template('teste.html')
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