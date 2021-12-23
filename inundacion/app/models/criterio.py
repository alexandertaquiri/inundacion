from sqlalchemy import Column, Integer, String
from app.db import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import update


class Criterio_ord(db.Model):
    __tablename__ = 'criterios'
    id = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String(30), nullable=False)


    #constructor
    def __init__(self, nombre=None):
        self.nombre = nombre
    
    #devuelve todos los datos
    def all():
        return Criterio_ord.query.all()

    def devolverCriterio(criterio_id):
        return Criterio_ord.query.filter_by(id = criterio_id).first()
    
    def devolverCriterioConNombre(nombre):
        return Criterio_ord.query.filter_by(nombre = nombre).first()
    
    #la primera vez lo crea
    def create(nombre):
        crite = Criterio_ord(nombre=nombre)
        db.session.add(crite)
        db.session.commit()