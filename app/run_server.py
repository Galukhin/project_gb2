import json

import os
from flask import Flask, render_template, jsonify, send_from_directory, flash, redirect, url_for

from flask import request

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html', is_home=True)

@application.route('/about')
def about():
    return render_template('about_sp.html')

# Custom static data
@application.route('/data/<path:filename>')
def files(filename):
    return send_from_directory('data', filename)


@application.route('/test_pat/<id>')
def test_pat(id):
    result_pat1 = ''
    result_pat2 = ''
    result_pat3 = ''
    if id == '1':
        result_pat1 = ' Результат - положительный, Найдено 10 аномалий. '
    elif id == '2':
        result_pat2 = ' Результат - положительный, Найдено 3 аномалий. '
    elif id == '3':
        result_pat3 = ' Результат - отрицательный, Найдено 0 аномалий. '
    return render_template('index.html', result_pat1=result_pat1, result_pat2=result_pat2, result_pat3=result_pat3)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_txt = file.read()
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result_pat4 = ' Результат - отрицательный, Найдено 0 аномалий. '
            # return redirect(url_for('index', file_txt=file_txt, result_pat4=result_pat4))
            return render_template('index.html', file_txt=file_txt, result_pat4=result_pat4)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@application.route('/series/', methods=['POST'])
def new_series():
    series = request.json
    return '<h1>Waiting for results</h1>' + json.dumps(series)


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
    # application.run(host='0.0.0.0')
