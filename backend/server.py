from flask import Flask
from flask_cors import CORS 
from .routes import main

def create_server():
    server = Flask(__name__)
    CORS(server)  

    server.register_blueprint(main)  

    return server  