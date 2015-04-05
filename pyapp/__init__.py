from flask import Flask

app = Flask(__name__)
app.static_url_path = '/static'

import views