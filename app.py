import os, re
from model import mymodel
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.python.keras import backend as session

UPLOAD_FOLDER = 'saveimages'
ALLOWED_EXTENSION = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1] in ALLOWED_EXTENSION


@app.route('/')
def upload_result():
    return redirect(url_for('template'))


@app.route('/template', methods=['GET'])
def template():
    return render_template('dbd.html')


@app.route('/template/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        #  Проверяем, есть ли в полученном запросе файл с расширением .jpg
        answer_request = str(request.files)
        mask = re.compile('.jpg')  #
        answer_result = mask.findall(answer_request) # True or False
        if '.jpg' not in answer_result:
            return redirect(url_for('error'))
        file = request.files['inputfile']
        if allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        file = request.files['inputfile']

        return """
                    <a href='/upload/{filename}'> Press here {filename} and wait a bit</a> 
               """.format(filename=file.filename)


@app.route('/error')
def error():
    return """
                <h1> File didn`t load </h1>
                <a href="/template"> Load correct 'name'.jpg file</a>
           """


@app.route('/upload/<filename>') #example filename == cat
def uploaded_file(filename):
    file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    type = 'net/binary.h5'
    session.clear_session()
    model = mymodel(type, file)
    number = model.number
    session.clear_session()
    if number:
        return '<a href="/template">The Dog is at the picture. Press here to return start page</a>'
    else:
        return '<a href="/template">The Cat is at the picture. Press here to return start page</a>'


if __name__ == "__main__":
    app.run(debug=True, port=777)


