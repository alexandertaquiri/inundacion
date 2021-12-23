from os import write
from sqlalchemy.sql.expression import _False
from app.models.puntoEncuentro import PuntoEncuentro
from app.models.coordenada import Coordenada
from app.db import db
from flask import redirect, render_template, request, url_for, abort, session
from flask import jsonify
import ast
from app.helpers.auth import authenticated
from app.helpers.auth import authenticated_con_permisos
from app.resources.configuracion import datosDeConfiguracion


def obtenerCoordenada(idCoordenada):
    return Coordenada.query.filter_by(id = idCoordenada).first()


def obtenerDiccionario(p, latitud, longitud):
    diccionario={}
    diccionario["id"]=p.id
    diccionario["nombre"]=p.nombre
    diccionario["direccion"]=p.direccion
    diccionario["estado"]=p.estado
    diccionario["telefono"]=p.telefono
    diccionario["email"]=p.email
    diccionario["latitud"]=latitud
    diccionario["longitud"]=longitud
    return diccionario


def list():
    user = authenticated_con_permisos(session, "punto_encuentro_show")
    if user == None:
        abort(401)

    #agregado para configuracion
    datosConfig = datosDeConfiguracion()

    page = request.args.get('page', 1, type=int)
    puntosEncuentro = PuntoEncuentro.query.paginate(page=page, per_page=datosConfig['cantidad'])
    return render_template('puntosEncuentro/index.html', puntosEncuentro=puntosEncuentro, user=user, datosConfig=datosConfig)
        

def byNombre():
    user = authenticated_con_permisos(session, "punto_encuentro_show")
    if user == None:
        abort(401)

    #agregado para configuracion
    datosConfig = datosDeConfiguracion()


    nombre = request.args.get("byNombre")
    page = request.args.get('page', 1, type=int)
    puntosEncuentro = PuntoEncuentro.query.filter_by(nombre = nombre).paginate(page=page, per_page=datosConfig['cantidad'])
    return render_template('puntosEncuentro/index.html', puntosEncuentro=puntosEncuentro, user=user, datosConfig=datosConfig)


def estado():
    user = authenticated_con_permisos(session, "punto_encuentro_show")
    if user == None:
        abort(401)

    datosConfig = datosDeConfiguracion()

    estado = request.form.get("select")
    page = request.args.get('page', 1, type=int)
    if (estado != "Todos"):
        puntosEncuentro = PuntoEncuentro.query.filter_by(estado = estado).paginate(page=page, per_page=datosConfig['cantidad'])
    else: 
        puntosEncuentro = PuntoEncuentro.query.paginate(page=page, per_page=datosConfig['cantidad'])  
    return render_template('puntosEncuentro/index.html', puntosEncuentro=puntosEncuentro, user=user, datosConfig=datosConfig)


def new():
    user = authenticated_con_permisos(session, "punto_encuentro_new")
    if user == None:
        abort(401)

    errores = ast.literal_eval(request.args.get("errores")) if request.args.get("errores") else " "
    datos = ast.literal_eval(request.args.get("datos")) if request.args.get("datos") else " "
    return render_template("puntosEncuentro/new.html", errores=errores, datos=datos, datosConfig=datosDeConfiguracion())


def create():   
    user = authenticated_con_permisos(session, "punto_encuentro_create")
    if user == None:
        abort(401)

    errores = PuntoEncuentro.exist(request.form.get("nombre"), request.form.get("calles") + " " + request.form.get("altura"), request.form.get("prefijo") + request.form.get("numero"), request.form.get("email"))
    datos = request.form.to_dict()
    
    if errores:
        db.session.rollback()
        return redirect(url_for("puntosEncuentro_new", errores=errores, datos=datos, datosConfig=datosDeConfiguracion()))

    errores = PuntoEncuentro.validar(request.form)

    if errores:
        db.session.rollback()
        return redirect(url_for("puntosEncuentro_new", errores=errores, datos=datos, datosConfig=datosDeConfiguracion()))
    else:
        PuntoEncuentro.create(request.form.get("nombre"), request.form.get("calles") + " " + request.form.get("altura"), 
        request.form.get("estado"), request.form.get("latitud"), request.form.get("longitud"), request.form.get("prefijo") + request.form.get("numero"), request.form.get("email"))
        return redirect(url_for("puntosEncuentro_list"))


def viewModify():
    user = authenticated_con_permisos(session, "punto_encuentro_update")
    if user == None:
        abort(401)

    punto = PuntoEncuentro.query.filter_by(id = request.form.get("idModificar")).first()
    coordenada = Coordenada.obtenerCoordenada(punto.coordenada_id)
    diccionario = obtenerDiccionario(punto, coordenada.latitud, coordenada.longitud)
    errores = ast.literal_eval(request.args.get("errores")) if request.args.get("errores") else " "
    return render_template("puntosEncuentro/viewModify.html", errores=errores, datos=diccionario, datosConfig=datosDeConfiguracion())


