from flask import jsonify
from app.models.configuracion import Configuracion
from flask import request
from app.resources.configuracion import datosDeConfiguracion


def api_configuracion():
    lista = []
    datos = datosDeConfiguracion()
    lista.append(datos['coloresPublicos'])
    diccio={'colores_publicos': lista}
    return jsonify(diccio)
