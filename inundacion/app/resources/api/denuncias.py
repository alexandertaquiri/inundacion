from flask import jsonify, Blueprint, request, abort, Response
from sqlalchemy.sql.sqltypes import Date
from app.models.denuncia import Denuncia
from app.models.denuncia_categoria import DenunciaCategoria
from app.db import db
import json
from datetime import date
from app.resources.configuracion import datosDeConfiguracion
from app.resources.denuncia import ValidarFormulario



denuncia_api = Blueprint("denuncias", __name__, url_prefix="/denuncias")

@denuncia_api.get("/")
def index():
    denuncias_rows = Denuncia.query.all()
    print (denuncias_rows)
    denuncias = [denuncia.as_dict() for denuncia in denuncias_rows]
    return jsonify(denuncias=denuncias)

@denuncia_api.post("/")
def create():
    
    # # Primer Version (El servicio debe verificar que el ID de la categoría exista en la base de datos)
    # nueva_denuncia = Denuncia(**request.get_json())
    # # Verifico que el ID de la categoría exista en la BD
    # if DenunciaCategoria.get_by_id(nueva_denuncia.categoria_id):
    # # Creo la nueva denuncia y la almaceno
    #     Denuncia.new_denuncia_from_api(nueva_denuncia)
    #     return jsonify(nueva_denuncia.as_dict()), 201
    # else:
    #      return jsonify({'detalle' : 'La categoria ingresada no existe en el sistema'}), 400

    try:
        form = ValidarFormulario(**request.get_json())
        if form.validate():
            new_denuncia = Denuncia(**request.get_json())    
            # verifico que el ID de la categoría exista en la BD
            if DenunciaCategoria.get_by_id(new_denuncia.categoria_id):
                # Creo la nueva denuncia y la almaceno
                Denuncia.new_denuncia_from_api(new_denuncia)
                return jsonify(new_denuncia.as_dict()),201
            return jsonify({'detalle' : 'La categoria ingresada no existe en el sistema'}), 409
        return jsonify({'detalle' : form.errors}), 400 
    except:    
        return jsonify({'detalle' : ''}), 500 
