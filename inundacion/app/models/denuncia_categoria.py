from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import true
from app.db import db
from sqlalchemy import Column, Integer, String

class DenunciaCategoria(db.Model):
    __tablename__ = 'denuncia_categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = Column(String(50))


    @classmethod
    def all(self):
        return self.query.all()

    #Constructor
    def __init__(self, nombre=None):
        self.nombre = nombre

    #Devuelve todas las categorias
    def all():
        return DenunciaCategoria.query.all()

    #Devuelve categoriaConId
        
    def categoriaConId(id_categoria):
        return DenunciaCategoria.query.filter_by(id = id_categoria).first()

    @staticmethod
    def get_by_id(id):
        return DenunciaCategoria.query.get(id)

    
    #Devuelve categoriaConNombre

    def categoriaConNombre(nombre):
        return DenunciaCategoria.query.filter_by(nombre = nombre).first()  

    #crear Categoria
    def crear(nombre):
        denuncia_categoria= DenunciaCategoria (nombre=nombre)
        db.session.add(denuncia_categoria)
        db.session.commit()

    def as_dict(self):
        return {
            "id_categoria": self.id_categoria,
             "nombre": self.nombre,
            
        }