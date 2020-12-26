import os
from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import json
import uuid
from os.path import join, dirname, realpath

#UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img/')
UPLOAD_FOLDER = 'static/img/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
"""REMOVE make_response AFTER USING IT ITS NO NEEDED"""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artigos')
def artigos():
    return render_template('artigos.html')

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/teste')
def teste():
    return render_template('teste.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/artigosold", methods=["POST"])
def artigoold_set():
    req = request.get_json()
    data = json.loads(json.dumps(req))

    try:
        conn = mysql.connect()
        cur = conn.cursor()
    except Exception:
        print('Error: unable to connect to database')

    try:
        sql = "INSERT INTO es (nome, quant, imgpath, description) VALUES (%s, %s, %s, %s)"
        val = (data['nome'], data['quant'], data['imgpath'], data['desc'])
        cur.execute(sql, val)
    except Exception:
        print('Error: unable to insert items')
    
    conn.commit()
    cur.close()
    conn.close()
    res = make_response(jsonify({"message": "OK"}), 200)
    return res

@app.route("/artigos", methods=["POST"])
def artigo_set():
    req = request.form['data']
    data = json.loads(req)

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
        conn = mysql.connect()
        cur = conn.cursor()
    except Exception:
        print('Error: unable to connect to database')

    try:
        sql = "INSERT INTO es (nome, quant, imgpath, description) VALUES (%s, %s, %s, %s)"
        val = (data['nome'], data['quant'], fullpath, data['desc'])
        cur.execute(sql, val)
    except Exception:
        print('Error: unable to insert items')

    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfile+"."+filetype))
    except Exception:
        print('Error: unable to save file')

    conn.commit()
    cur.close()
    conn.close()
    res = make_response(jsonify({"message": "OK"}), 200)
    return res

@app.route('/listartigos')
def v_timestamp():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM es")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('listartigos.html', data=data)

@app.route("/testeroute", methods=['POST'])
def file_test():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            flash('No selected file')
            return redirect(request.url)

        filename = file.filename
        newfile = str(uuid.uuid4())
        filetype = filename.rsplit('.', 1)[1].lower()
        print(newfile+"."+filetype)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfile+"."+filetype))
        return 'hi'


@app.route("/teste123", methods=['GET'])
def user_get():
    name = request.args.get('search')
    rv = 0
    try:
        conn = mysql.connect()
        cur = conn.cursor()
    except Exception:
        return 'Error: unable to connect to database'

    try:
        cur.execute("SELECT * FROM users WHERE id="+name)
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
    except Exception:
        return 'Error: unable to fetch items'
    finally:
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        cur.close()
        return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)