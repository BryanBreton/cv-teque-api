import psycopg2
from flask import Flask, request, jsonify, Blueprint
from flask_api import status
import json
from flask_restplus import Api, Resource
from base64 import b64decode, b64encode
from flask_cors import CORS, cross_origin
from bdd import getCursor, getConnection

etudiants = Blueprint('etudiants', __name__)

app = Flask(__name__)
api = Api(app=app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
con = getConnection()
cur = getCursor()

@etudiants.route("/etudiant/<int:id>", methods=["GET"])
def getOneEtudiant(id):
    cur.execute("SELECT * from etudiant where id="+str(id))
    etudiant = cur.fetchone()
    if etudiant != None:
        etudiantObj = {
            "id": etudiant[0],
            "nom": etudiant[1],
            "prenom": etudiant[2],
            "email": etudiant[3],
            "password": etudiant[4],
            "date_naissance": etudiant[5],
            "id_ecole": etudiant[6],
        }
        return jsonify(etudiantObj)
    else:
        return jsonify('n\'existe pas')

@etudiants.route("/connexion/etudiant", methods=["GET"])
def connexionEtudiant():
    auth=request.headers.get('Authorization')
    #regarder le code du projet micro serv pour base 64
    print(auth)
    login, pwd = auth.split(":", 1)
    reqConnexion = "select * from etudiant where email='%s' and password='%s'"
    cur.execute(reqConnexion % (str(login), str(pwd)))
    user = cur.fetchone()
    if user == None:
        return "Email ou mot de passe incorrect"
    else:
        userReturn = {
            "id": user[0],
            "nom": user[1],
            "prenom": user[2],
            "mail": user[3],
            "dateNaissance": user[5],
            "idEcole": user[6]
        }
        return jsonify(userReturn)

@etudiants.route('/etudiant', methods=["POST"])
def addEtudiant(self):
    student = {
        "nom": str(request.json["nom"]),
        "prenom": str(request.json["prenom"]),
        "email": str(request.json["email"]),
        "password": str(request.json["password"]),
        "dateNaissance": str(request.json["dateNaissance"]),
        "idEcole": str(request.json['idEcole'])
    }
    reqAddStudent = "insert into etudiant (nom, prenom, email, password, date_naissance, id_ecole) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5})".format(student["nom"], student["prenom"], student["email"], student["password"], student["dateNaissance"], student["idEcole"])
    print (reqAddStudent)
    cur.execute(reqAddStudent)
    con.commit()
    return "created", status.HTTP_201_CREATED