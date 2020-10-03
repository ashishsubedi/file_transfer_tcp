from os import environ
from flask import Flask

app = Flask(__name__)
app.run(environ.get('PORT'))

@app.route('/')
def hello_world():
    return 'Hello, World!'