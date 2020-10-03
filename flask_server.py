from os import environ
from flask import Flask
import server

app = Flask(__name__)
app.run(environ.get('PORT'))

@app.route('/')
def hello_world():
    return 'Hello, World!'

server.startServer()