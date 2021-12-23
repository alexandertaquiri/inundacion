from os import error
from re import match
from flask import jsonify
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import db
from sqlalchemy.orm import relationship
from app.models.coordenada import Coordenada
import re
from sqlalchemy import update


class Zona_inundable(db.Model):
    __tablename__ = "zonas_inundables"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    codigo = Column(String(10), unique=True)
    descripcion = Column(String(150))
    estado = Column(Integer, nullable=False)
    coordenadas = Column(String(500))
    color = Column(String(15))
    
    
    #Constructor
    def __init__(self, nombre=None, codigo=codigo, descripcion=None, estado=None, coordenadas=None, color=None):
        self.nombre = nombre
        self.codigo = codigo
        self.descripcion = descripcion
        self.estado = estado
        self.coordenadas = coordenadas
        self.color = color

    #Crear zona    
    def crear(nombre, codigo, descripcion, estado, coordenadas, color):
        zona=Zona_inundable(nombre=nombre, codigo=codigo, descripcion=descripcion, estado=estado, coordenadas=coordenadas, color=color)
        db.session.add(zona)
        db.session.commit()    
    
    #devolver todas las zonas
    def getAll():
        zonas = Zona_inundable.query.all()
        return zonas 

    #retorna zona por id
    def getIdZona(zona_id):
        return Zona_inundable.query.get(zona_id)

    #borrado
    def borrar(id_zona):
        zona = Zona_inundable.getIdZona(id_zona)
        db.session.delete(zona)
        db.session.commit()
    
    #devolver zona por el nombre
    def devolverZona(cod):
        return Zona_inundable.query.filter_by(codigo = cod).first() 
    
    #Actualizar zona mediante el archivo CSV
    def actualizarZona(nombre, codigo, descripcion, estado, coordenadas, color):
        zona = Zona_inundable.devolverZona(codigo)
        zona.nombre = nombre
        zona.descripcion=descripcion
        zona.estado = estado
        zona.coordenadas = coordenadas
        zona.color = color
        db.session.commit()
    
#---Actualizacion de zona mediante el formulario ---------------------------------------
        
    #actualizacion personalizada
    def actualizarNombre(nombre, id):
        zona = Zona_inundable.getIdZona(id)
        zona.nombre = nombre
        db.session.commit()
        
    #actualizacion personalizada
    def actualizarDescripcion(descripcion, id):
        zona = Zona_inundable.getIdZona(id)
        zona.descripcion = descripcion
        db.session.commit()
        
    #actualizacion personalizada
    def actualizarEstado(estado, id):
        zona = Zona_inundable.getIdZona(id)
        zona.estado = estado
        db.session.commit()
 
    #actualizacion personalizada
    def actualizarColor(color, id):
        zona = Zona_inundable.getIdZona(id)
        zona.color = color
        db.session.commit()

    #actualizacion personalizada
    def actualizarCodigo(codigo, id):
        zona = Zona_inundable.getIdZona(id)
        zona.codigo = codigo
        db.session.commit()

#---- Para API ---------------------------------
    def parsearLista(coord):
        x = 2
        final_list= lambda coord, x: [coord[i:i+x] for i in range(0, len(coord), x)]
        output=final_list(coord, x)
        return output
        
    def zonaApi(idZona):
        zona = Zona_inundable.getIdZona(idZona)
        dict = {}
        if zona == None:
            dict['error'] = "No existe zona con el id ingresado"
            return jsonify(dict)
        else:
            lista = []
            dict ["id"] = zona.id
            dict ["nombre"] = zona.nombre
            dict ["coordenadas"] = Zona_inundable.parsearLista(zona.coordenadas.split(" "))
            dict ["color"]= zona.color
            dict ["descripcion"] = zona.descripcion
            lista.append(dict)
            diccio={'atributos' : lista}
            return jsonify(diccio)
    
    # def zonaApiAll(elementosxPagina):
    #     zonasResultado = Zona_inundable.getAll()
    #     zonas = []
    #     for zona in zonasResultado:
    #         zonas.append({ "id": zona.id, "nombre": zona.nombre, "coordenadas": Zona_inundable.parsearLista(zona.coordenadas.split(" ")), "color": zona.color })
    #     cantidad = len(zonas)
    #     paginas = cantidad % elementosxPagina
    #     diccionario = { "zonas": zonas, "total": cantidad, "paginas": paginas, "elementosxPagina": elementosxPagina }
    #     return jsonify(diccionario)

    def zonaApiAll(pagina, elementosxPagina):
        zonasAll = []
        diccionario = {}
        zonasInundables = []
        zonas = Zona_inundable.getAll()
        page = int(pagina)
        paginas = len(zonas) // elementosxPagina

        if (len(zonas) % elementosxPagina) > 0:
            paginas = paginas + 1
        
        
        if ((page > 0) and (page <= paginas)):                
            zonasPaginaActual = Zona_inundable.query.paginate(page=page, per_page=elementosxPagina)
            cantidadPaginaActual = 0
            for zona in zonasPaginaActual.items:
                cantidadPaginaActual += 1
                zonasInundables.append({ "id": zona.id, "nombre": zona.nombre, "coordenadas": Zona_inundable.parsearLista(zona.coordenadas.split(" ")), "descripcion": zona.descripcion, "color": zona.color })
            diccionario = { "zonas": zonasInundables, "total": cantidadPaginaActual, "pagina": page }
            zonasAll.append(diccionario)
            #zonasInundables = []
            return jsonify(zonasAll), 200
        else:
            diccio = {}
            diccio['error'] = "No existe la pagina ingresada"
            return jsonify(diccio), 404