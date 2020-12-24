import os
from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import json
import uuid

UPLOAD_FOLDER = '/static/img'
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

@app.route("/artigos", methods=["POST"])
def artigo_set():
    req = request.get_json()
    data = json.loads(json.dumps(req))
    unique_filename = str(uuid.uuid4())



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


@app.route("/teste", methods=['GET'])
def user_get():
   
    try:
      
    except Exception:
        return 'Error: '

    return jsonify(json_data)


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