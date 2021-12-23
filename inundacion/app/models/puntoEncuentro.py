from os import error
from re import match
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import db
from sqlalchemy.orm import relationship
from app.models.coordenada import Coordenada
import re
from sqlalchemy import update
from flask import jsonify


class PuntoEncuentro(db.Model):
    __tablename__ = "puntosEncuentro"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), unique=True)
    direccion = Column(String(30), unique=True)
    estado = Column(String(30))
    coordenada_id = Column(Integer, ForeignKey("coordenadas.id"))
    coordenada = relationship(Coordenada)
    telefono = Column(String(30), unique=True)
    email = Column(String(30), unique=True)


    #Constructor
    def __init__(self, nombre=None, direccion=None, estado=None, coordenada_id=None, telefono=None, email=None):
        self.nombre = nombre
        self.direccion = direccion
        self.estado = estado
        self.coordenada_id = coordenada_id 
        self.telefono = telefono
        self.email = email


    def create(nombre, direccion, estado, latitud, longitud, telefono, email):
        coordenada = Coordenada.create(latitud, longitud)
        puntoEncuentro = PuntoEncuentro(nombre=nombre, direccion=direccion, estado=estado, coordenada_id=coordenada.id, telefono=telefono, email=email)
        db.session.add(puntoEncuentro)
        db.session.commit()


    def exist(nombre, direccion, telefono, email):
        errores = {}
        
        nombre_result = PuntoEncuentro.query.filter_by(nombre = nombre).first()
        direccion_result = PuntoEncuentro.query.filter_by(direccion = direccion).first()
        telefono_result = PuntoEncuentro.query.filter_by(telefono = telefono).first()
        email_result = PuntoEncuentro.query.filter_by(email = email).first()

        if ( (nombre_result is not None ) ):
            errores["error_nombre"] = "El nombre ya existe"

        if ( (direccion_result is not None ) ):
            errores["error_direccion"] = "La dirección ya existe"

        if ( (telefono_result is not None ) ):
            errores["error_telefono"] = "El teléfono ya existe"  

        if ( (email_result is not None ) ):
            errores["error_email"] = "El email ya existe"

        return errores


    def validar(form):
        errores = {}

        if not 4 <= len(form.get("nombre")) <= 30:
            errores["error_nombre"] = "El nombre es incorrecto"


        direccion = form.get("calles") + str(form.get("altura"))
        if not 4 <= len(direccion) <= 30:
            errores["error_direccion"] = "La dirección es incorrecta"
            if not (form.get("altura").isdigit()):
                errores["error_direccion"] = errores["error_direccion"] + ". " + "La altura debe contener sólo números"
        else:
            if not (form.get("altura").isdigit()):
                errores["error_direccion"] = "La altura debe contener sólo números" 


        latitud = form.get("latitud")
        longitud = form.get("longitud")
        coordenadaLatitud = Coordenada.query.filter_by(latitud = latitud).first()
        coordenadaLongitud = Coordenada.query.filter_by(longitud = longitud).first()
        
        if ((coordenadaLatitud is not None) and (coordenadaLongitud is not None)):
            if (coordenadaLatitud.id == coordenadaLongitud.id):
                errores["error_coordenada"] = "La ubicación geográfica ya está registrada"
        else:
            validador_coordenada = r"[\-\+]?[0-9]{2,3}\.[0-9]+$"
            if not re.match(validador_coordenada, latitud):
                errores["error_coordenada"] = "La ubicación geográfica es incorrecta"
            else:
                if not re.match(validador_coordenada, longitud):
                    errores["error_coordenada"] = "La ubicación geográfica es incorrecta"
       

        telefono = form.get("prefijo") + form.get("numero")
        if not (telefono.isdigit()):
            errores["error_telefono"] = "El teléfono es incorrecto"
        else:
            if (not 7 <= len(telefono) <= 12):
                errores["error_telefono"] = "El teléfono es incorrecto"
        

        email = form.get("email")
        validador_email = r"^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+([.]\w{2,4})+$"
        if not re.match(validador_email, email):
            errores["error_email"] = "El email es incorrecto"
        
        return errores    


    def delete(punto):
        db.session.delete(punto)
        db.session.commit()


    def nombreExisteEnDb(campo):
        elemento = PuntoEncuentro.query.filter_by(nombre = campo).first()
        if elemento is not None:
            return True
        return False

    
    def direccionExisteEnDb(campo):
        elemento = PuntoEncuentro.query.filter_by(direccion = campo).first()
        if elemento is not None:
            return True
        return False


    def telefonoExisteEnDb(campo):
        elemento = PuntoEncuentro.query.filter_by(telefono = campo).first()
        if elemento is not None:
            return True
        return False


    def emailExisteEnDb(campo):
        elemento = PuntoEncuentro.query.filter_by(email = campo).first()
        if elemento is not None:
            return True
        return False


    def validarNombre(nombre):
        if not 4 <= len(nombre) <= 30:
            return "El nombre es incorrecto"
        return None

    
    def validarDireccion(direccion):
        if not 4 <= len(direccion) <= 30:
            return "La dirección es incorrecta"
        return None


    def validarCoordenada(coord):
        validador_coordenada = r"[\-\+]?[0-9]{2,3}\.[0-9]+$"
        if not re.match(validador_coordenada, coord):
            return "La ubicación geográfica es incorrecta"
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
            return "El email es incorrecto"
        return None


    #---- Para API ---------------------------------
    
    #retorna todos los recorridos
    def getAll():
        puntos = PuntoEncuentro.query.all()
        return puntos
            
    def puntosAll(pagina, elementosxPagina):
        puntosAll = []
        diccionario = {}
        puntos = PuntoEncuentro.getAll()
        page = int(pagina)
        puntosEncuentro = []
        paginas = len(puntos) // elementosxPagina
        
        if (len(puntos) % elementosxPagina) > 0:
            paginas = paginas + 1

        if ((page > 0) and (page <= paginas)):
            puntosPaginaActual = PuntoEncuentro.query.paginate(page=page, per_page=elementosxPagina)
            cantidadPaginaActual = 0
            for punto in puntosPaginaActual.items:
                cantidadPaginaActual += 1
                coordenadas = Coordenada.query.filter_by(id = punto.coordenada_id).first()
                puntosEncuentro.append({ "id": punto.id, "nombre": punto.nombre, "direccion": punto.direccion, "lat": coordenadas.latitud, "long": coordenadas.longitud, "telefono": punto.telefono, "email": punto.email })
            diccionario = { "puntos_encuentro": puntosEncuentro, "total": cantidadPaginaActual, "pagina": page }
            puntosAll.append(diccionario)
            puntosEncuentro = []
            return jsonify(puntosAll), 200
        else:
            dict = {}
            dict['error'] = "No existe la pagina ingresada"
            return jsonify(dict), 404
        