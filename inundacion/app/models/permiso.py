from app.db import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String

class Permiso(db.Model):
    __tablename__ ="permiso"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), unique=True)
   # activo = Column (Integer, primary_key=True)

     #constructor   
    def __init__(self, nombre=None):
        self.nombre = nombre
        
    def get_by_name(nombre_permiso):
        return Permiso.query.filtrer_by(nombre=nombre_permiso).first() 

    def all():
        return Permiso.query.all()
