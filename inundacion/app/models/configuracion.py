from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import db
from app.models.criterio import Criterio_ord
from sqlalchemy.orm import relationship, backref
from sqlalchemy import update



class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String(30), nullable=False)
    elementoPorPagina = Column(Integer, nullable=True)
    coloresPublico = Column(String(50), nullable=True)
    coloresPrivado = Column(String(50), nullable=True)
    estado = Column(Integer, nullable=False)
    criterio_id = Column(Integer, ForeignKey("criterios.id"))
    criterio = relationship(Criterio_ord)
        
    def __init__(self, nombre=None, elementoPorPagina=None, coloresPublico=None, coloresPrivado=None, activo=None, criterio_id=None):
        self.nombre = nombre,
        self.elementoPorPagina = elementoPorPagina,
        self.coloresPublico = coloresPublico,
        self.coloresPrivado = coloresPrivado,
        self.estado = activo,
        self.criterio_id = criterio_id
    
    #retorna todos los datos de la configuracion
    def all():
        return Configuracion.query.all()
    
    #retorna solo la configuracion activa
    def activo():
        return Configuracion.query.filter(Configuracion.estado == 1).first()
   
    #retorna la configuracion por defecto
    def por_defecto():
        return Configuracion.query.filter(Configuracion.nombre == "Por defecto").first()
    
    #configuracion anterior
    def conf_anterior():
        return Configuracion.query.filter(Configuracion.nombre == "Nueva personalizada").first()

    #Se usa la primera vez cuando no esta vacia la tabla de configuracion
    def create(nombre, elementoPorPagina, coloresPublico, coloresPrivado, activo, criterio_id):
        conf = Configuracion(nombre=nombre, elementoPorPagina=elementoPorPagina, coloresPublico=coloresPublico, coloresPrivado=coloresPrivado, activo=activo, criterio_id=criterio_id)
        db.session.add(conf)
        db.session.commit()