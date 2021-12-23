from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import DATETIME
from app.db import db
from app.models.denunciaSeguimiento import Denuncia_seguimiento
from flask import session
#from app.resources import denuncia
from app.models.denuncia_categoria import DenunciaCategoria
from datetime import date
from sqlalchemy import update 
import datetime
import re
import json
from app.models.user import User
from app.models.coordenada import Coordenada
from flask import jsonify

seguimientos = db.Table('denuncia_tiene_seguimiento',
              Column('denuncia_id', Integer, ForeignKey('denuncias.id'), primary_key=True),
              Column('denuncia_seguimiento_id', Integer,  ForeignKey('denuncia_seguimiento.id'), primary_key=True )
            )


class Denuncia(db.Model):
    __tablename__ = "denuncias"
    id = Column(Integer, primary_key=True , autoincrement=True)
    titulo = Column(String(50))
    # backref nos ahorra hacer la relacion desde la otra clase
    categoria_id = db.Column("categoria",db.Integer, db.ForeignKey('denuncia_categoria.id_categoria'))
    categoria = db.relationship("DenunciaCategoria", backref="denuncias")
    #categoria = Column(String(50))
    fecha_creacion = Column(Date)
    fecha_cierre = Column(Date)
    descripcion = Column(String(150))
    latitud = Column(String(50))
    longitud = Column(String(50))
    # Estados -> Sin confirmar, En curso, Resuelta, Cerrada
    estado = Column(String(20))
    asignado_a = Column(String(100))
    apellido_denunciante = Column(String(100))
    nombre_denunciante = Column(String(100))
    tel_cel_denunciante = Column(String(100))
    # Intentos maximos -> 3, se pasa a Cerrada, "No fue posible contactar al denunciante"
    intentos_comunicacion = Column(Integer)
    email_denunciante = Column(String(100))

    seguimientos = relationship('Denuncia_seguimiento', secondary=seguimientos, backref= backref(
        'denuncia_con_seguimiento', lazy=True), lazy='subquery')

#Constructor
    def __init__(self, titulo=None, categoria_id=None, fecha_creacion=None, fecha_cierre=None, descripcion=None, latitud=None, longitud=None, estado=None, asignado_a=None, apellido_denunciante=None, nombre_denunciante=None, tel_cel_denunciante=None, intentos_comunicacion=None, email_denunciante=None):
        self.titulo = titulo
        self.categoria_id = categoria_id
        self.fecha_creacion = fecha_creacion       
        self.fecha_cierre = fecha_cierre
        # self.fecha_cierre = 'Abierta'
        self.descripcion = descripcion
        self.latitud = latitud
        self.longitud = longitud
        self.estado = estado 
        self.asignado_a = asignado_a
        self.apellido_denunciante = apellido_denunciante
        self.nombre_denunciante = nombre_denunciante
        self.tel_cel_denunciante = tel_cel_denunciante
        self.intentos_comunicacion = intentos_comunicacion
        self.email_denunciante = email_denunciante



    # def get_seguimiento(denun_id):
        
    #     return seguimientos.query.filter_by(denuncia_id = denun_id)
    #    # User.query.filter(Role.id == 4, Team.id == current_user.team_id).all()
            

    def findById(denuncia_id):
        return Denuncia.query.filter_by(id = denuncia_id).first()
    


    def validarTitulo(titulo):
        if not 4 <= len(titulo) <= 30:
            return "El titulo es incorrecto"
        return None

    def validarDescripcion(descripcion):
        if not 4 <= len(descripcion) <= 30:
            return "La descripcion es incorrecto"
        return None

    def validarCoordenada(coord):
        validador_coordenada = r"[\-\+]?[0-9]{2,3}\.[0-9]+$"
        if not re.match(validador_coordenada, coord):
            return "La ubicación geográfica es incorrecta"
        return None   

    def validarApellido(apellido):
        if not 4 <= len(apellido) <= 30:
            return "El nombre es incorrecto"
        return None

    def validarNombre(nombre):
        if not 4 <= len(nombre) <= 30:
            return "El nombre es incorrecto"
        return None

    def validarTelefono(telefono):
        if not (telefono.isdigit()):
            return "El teléfono es incorrecto"
        else:
            if (not 7 <= len(telefono) <= 12):
                return "El teléfono es incorrecto"
        return None               

    def validarEmail(email):
        validador_email = r"^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+([.]\w{2,4})+$"
        if not re.match(validador_email, email):
            return False
        return True

     #funcion para devolver denuncias
    def all():
       return Denuncia.query.all()    

########################CREAR DENUNCIA#####################################    

    def crear(titulo, categoria_id, descripcion, latitud, longitud, asignado_a, apellido_denunciante, nombre_denunciante, tel_cel_denunciante, email_denunciante):
       denuncia=Denuncia (titulo=titulo, categoria_id=categoria_id, descripcion=descripcion, latitud=latitud, longitud=longitud, estado="Sin confirmar", asignado_a=asignado_a, apellido_denunciante=apellido_denunciante, nombre_denunciante=nombre_denunciante, tel_cel_denunciante=tel_cel_denunciante, intentos_comunicacion="0", email_denunciante=email_denunciante, fecha_creacion=date.today(), fecha_cierre= None)
       db.session.add(denuncia)
       db.session.commit()  


    def delete(denuncia):
        db.session.delete(denuncia)
        db.session.commit()

    def asignarSeguimiento(segui,denuncias):
        print("trae o no id##################33")
        print(segui)
        print(denuncias)
        

        denuncia=Denuncia.findById(denuncias)
        seguiD= Denuncia_seguimiento.get_by_id(segui)
        denuncia.seguimientos.append(seguiD)
        db.session.commit() 

    @staticmethod
    def new_denuncia_from_api(denuncia):
        denuncia.estado = "Sin confirmar"
        # print (f"esto es el estado {denuncia.estado}")
        fecha = date.today()
        denuncia.fecha_creacion = fecha
        denuncia.intentos_comunicacion = 0
        denuncia.asignado_a = ''
        # almaceno la denuncia
        if denuncia != None:
           db.session.add(denuncia)
           db.session.commit()
        
    
    def as_dict(self):
        return {
            "titulo": self.titulo,
            "categoria_id": self.categoria_id,
            "descripcion": self.descripcion,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "nombre_denunciante": self.nombre_denunciante,
            "apellido_denunciante": self.apellido_denunciante,
            "tel_cel_denunciante": self.tel_cel_denunciante,
            "email_denunciante": self.email_denunciante,
            "estado": self.estado, 
        }
    
    
    

    
           


        

      

    
