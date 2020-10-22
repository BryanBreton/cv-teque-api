import psycopg2
from flask import Flask, request, jsonify
from flask_api import status
import json
from flask_restplus import Api, Resource
from base64 import b64decode, b64encode
from flask_cors import CORS, cross_origin
from bdd import getCursor, getConnection
from offres import offres
from entreprises import entreprises
from etudiants import etudiants

app = Flask(__name__)
app.register_blueprint(offres)
app.register_blueprint(entreprises)
app.register_blueprint(etudiants)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.run(host='0.0.0.0', port='3000', debug=True)