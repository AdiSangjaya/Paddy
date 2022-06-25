# 6A 19090019 Adi Sangjaya 
# 6A 19090121 Moh Farid Nurul Ikhsani 

from bson import decode
import keras
import numpy as np
from keras.preprocessing import image 
from keras.preprocessing.image import ImageDataGenerator
import datetime 
import matplotlib.pyplot as plt
from datetime import date
import pickle
from flask import Flask, jsonify,request,flash,redirect,render_template, session,url_for
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from itsdangerous import json
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from flask_restful import Resource, Api
import pymongo
import re
from PIL import Image
import datetime
import random
import string
from functools import wraps

#Belajar JWT
import jwt
import os
import datetime



app = Flask(__name__)
# jwt = JWTManager(app)
UPLOAD_FOLDER = 'fotohama'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "awokwok"
key = "Percobaan"
MONGO_ADDR = 'mongodb://localhost:27017'
MONGO_DB = "db_hama"

conn = pymongo.MongoClient(MONGO_ADDR)
db = conn[MONGO_DB]

api = Api(app)
#CORS(app)


from tensorflow.keras.models import load_model
MODEL_PATH = 'model.h5'
model = load_model(MODEL_PATH,compile=False)

pickle_inn = open('num_class_hama.pkl','rb')
num_class_hama = pickle.load(pickle_inn)

