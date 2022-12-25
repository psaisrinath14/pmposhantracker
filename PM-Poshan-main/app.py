from flask import Flask,flash, render_template, send_file,redirect,  url_for,request
from data import data
import urllib.request
from stu_data import stu_data
from werkzeug.utils import secure_filename
from classdata import classdata
from PIL import Image
from keras_preprocessing.image import load_img,img_to_array
import numpy as np
from keras.models import load_model
import os
import urllib
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model = load_model(r'C:\Users\saisr\Documents\calories\meals.h5')
labels = {0: 'bendi', 1: 'pappu', 2: 'rice'  }
def processed_img(img_path):
    img=load_img(img_path,target_size=(224,224,3))
    img=img_to_array(img)
    img=img/255
    img=np.expand_dims(img,[0])
    answer=model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    if (res == 'pappu'):
        calories = '62.5'
    if (res == 'bendi'):
        calories = '33'
    if (res == 'rice'):
        calories = '130'

    return res.capitalize(),calories

UPLOAD_FOLDER = 'static/uploads/'


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
file_arr = []
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/student_dash", methods=["POST", "GET"])
def student_dash():
    if request.method == "POST":
        print(request.form)
        return render_template("student/student_success.html")
    else:
        return render_template("student/student.html")





@app.route("/get_class_data")
def get_class_data():
    return classdata


@app.route("/performance/get_stu_data")
def get_stu_data():
    return stu_data

@app.route("/performance/<school>/get_school_graph_data")
def school_wise_graph(school):
    data = stu_data[school]
    return {
        "girls": {
            "height": data[0],
            "weight": data[1],
        },
        "boys": {"height": data[2], "weight": data[3]},
    }


@app.route("/school_dash")
def school_dash():
    return render_template("school/school_dash.html")

@app.route("/upload_menu", methods=["POST", "GET"])
def upload_menu():
    if request.method == "POST":
        print(request.form)
        return render_template("school/upload_menu_success.html")
    else:
        return render_template("school/upload_menu.html")


@app.route("/reg_student", methods=["POST", "GET"])
def reg_student():
    if request.method == "POST":
        print(request.form)
        return render_template("school/reg_student_success.html")
    else:
        return render_template("school/reg_student.html")


@app.route("/upload_hdata", methods=["POST", "GET"])
def upload_data():
    if request.method == "POST":
        print(request.form)
        return render_template("school/upload_hdata_success.html")
    else:
        return render_template("school/upload_hdata.html")


@app.route("/upload_attendance", methods=["POST","GET"])
def upload_attendance():

    if request.method == "POST":
        if 'file1' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']
        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            f1 = UPLOAD_FOLDER + filename1
            a, b = processed_img(f1)
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file1.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            f2 = UPLOAD_FOLDER + filename2
            c, d = processed_img(f2)
        if file3 and allowed_file(file3.filename):
            filename3 = secure_filename(file3.filename)
            file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
            f3 = UPLOAD_FOLDER + filename3
            e, f = processed_img(f3)
        return render_template("school/upload_attendance_success.html",item=a,cal=b,item1=c,cal1=d,item2=e,cal2=f,total=(float(b)+float(d)+float(f)))
    else:


        return render_template("school/upload_attendance.html")











if __name__ == "__main__":
    app.run(debug=True)
