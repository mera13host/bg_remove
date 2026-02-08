from flask import Flask
from flask import render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import time
from rembg import remove

app = Flask(__name__)  # = missing था

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_background', methods=['POST'])
def remove_background():
    file = request.files['file']
    if file and allowed_file(file.filename):
        new_filename = secure_filename(file.filename)
        timestamp = str(int(time.time()))
        filename_parts = new_filename.split('.')
        
        filename = f"{filename_parts[0]}_{timestamp}.{filename_parts[1]}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename_parts[0]}_{timestamp}_output.png")

        with open(filepath, 'rb') as f:
            with open(output_path, 'wb') as output:
                output.write(remove(f.read()))

        output_filename = f"{filename_parts[0]}_{timestamp}_output.png"
        return redirect(url_for('output', filename=output_filename))
    else:
        return redirect(url_for('index'))

@app.route('/output/<filename>')
def output(filename):
    return render_template('result.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)