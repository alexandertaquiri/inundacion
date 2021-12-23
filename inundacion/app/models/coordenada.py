from sqlalchemy import Column, Integer
from sqlalchemy.sql.sqltypes import String
from app.db import db
from sqlalchemy import update

class Coordenada(db.Model):
    __tablename__ = "coordenadas"
    id = Column(Integer, primary_key=True)
    latitud = Column(String(20))
    longitud = Column(String(20))

    #Constructor
    def __init__(self, latitud=None, longitud=None):
        self.latitud = latitud
        self.longitud = longitud

    def create(latitud, longitud):
        coordenada = Coordenada(latitud=latitud, longitud=longitud)
        db.session.add(coordenada)
        db.session.commit()
        return coordenada

    def obtenerCoordenada(idCoordenada):
        return Coordenada.query.filter_by(id = idCoordenada).first()

    def delete(coordenada):
        db.session.delete(coordenada)
        db.session.commit()
        