from flask import Flask

from formml.forms.loader import XmlLoader

forms = XmlLoader.load_directory('./examples')
app = Flask(__name__)


@app.route('/')
def index():
    return forms[0].to_html()
