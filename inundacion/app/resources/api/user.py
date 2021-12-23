from flask import jsonify, Blueprint, request, abort, Response
from sqlalchemy.sql.sqltypes import Date
from app.models.user import User

from app.db import db
import json
from datetime import date


user_api = Blueprint("usuarios", __name__, url_prefix="/usuarios")

@user_api.get("/")
def index():
    user_rows = User.query.all()
    print (user_rows)
    usuarios = [user.as_dict() for user in user_rows]
    return jsonify(usuarios=usuarios)

@user_api.post("/")
def create():
    form = User(**request.get_json())
    User.new_usuario_from_api(form)
    return jsonify(form.as_dict()), 201

    
