import psycopg2
from flask import Flask, request, jsonify, Blueprint
from flask_api import status
import json
from flask_restplus import Api, Resource
from base64 import b64decode, b64encode
from flask_cors import CORS, cross_origin
from bdd import getCursor, getConnection

entreprises = Blueprint('entreprises', __name__)

app = Flask(__name__)
api = Api(app=app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
con = getConnection()
cur = getCursor()

@entreprises.route("/entreprise/<int:id>", methods=["GET"])
def getOneEntreprise(id):
    cur.execute("SELECT * from entreprise where id="+str(id))
    entreprise = cur.fetchone()
    if entreprise != None:
        entrepriseObj = {
            "id": entreprise[0],
            "nom": entreprise[1],
            "ville": entreprise[2],
            "adresse": entreprise[3],
            "code_postal": entreprise[4]
        }
        return jsonify(entrepriseObj)
    else:
        return jsonify("n'existe pas")


@entreprises.route("/connexion/entreprise", methods=["GET"])
def connexionEntreprise():
    auth=request.headers.get('Authorization')
    #regarder le code du projet micro serv pour base 64
    print(auth)
    login, pwd = auth.split(":", 1)
    reqConnexion = "select * from entreprise where pseudo='%s' and password='%s'"
    cur.execute(reqConnexion % (str(login), str(pwd)))
    user = cur.fetchone()
    if user == None:
        return "Email ou mot de passe incorrect"
    else:
        userReturn = {
            "id": user[0],
            "nom": user[1],
            "ville": user[2],
            "adresse": user[3],
            "codePostal": user[4],
            "pseudo": user[6]
        }
        return jsonify(userReturn)

@entreprises.route('/entreprise', methods=["POST"])
def addEntreprise():
    company = {
        "nom": str(request.json["nom"]),
        "ville": str(request.json["ville"]),
        "adresse": str(request.json["adresse"]),
        "codePostal": str(request.json["codePostal"])
    }
    reqAddCompany = "insert into entreprise (nom, ville, adresse, code_postal) VALUES ('{0}', '{1}', '{2}', '{3}')".format(company["nom"], company["ville"], company["adresse"], company["codePostal"])
    print (reqAddCompany)
    cur.execute(reqAddCompany)
    con.commit()
    return "created", status.HTTP_201_CREATED