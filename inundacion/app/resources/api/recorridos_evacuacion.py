from flask import jsonify
from app.models.recorridoEvacuacion import RecorridoEvacuacion
from flask import request
from app.resources.configuracion import datosDeConfiguracion


def recorridosAll(pagina):
    datos = datosDeConfiguracion()
    return RecorridoEvacuacion.recorridosAll(pagina, datos['cantidad'])
