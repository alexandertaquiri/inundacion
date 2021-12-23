from os import write
from sqlalchemy.sql.expression import _False
from app.models.recorridoEvacuacion import RecorridoEvacuacion
from app.db import db
from flask import redirect, render_template, request, url_for, abort, session
from flask import jsonify
import ast
from app.helpers.auth import authenticated
from app.helpers.auth import authenticated_con_permisos
from app.resources.configuracion import datosDeConfiguracion


def obtenerDiccionario(recorrido):
    estado = ""
    if (recorrido.publicado):
        estado = "Publicado"
    else:
        estado = "Despublicado"
    
    diccionario={}
    diccionario["id"]=recorrido.id
    diccionario["nombre"]=recorrido.nombre
    diccionario["descripcion"]=recorrido.descripcion

    diccionario["estado"]=estado
    diccionario["coordenadas"]=recorrido.coordenadas
    return diccionario


def list():
    user = authenticated_con_permisos(session, "recorrido_evacuacion_show")
    if user == None:
        abort(401)
    
    criterios = {}

    #agregado para configuracion
    datosConfig = datosDeConfiguracion()
    criterios["index"] = "index"

    page = request.args.get('page', 1, type=int)
    recorridosEvacuacion = RecorridoEvacuacion.query.paginate(page=page, per_page=datosConfig['cantidad'])
    return render_template('recorridosEvacuacion/index.html', criterios=criterios, recorridosEvacuacion=recorridosEvacuacion, user=user, datosConfig=datosConfig)


def byNombre():
    user = authenticated_con_permisos(session, "recorrido_evacuacion_show")
    if user == None:
        abort(401)

    criterios = {}

    #agregado para configuracion
    datosConfig = datosDeConfiguracion()

    if request.args.get("byNombre"):
        nombre = request.args.get("byNombre")
    else:
        nombre = request.form.get("byNombre")

    criterios["nombre"] = nombre

    page = request.args.get('page', 1, type=int)
    recorridosEvacuacion = RecorridoEvacuacion.query.filter(RecorridoEvacuacion.nombre.like('%' + nombre + '%')).paginate(page=page, per_page=datosConfig['cantidad'])
    return render_template('recorridosEvacuacion/index.html', criterios=criterios, recorridosEvacuacion=recorridosEvacuacion, user=user, datosConfig=datosConfig)


def estado():
    user = authenticated_con_permisos(session, "recorrido_evacuacion_show")
    if user == None:
        abort(401)

    criterios = {}

    datosConfig = datosDeConfiguracion()
    page = request.args.get('page', 1, type=int)

    if request.args.get("estado"):
        estado = request.args.get("estado")
    else:
        estado = request.form.get("select")

    criterios["estado"] = estado

    if (estado != "Todos"):
        recorridosEvacuacion = RecorridoEvacuacion.query.filter_by(publicado = estado).paginate(page=page, per_page=datosConfig['cantidad'])
        return render_template('recorridosEvacuacion/index.html', criterios=criterios, recorridosEvacuacion=recorridosEvacuacion, user=user, datosConfig=datosConfig)
    else: 
        return redirect(url_for("recorridosEvacuacion_list"))
    

def new():
    user = authenticated_con_permisos(session, "recorrido_evacuacion_new")
    if user == None:
        abort(401)

    errores = ast.literal_eval(request.args.get("errores")) if request.args.get("errores") else " "
    datos = ast.literal_eval(request.args.get("datos")) if request.args.get("datos") else " "
    return render_template("recorridosEvacuacion/new.html", errores=errores, datos=datos, datosConfig=datosDeConfiguracion())


def create():   
    user = authenticated_con_permisos(session, "recorrido_evacuacion_create")
    if user == None:
        abort(401)

    diccionario = {}    
    coordenadas = request.form.get("coordenadas")
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    estado = request.form.get("estado")
    
    diccionario["nombre"] = nombre
    diccionario["estado"] = estado
    diccionario["descripcion"] = descripcion

    latLong = request.form.get("coordenadas").split(",")        
    if (len(latLong) >= 6):
        diccionario["coordenadas"] = coordenadas

    errores = RecorridoEvacuacion.exist(nombre)
    
    if errores:
        return redirect(url_for("recorridosEvacuacion_new", errores=errores, datos=diccionario, datosConfig=datosDeConfiguracion()))

    errores = RecorridoEvacuacion.validar(request.form)

    if errores:
        return redirect(url_for("recorridosEvacuacion_new", errores=errores, datos=diccionario, datosConfig=datosDeConfiguracion()))
    else:
        RecorridoEvacuacion.create(nombre, descripcion, estado, coordenadas)
        return redirect(url_for("recorridosEvacuacion_list"))


def viewModify():
    user = authenticated_con_permisos(session, "recorrido_evacuacion_update")
    if user == None:
        abort(401)

    recorrido = RecorridoEvacuacion.query.filter_by(id = request.form.get("idModificar")).first()
    
    diccionario = obtenerDiccionario(recorrido)
 
    errores = ast.literal_eval(request.args.get("errores")) if request.args.get("errores") else " "
    return render_template("recorridosEvacuacion/viewModify.html", errores=errores, datos=diccionario, datosConfig=datosDeConfiguracion())


def delete():
    user = authenticated_con_permisos(session, "recorrido_evacuacion_destroy")
    if user == None:
        abort(401)

    idBorrar = request.form.get("idBorrar")
    recorrido = RecorridoEvacuacion.query.get(idBorrar)
    RecorridoEvacuacion.delete(recorrido)
    return redirect(url_for("recorridosEvacuacion_list"))


def modify():   
    user = authenticated_con_permisos(session, "recorrido_evacuacion_update")
    if user == None:
        abort(401)

    errores = {}
        
    diccionario = {}
    idModificar = request.form.get("idModificar")    
    coordenadas = request.form.get("coordenadas")
    nombreNuevo = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    estado = request.form.get("estado")

    recorrido = RecorridoEvacuacion.query.get(idModificar)

    if recorrido.nombre != nombreNuevo:
        diccionario["nombre"] = nombreNuevo
        if not RecorridoEvacuacion.nombreExisteEnDb(nombreNuevo):
            errorNombre = RecorridoEvacuacion.validarNombre(nombreNuevo)
            if errorNombre is not None:
                errores["error_nombre"] = errorNombre  
            else:
                recorrido.nombre = nombreNuevo
        else:     
            errores["error_nombre"] = "El nombre ya existe en otro recorrido de evacuación" 
    else:
        diccionario["nombre"] = recorrido.nombre

    if recorrido.descripcion != descripcion:
        diccionario["descripcion"] = descripcion
        if not 4 <= len(descripcion) <= 150:
            errores["error_descripcion"] = "La descripción es incorrecta"
        else:
            recorrido.descripcion = descripcion
    else:
        diccionario["descripcion"] = recorrido.descripcion

    diccionario["descripcion"] = descripcion
    diccionario["id"] = idModificar
    diccionario["coordenadas"] = coordenadas
    recorrido.coordenadas = coordenadas
    recorrido.descripcion = descripcion

    if estado == "0":
        recorrido.publicado = False
        diccionario["estado"] = "Despublicado"
    else:
        recorrido.publicado = True
        diccionario["estado"] = "Publicado"

    if errores:
        return render_template("recorridosEvacuacion/viewModify.html", errores=errores, datos=diccionario, datosConfig=datosDeConfiguracion())
    else:
        db.session.commit()
        return redirect(url_for("recorridosEvacuacion_list"))