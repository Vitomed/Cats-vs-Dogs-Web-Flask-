import os
from model import mymodel
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from tensorflow.python.keras import backend as session

UPLOAD_FOLDER = 'saveimages'
ALLOWED_EXTENSION = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1] in ALLOWED_EXTENSION


@app.route('/', methods=['GET'])
def upload_result():
    return render_template('dbd.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['inputfile']
    if request.method == 'POST':
        if allowed_file(file.filename):
            file = request.files['inputfile']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return file.filename


@app.route('/upload/<filename>') #example filename == cat
def uploaded_file(filename):
    file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename) + '.jpg')
    type = 'net/binary.h5'
    session.clear_session()
    model = mymodel(type, file)
    number = model.number
    session.clear_session()
    if number:
        return "Dog"
    else:
        return "Cat"

if __name__ == "__main__":
    app.run(debug=True, port=777)


