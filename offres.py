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

@offres.route("/offres", methods=['GET'])
def get():
    cur.execute("SELECT * FROM offre")
    offres = cur.fetchall()
    listeOffres = []
    for item in offres:
        listeOffres.append({
            "id": item[0],
            "titre": item[1],
            "description": item[2],
            "date": str(item[3]),
            "typeOffre": item[4],
            "idEntreprise": item[5]
        })
    return jsonify(listeOffres)

@offres.route("/offres/ecole/<int:id>", methods=["GET"])
def getOffresByEcole(id):
    cur.execute("select o.id, o.nom, o.description, o.date_offre, o.type_offre, o.id_entreprise, e.nom from offre_ecole oe join offre o on oe.id_offre=o.id join entreprise e on o.id_entreprise = e.id where oe.id_ecole='{0}'".format(id))
    offres = cur.fetchall()
    listeOffres = []
    for item in offres:
        listeOffres.append({
            "id": item[0],
            "titre": item[1],
            "description": item[2],
            "date": str(item[3]),
            "typeOffre": item[4],
            "idEntreprise": item[5],
            "nomEntreprise": item[6]
        })
    return jsonify(listeOffres)

@offres.route("/like", methods=["POST"])
def like():
    cur.execute("insert into liked (id_offre, id_etudiant) VALUES ('{0}', {1})".format(request.json["idOffre"], request.json["idEtudiant"]))
    con.commit()
    return "created", 201, {'Access-Control-Allow-Origin': '*'}

@offres.route('/offre/like/<int:idEtudiant>', methods=["GET"])
def offreLiked(idEtudiant):
    cur.execute("select o.id, o.nom, o.description, o.date_offre, o.type_offre, e.id, e.nom from liked join offre o on liked.id_offre=o.id join entreprise e on o.id_entreprise=e.id where liked.id_etudiant='{0}'".format(idEtudiant))
    offres = cur.fetchall()
    listeOffres = []
    for item in offres:
        listeOffres.append({
            "id": item[0],
            "titre": item[1],
            "description": item[2],
            "date": str(item[3]),
            "typeOffre": item[4],
            "idEntreprise": item[5],
            "nomEntreprise": item[6]
        })
    return jsonify(listeOffres)

@offres.route('/file', methods=["POST"])
def addFile(self):
    print(request.json)
    return 0