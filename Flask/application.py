from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask import send_file

application = app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save_all_pdf', methods=['POST'])
def save_all_pdf():
    # Read from user input
    input_features = [x for x in request.form.values()]
    url_entered = str.lower(str(input_features[0]))
    print("Hello, world!")
    print(url_entered)
    print('------')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)