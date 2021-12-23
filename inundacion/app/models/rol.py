from sqlalchemy.orm import relationship, backref
#from sqlalchemy.sql.schema import ForeignKey
from app.db import db
from sqlalchemy import Column, String, Integer, ForeignKey
from app.models.permiso import Permiso
from sqlalchemy import update

permisos = db.Table('rol_tiene_permiso',
          Column('rol_id', Integer, ForeignKey('rol.id'), primary_key=True),
          Column('permiso_id', Integer, ForeignKey('permiso.id'), primary_key=True)
          )
  
class Rol(db.Model):
    __tablename__ = 'rol'
    id = Column (Integer, primary_key=True)
    nombre = Column (String(30), unique=True)
    permisos = relationship('Permiso', secondary=permisos, backref= backref('roles_con_el_permiso', lazy = True), lazy='subquery')
    #permisos = relationship('Permiso', secondary='rol_tiene_permiso', backref=backref('roles_con_el_permiso', lazy = True), lazy='subquery')
    
 #constructor   
    def __init__(self, nombre=None):
        self.nombre = nombre
        
    def get_by_nombre(nombre):
        rol = Rol.query.filter_by(nombre = nombre).first()
        return rol

    def getAll():
        roles = Rol.query.all()
        return roles
