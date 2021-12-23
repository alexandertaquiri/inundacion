from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import DATETIME
from app.db import db
from sqlalchemy import update
from flask import session
from datetime import date
from sqlalchemy import and_
import datetime
import re


class Denuncia_seguimiento(db.Model):
    __tablename__="denuncia_seguimiento"
    id = Column(Integer, primary_key=True)
    descripcion= Column(String(200))
    autor= Column(String(80))
    fecha= Column(DATETIME, nullable=True)

#Constructor
    def __init__(self, descripcion=None, autor=None, fecha=None):
        self.descripcion = descripcion
        self.autor = autor
        self.fecha = fecha

    def crear(descripcion, autor):
        seguimiento=Denuncia_seguimiento (descripcion=descripcion, autor=autor, fecha=date.today())
        db.session.add(seguimiento)
        db.session.commit()
        return seguimiento

    def get_by_id(id_seguimiento):
        segui = Denuncia_seguimiento.query.filter_by(id = id_seguimiento).first()
        return segui    

    def findById(denuncia_id):
        return Denuncia_seguimiento.query.filter_by(id = denuncia_id)        
            