def allowed_file(filename):     
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class index(Resource):
  def post(self):

    if 'image' not in request.files:
      flash('No file part')
      return jsonify({
            "pesan":"tidak ada form image"
          })
    file = request.files['image']
    if file.filename == '':
      return jsonify({
            "pesan":"tidak ada file image yang dipilih"
          })
    if file and allowed_file(file.filename):
      letters = string.ascii_lowercase
      result_str = ''.join(random.choice(letters) for i in range(5))
      
      filename = secure_filename(file.filename+result_str+".jpg")
      print(filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      path=("fotohama/"+filename)
      
      today = date.today()
      db.riwayat.insert_one({'nama_file': filename, 'path': path, 'prediksi':'No predict', 'akurasi':0, 'tanggal':today.strftime("%d/%m/%Y")})

      img=image.load_img(path,target_size=(224,224))
      img1=image.img_to_array(img)
      img1=img1/255
      img1=np.expand_dims(img1,[0])
      plt.imshow(img)
      predict=model.predict(img1)
      classes=np.argmax(predict,axis=1)
      for key,values in num_class_hama.items():
          if classes==values:
            accuracy = float(round(np.max(model.predict(img1))*100,2))
            info = db['hama'].find_one({'nama_hama': str(key)})
            db.riwayat.update_one({'nama_file': filename}, 
              {"$set": {
                'prediksi': str(key), 
                'akurasi':accuracy
              }
              })
            if accuracy >90:
              today = date.today()
              db.riwayat.insert_one({'nama_file': filename, 'path': path, 'prediksi':'No predict', 'akurasi':0, 'tanggal':today.strftime("%d/%m/%Y")})
              print("The predicted image of the hama is: "+str(key)+" with a probability of "+str(accuracy)+"%")            
              return jsonify({
                "Nama_Hama":str(key),
                "Accuracy":str(accuracy)+"%",
                "Perkenalan_Singkat": info['perkenalan'],
                "Penanganan" : info['penanganan'],        
              })
            else :
              print("The predicted image of the Hama is: "+str(key)+" with a probability of "+str(accuracy)+"%")
              return jsonify({
                "Message":str("Jenis Hama belum tersedia "),
                "Nama_Hama":str("Jenis Hama belum tersedia "),
                "Accuracy":str(accuracy)+"%"               
                
              })
    else:
      return jsonify({
        "Message":"bukan file image"
      })

#Buat belajar JWT
# @app.route("/api/v1/users", methods=["POST"])
# def register():
#   new_user = request.get_json()
#   new_user["password"] = new_user["password"]
#   doc = db.admin.find_one({"username": new_user["username"]})
#   if not doc:
#     db.admin.insert_one(new_user)
#     return jsonify({'msg': 'User Admin berhasil dibuat'}), 201
#   else:
#     return jsonify({'msg': 'Username sudah pernah dibuat'}), 409
#   return jsonify({'msg': 'Username atau Password Salah'}), 401

# @app.route("/api/v1/login", methods=["POST"])
# def loginApi():
# 	login_details = request.get_json()
# 	user_from_db = db.admin.find_one({'username': login_details['username']})

# 	if user_from_db:
# 		password = login_details['password']
# 		if password == user_from_db['password']:
# 			access_token = create_access_token(identity=user_from_db['username'])
# 			return jsonify(access_token=access_token), 200

# @app.route("/api/v1/user", methods=["GET"])
# @jwt_required()
# def profile():
# 	current_user = get_jwt_identity()
# 	user_from_db = db.admin.find_one({'username' : current_user})
# 	if user_from_db:
# 		del user_from_db['_id'], user_from_db['password']
# 		return jsonify({'profile' : user_from_db }), 200
# 	else:
# 		return jsonify({'msg': 'Profil admin tidak ditemukan'}), 404

  
@app.route('/admin')
def admin():
    return render_template("login.html")
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] # .encode('utf-8')
        user = db['admin'].find_one({'username': str(username)})
        print(user)

        if user is not None and len(user) > 0:
            if password == user['password']:
                
                token =jwt.encode(
                {
                    "username":username,
                    "exp":datetime.datetime.now() + datetime.timedelta(minutes=120)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
                print(token)
                return redirect(url_for('datahama'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
    
#menampilkan daftar hama
@app.route('/datahama')
def datahama():
    data = db['hama'].find({})
    return render_template('datahama.html', datahama = data)

#tambah Data
#@app.route('/tambahData')
#def tambahData():

    #return render_template('tambahData.html')

#roses memasukan data hama ke database
#@app.route('/daftarhama', methods=["POST"])
#def daftarhama():
#    if request.method == "POST":
#        nama_hama = request.form['nama_hama']
#        perkenalan = request.form['perkenalan']
#        penanganan = request.form['penanganan']
#        if not re.match(r'[A-Za-z]+', nama_hama):
#            flash("Nama harus pakai huruf Dong!")
        
#        else:
#            db.hama.insert_one({'nama_hama': nama_hama, 'perkenalan': perkenalan, 'penanganan':penanganan})
#            flash('Data Hama berhasil ditambah')
#            return redirect(url_for('datahama'))

#    return render_template("tambahData.html")

@app.route('/edithama/<nama_hama>', methods = ['POST', 'GET'])
def edithama(nama_hama):
  
    data = db['hama'].find_one({'nama_hama': nama_hama})
    print(data)
    return render_template('edithama.html', edithama = data)

@app.route('/updatehama/<nama_hama>', methods=['POST'])
def updathama(nama_hama):
    if request.method == 'POST':
        nama_hama = request.form['nama_hama']
        perkenalan = request.form['perkenalan']
        penanganan = request.form['penanganan']
        if not re.match(r'[A-Za-z]+', nama_hama):
            flash("Nama harus pakai huruf Dong!")
        else:
          db.hama.update_one({'nama': nama_hama}, 
          {"$set": { 
            'nama_hama': nama_hama,
            'perkenalan': perkenalan, 
            'penanganan':penanganan
            }
            })

          flash('Data Hama berhasil diupdate')
          return render_template("popUpEdit.html")

    return render_template("datahama.html")

#menampilkan riwayat
@app.route('/riwayat')
def riwayat():
    dataRiwayat = db['riwayat'].find({})
    print(dataRiwayat)
    return render_template('riwayat.html',riwayat  = dataRiwayat)
#hapus riwayat
@app.route('/hapusRiwayat/<nama_file>', methods = ['POST','GET'])
def hapusRiwayat(nama_file):
  
    db.riwayat.delete_one({'nama_file': nama_file})
    flash('Riwayat Berhasil Dihapus!')
    return redirect(url_for('riwayat'))
  

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


api.add_resource(index, "/api/image", methods=["POST"])

if __name__ == '__main__':
  

  #app.run()
  app.run(debug = True, port=5000, host='0.0.0.0')

