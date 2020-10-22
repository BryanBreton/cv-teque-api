import psycopg2
from flask import Flask, request, jsonify, Blueprint
from flask_api import status
import json
from flask_restplus import Api, Resource
from base64 import b64decode, b64encode
from flask_cors import CORS, cross_origin
from bdd import getCursor, getConnection

offres = Blueprint('offres', __name__)

app = Flask(__name__)
api = Api(app=app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
con = getConnection()
cur = getCursor()

@offres.route('/ecole', methods=["POST"])
def addEcole():
    school = {
        "nom": str(request.json["nom"]),
        "ville": str(request.json["ville"]),
        "adresse": str(request.json["adresse"]),
        "codePostal": str(request.json["codePostal"]),
        "nomDomaine": str(request.json["nomDomaine"])
    }
    reqAddSchool = "insert into ecole (nom, ville, adresse, code_postal, nom_domaine) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(school["nom"], school["ville"], school["adresse"], school["codePostal"], school["nomDomaine"])
    print (reqAddSchool)
    cur.execute(reqAddSchool)
    con.commit()
    return "created", status.HTTP_201_CREATED

@offres.route("/ecole/filtre", methods=["POST"])
def ecoleFiltre():
    if request.json["filtre"] == "":
        #pas de filtre
        if request.json["ville"] == "":
            #aucun des deux
            req = "select distinct ecole.nom from filtre_ecole fe join ecole on fe.id_ecole = ecole.id join filtre on fe.id_filtre = filtre.id"
        else:
            #que ville
            req = "select distinct ecole.nom from filtre_ecole fe join ecole on fe.id_ecole = ecole.id join filtre on fe.id_filtre = filtre.id where ecole.ville='{0}'".format(request.json["ville"])
    else:
        #y a un filtre
        if request.json["ville"] == "":
            #que filtre
            req = "select distinct ecole.nom from filtre_ecole fe join ecole on fe.id_ecole = ecole.id join filtre on fe.id_filtre = filtre.id where filtre.nom = '{0}'".format(request.json["filtre"])
        else:
            #les deux
            req = "select distinct ecole.nom from filtre_ecole fe join ecole on fe.id_ecole = ecole.id join filtre on fe.id_filtre = filtre.id where filtre.nom = '{0}' and ecole.ville = '{1}'".format(request.json["filtre"], request.json["ville"])
    cur.execute(req)
    schools = cur.fetchall()
    ecoles = []
    for ecole in schools:
        ecoles.append(ecole[0])
    return jsonify(ecoles)