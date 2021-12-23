from os import error
from re import match
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import Boolean
from app.db import db
import re
from sqlalchemy import update
from sqlalchemy.orm import backref
from flask import jsonify


class RecorridoEvacuacion(db.Model):
    _tablename_ = "recorrido_evacuacion"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), unique=True)
    descripcion = Column(String(150))
    publicado = Column(Boolean)
    coordenadas = Column(String(500))


    #Constructor
    def __init__(self, nombre=None, descripcion=None, publicado=None, coordenadas=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.publicado = publicado
        self.coordenadas = coordenadas


    def create(nombre, descripcion, estado, coordenadas):

        if (estado == "0"):
            estado = False
        else:
            estado = True

        recorridoEvacuacion = RecorridoEvacuacion(nombre=nombre, descripcion=descripcion, publicado=estado, coordenadas=coordenadas)
        db.session.add(recorridoEvacuacion)
        db.session.commit()


    def nombreExisteEnDb(campo):
        elemento = RecorridoEvacuacion.query.filter_by(nombre = campo).first()
        if elemento is not None:
            return True
        return False


    def exist(nombre):
        errores = {}
        
        nombre_result = RecorridoEvacuacion.query.filter_by(nombre = nombre).first()

        if ( (nombre_result is not None ) ):
            errores["error_nombre"] = "El nombre ya existe"

        return errores


    def validar(datos):
        errores = {}

        if not 4 <= len(datos.get("nombre")) <= 30:
            errores["error_nombre"] = "El nombre es incorrecto"

        if not 4 <= len(datos.get("descripcion")) <= 150:
            errores["error_descripcion"] = "La descripción es incorrecta"

        latLong = datos.get("coordenadas").split(",")        
        if (len(latLong) < 6):
            errores["error_coordenadas"] = "Debe seleccionar tres puntos en el mapa como mínimo"
            
        return errores   


    def validarNombre(nombre):
        if not 4 <= len(nombre) <= 30:
            return "El nombre es incorrecto"
        return None


    def delete(recorrido):
        db.session.delete(recorrido)
        db.session.commit()


    
    #---- Para API ---------------------------------
    
    #retorna todos los recorridos
    def getAll():
        recorridos = RecorridoEvacuacion.query.all()
        return recorridos

    def parsearLista(coord):
        x = 2
        final_list= lambda coord, x: [coord[i:i+x] for i in range(0, len(coord), x)]
        output=final_list(coord, x)
        return output
        
    def recorridosAll(pagina, elementosxPagina):
        recorridosAll = []
        diccionario = {}
        recorridosEvacuacion = []
        page = int(pagina)
        recorridos = RecorridoEvacuacion.getAll()
        recorridosEvacuacion = []
        paginas = len(recorridos) // elementosxPagina

        if (len(recorridos) % elementosxPagina) > 0:
            paginas = paginas + 1

        if ((page > 0) and (page <= paginas)):
            recorridosPaginaActual = RecorridoEvacuacion.query.paginate(page=page, per_page=elementosxPagina)
            cantidadPaginaActual = 0
            for recorrido in recorridosPaginaActual.items:
                cantidadPaginaActual += 1
                recorridosEvacuacion.append({ "id": recorrido.id, "nombre": recorrido.nombre, "coordenadas": RecorridoEvacuacion.parsearLista(recorrido.coordenadas.split(",")), "descripcion": recorrido.descripcion })
            diccionario = { "recorridos": recorridosEvacuacion, "total": cantidadPaginaActual, "pagina": page }
            recorridosAll.append(diccionario)
            return jsonify(recorridosAll), 200
        else:
            dict = {}
            dict['error'] = "No existe la pagina ingresada"
            return jsonify(dict), 404
            