def modify():
    user = authenticated_con_permisos(session, "punto_encuentro_update")
    if user == None:
        abort(401)

    errores = {}
    diccionario = {}
    diccionario["id"] = request.form.get("idModificar")
    punto = PuntoEncuentro.query.get(request.form.get("idModificar"))
    coordenada = Coordenada.obtenerCoordenada(punto.coordenada_id)


    nombreNuevo = request.form.get("nombre")
    if punto.nombre != nombreNuevo:
        diccionario["nombre"] = nombreNuevo
        if not PuntoEncuentro.nombreExisteEnDb(nombreNuevo):
            errorNombre = PuntoEncuentro.validarNombre(nombreNuevo)
            if errorNombre is not None:
                errores["error_nombre"] = errorNombre
            else:
                punto.nombre = nombreNuevo  
        else:        
            errores["error_nombre"] = "El nombre ya existe en otro punto de encuentro"     
    else:
        diccionario["nombre"] = punto.nombre


    direccionNueva = request.form.get("direccion")
    if punto.direccion != direccionNueva:
        diccionario["direccion"] = direccionNueva
        if not PuntoEncuentro.direccionExisteEnDb(direccionNueva):
            errorDireccion = PuntoEncuentro.validarDireccion(direccionNueva)
            if errorDireccion is not None:
                errores["error_direccion"] = errorDireccion
            else:
                punto.direccion = direccionNueva  
        else:
            errores["error_direccion"] = "La dirección ya existe en otro punto de encuentro"     
    else:
        diccionario["direccion"] = punto.direccion

    
    punto.estado = request.form.get("estado")
    diccionario["estado"] = punto.estado


    latitudNueva = request.form.get("latitud")
    longitudNueva = request.form.get("longitud")
    diccionario["latitud"] = latitudNueva
    diccionario["longitud"] = longitudNueva
    coordenadaLatitud = Coordenada.query.filter_by(latitud = latitudNueva).first()
    coordenadaLongitud = Coordenada.query.filter_by(longitud = longitudNueva).first()

    if ((coordenadaLatitud is not None) and (coordenadaLongitud is not None) and (latitudNueva != coordenada.latitud) and (longitudNueva != coordenada.longitud)):
        if (coordenadaLatitud.id == coordenadaLongitud.id):
            errores["error_coordenada"] = "La ubicación geográfica ya existe en otro punto de encuentro"
    else:
        if ((latitudNueva != coordenada.latitud) and (longitudNueva != coordenada.longitud)):
            if coordenada.latitud != latitudNueva:
                diccionario["latitud"] = latitudNueva
                errorCoordenada = PuntoEncuentro.validarCoordenada(latitudNueva)
                if errorCoordenada is not None:
                    errores["error_coordenada"] = errorCoordenada
                else:
                    coordenada.latitud = latitudNueva
            else:
                diccionario["latitud"] = coordenada.latitud

            if coordenada.longitud != longitudNueva:
                diccionario["longitud"] = longitudNueva
                errorCoordenada = PuntoEncuentro.validarCoordenada(longitudNueva)
                if errorCoordenada is not None:
                    errores["error_coordenada"] = errorCoordenada
                else:
                    coordenada.longitud = longitudNueva       
            else:
                diccionario["longitud"] = coordenada.longitud


    telefonoNuevo = request.form.get("telefono")
    if punto.telefono != telefonoNuevo:
        diccionario["telefono"] = telefonoNuevo
        if not PuntoEncuentro.telefonoExisteEnDb(telefonoNuevo):
            errorTelefono = PuntoEncuentro.validarTelefono(telefonoNuevo)
            if errorTelefono is not None:
                errores["error_telefono"] = errorTelefono  
            else:
                punto.telefono = telefonoNuevo
        else:     
            errores["error_telefono"] = "El teléfono ya existe en otro punto de encuentro" 
    else:
        diccionario["telefono"] = punto.telefono


    emailNuevo = request.form.get("email")
    if punto.email != emailNuevo:
        diccionario["email"] = emailNuevo
        if not PuntoEncuentro.emailExisteEnDb(emailNuevo):
            errorEmail = PuntoEncuentro.validarEmail(emailNuevo)
            if errorEmail is not None:
                errores["error_email"] = errorEmail 
            else:
                punto.email = emailNuevo
        else:    
            errores["error_email"] = "El email ya existe en otro punto de encuentro" 
    else:
        diccionario["email"] = punto.email


    if errores:
        db.session.rollback()
        return render_template("puntosEncuentro/viewModify.html", errores=errores, datos=diccionario, datosConfig=datosDeConfiguracion())
    else:
        db.session.commit()
        return redirect(url_for("puntosEncuentro_list"))
    

def delete():
    user = authenticated_con_permisos(session, "punto_encuentro_destroy")
    if user == None:
        abort(401)

    idBorrar = request.form.get("idBorrar")
    punto = PuntoEncuentro.query.get(idBorrar)
    coordenada = Coordenada.obtenerCoordenada(punto.coordenada_id)
    PuntoEncuentro.delete(punto)
    Coordenada.delete(coordenada)
    return redirect(url_for("puntosEncuentro_list"))
