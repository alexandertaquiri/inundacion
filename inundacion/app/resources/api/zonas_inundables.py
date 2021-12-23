from flask import jsonify
from app.models.zona_inundable import Zona_inundable
from flask import request
from app.resources.configuracion import datosDeConfiguracion


def apiZona(idZona):
    return Zona_inundable.zonaApi(idZona)

def apiZonaAll(pagina):
    datos = datosDeConfiguracion()
    return Zona_inundable.zonaApiAll(pagina, datos['cantidad'])