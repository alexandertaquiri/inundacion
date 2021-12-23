from flask import jsonify
from app.models.puntoEncuentro import PuntoEncuentro
from flask import request
from app.resources.configuracion import datosDeConfiguracion


def puntosAll(pagina):
    datos = datosDeConfiguracion()
    return PuntoEncuentro.puntosAll(pagina, datos['cantidad'])