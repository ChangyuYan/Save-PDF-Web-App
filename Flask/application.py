from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask import send_file

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
from zipfile import ZipFile
import os

application = app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save_all_pdf', methods=['POST'])
def save_all_pdf():
    # Read from user input
    input_features = [x for x in request.form.values()]
    page_url = str.lower(str(input_features[0]))
    u_client = uReq(page_url)
    page_html = u_client.read()
    u_client.close()

    # Parse HTML
    page_soup = soup(page_html, "html.parser")
    # Grab each row
    containers = page_soup.findAll("a")
    link_prefix = page_url[: page_url.rfind('/')]

    # Create a zipfile object
    zip_file_name = 'pdf_files.zip'
    zip_obj = ZipFile(zip_file_name, 'w')

    for anchor in containers:
        link = anchor.get('href')
        if link and link[-3:] == 'pdf':
            file_url = "%s/%s" % (link_prefix, link)
            r = requests.get(file_url, stream=True)
            current_file_name = ("%s.pdf" % anchor.text)
            print(current_file_name)
            with open(current_file_name, "wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
            zip_obj.write(current_file_name)
            os.remove(current_file_name)

    zip_obj.close()

    return send_file(zip_file_name)


if __name__ == '__main__':
    app.run(debug=True)
