from flask import jsonify, Blueprint, request, abort, Response
from app.models.denuncia import Denuncia
from app.models.denuncia_categoria import DenunciaCategoria
from app.db import db
import json


categoria_api = Blueprint("categorias", __name__, url_prefix="/categorias")

@categoria_api.get("/")
def index():
    categorias_rows = DenunciaCategoria.query.all()
    print (categorias_rows)
    categorias = [categoria.as_dict() for categoria in categorias_rows]
    return jsonify(categorias=categorias)
