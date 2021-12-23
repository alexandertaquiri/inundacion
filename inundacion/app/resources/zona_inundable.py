from app.db import db
from flask import redirect, render_template, request, url_for, abort, session


from app.models.configuracion import Configuracion
from app.resources.configuracion import datosDeConfiguracion

from app.models.criterio import Criterio_ord

#importado para los permisos
from app.models.user import User
from app.models.zona_inundable import Zona_inundable

from app.helpers.auth import authenticated
from app.helpers.auth import authenticated_con_permisos


import json
import csv
import os.path
import io


#Principal para listar zonas inundables
def index():
   #chequeando logueo y permisos
   user = authenticated_con_permisos(session, "zona_inundable_show")
   if user == None:
      abort(401)

   #obtengo los datos de la configuracion 
   datosConfig = datosDeConfiguracion()
   
   page = request.args.get('page', 1, type=int)

   zonas = Zona_inundable.query.paginate(page=page, per_page=datosConfig["cantidad"])
   

      
   return render_template("zona_inundable/index.html",
                          title="Listado zonas inundables", 
                          user=user,
                          datosConfig=datosConfig,
                          zonas=zonas,
                          )
   
#para busqueda por nombre    
def byNombre():
    user = authenticated_con_permisos(session, "zona_inundable_show")
    if user == None:
        abort(401)

    datosConfig = datosDeConfiguracion()

    nombre = request.args.get("byNombre")
    page = request.args.get('page', 1, type=int)
    zonas = Zona_inundable.query.filter_by(nombre = nombre).paginate(page=page, per_page=datosConfig["cantidad"])
    return render_template('zona_inundable/index.html', zonas=zonas, user=user, datosConfig=datosConfig)    


#para busqueda por estado
def estado():
    user = authenticated_con_permisos(session, "zona_inundable_show")
    if user == None:
        abort(401)

    datosConfig = datosDeConfiguracion()

    estado = request.form.get("select")
    page = request.args.get('page', 1, type=int)
    if (estado != "Todos"):
        zonas = Zona_inundable.query.filter_by(estado = estado).paginate(page=page, per_page=datosConfig["cantidad"])
    else: 
        zonas = Zona_inundable.query.paginate(page=page, per_page=datosConfig["cantidad"])  
    return render_template('zona_inundable/index.html', zonas=zonas, user=user, datosConfig=datosConfig)

#new para importar zonas mediante un archivo CSV
def new():
   
   errores={}
       
   #chequeando logueo y permisos
   user = authenticated_con_permisos(session, "zona_inundable_create")
   if user == None:
      abort(401)

   #obtengo los datos de la configuracion 
   datosConfig = datosDeConfiguracion()
   
   return render_template("zona_inundable/new.html",
                          title="Ingresar archivo csv", 
                          user=user,
                          datosConfig=datosConfig,
                          errores=errores
                          )
    
#create de las zonas inundavbles a travez del archivo CSV
def create():     
   #Verifico permisos 
   user = authenticated_con_permisos(session, "zona_inundable_create")
   if user == None:
      abort(401)   
   
   #obtengo los datos de la configuracion 
   datosConfig = datosDeConfiguracion()
   
   #para la verificacion de errores
   errores = {}
    
   #Obtengo el archivo 
   f = request.files['fileupload']
   if not f:
      errores["error_nombreCompleto"] = "No se ingreso archivo" 
      return render_template("zona_inundable/new.html", title="Ingresar archivo csv", user=user, datosConfig=datosConfig, errores=errores)
    
   #except por si se ingresa un tipo de archivo distinto al .csv ------------
   try:
        #------ Decodifico el archivo CSV---------
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
   except UnicodeDecodeError:
       errores["error_extension_archivo"] = "Error en el tipo de archivo. Ingrese un archivo con extension '.csv'"
       return render_template("zona_inundable/new.html", title="Ingresar archivo csv", user=user, datosConfig=datosConfig, errores=errores)
           
   csv_input = csv.reader(stream, delimiter=',')

   #datos de encabezado 
   encabezado = next(csv_input)
   
   #except por si se ingresa un tipo de archivo con una confeccion incorrecta csv ------------  
   try:          
    for row in csv_input:
            nombre = row[0]
            codigo = row[1]
            estado = row[2]
            color = row[3]
            descripcion = row[4]       
            coordenadas = row[5]   
            if (Zona_inundable.devolverZona(codigo)) == None:
                #creamos la zona
                Zona_inundable.crear(nombre, codigo, descripcion, estado, coordenadas, color)          
                #caso exitoso de alta
                errores["sin_errores"] = "Altas exitosas de zonas inundables" 
            else:                   
                #actualizamos zona ya existente
                Zona_inundable.actualizarZona(nombre, codigo, descripcion, estado, coordenadas, color)
                #caso exitoso de alta
                errores["sin_errores_update"] = "Actualizacion exitosa de zonas inundables"
   except IndexError:
        errores["error_tipo_archivo"] = "Error por confección incorrecta del archivo '.csv'"
        return render_template("zona_inundable/new.html", title="Ingresar archivo csv", user=user, datosConfig=datosConfig, errores=errores)

   return render_template("zona_inundable/new.html", title="Ingresar archivo csv", user=user, datosConfig=datosConfig, errores=errores)
     
#borrado
def delete():
    user = authenticated_con_permisos(session, "zona_inundable_destroy")
    if user == None:
        abort(401)

    idBorrar = request.form.get("idBorrar")
    
    Zona_inundable.borrar(idBorrar)
    
    return redirect(url_for("zona_index"))    

#funcion que devuelve los datos de la base de datos del id por parametro
def datos_bd_zona(id):

    #accedo a la zona en la base de datos
    zona = Zona_inundable.getIdZona(id)

    coordenadas = zona.coordenadas.split(' ')
    
    diccio = {}
    #-----------------------
    
    diccio["id"] = zona.id
    diccio["nombre"] = zona.nombre
    diccio["descripcion"] = zona.descripcion
    diccio["codigo"] = zona.codigo
    diccio["estado"] = zona.estado
    diccio["coordenadas"] = zona.coordenadas
    diccio["color"] = zona.color
    diccio["cantidad_puntos"] = int(len(coordenadas) / 2)    
    
    return diccio

#visualizar
def visualizar():
    user = authenticated_con_permisos(session, "zona_inundable_show")
    if user == None:
        abort(401)

    #obtengo los datos de la configuracion 
    datosConfig = datosDeConfiguracion()

    #obtengo el id enviado por url
    idVisualizar = request.args.get('id_vizualizar')
    
    return render_template("zona_inundable/visualizar.html", title="Ver Zona", user=user, datosConfig=datosConfig, diccio=datos_bd_zona(idVisualizar))

#modificar
def modificar():
    #para validaciones
    errores = {}
    
    user = authenticated_con_permisos(session, "zona_inundable_update")
    if user == None:
        abort(401)

    #obtengo los datos de la configuracion 
    datosConfig = datosDeConfiguracion()

    #obtengo id de la url
    id_zona = request.args.get('id') 
        
    return render_template("zona_inundable/edit.html", title="Editar Zona", user=user, datosConfig=datosConfig, diccio=datos_bd_zona(id_zona), errores=errores)

#confirmacion y validacion del modificar
def modificar_confirm():
    #verificacion de permisos
    user = authenticated_con_permisos(session, "zona_inundable_update")
    if user == None:
        abort(401)

    #obtengo los datos de la configuracion 
    datosConfig = datosDeConfiguracion()

    #obtengo parametros
    datos_form =request.form
    
    nombre = datos_form['nombre']
    codigo = datos_form['codigo']
    descripcion = datos_form['descripcion']
    estado = datos_form['estado']
    color = datos_form['color']
    id_zona = datos_form['idModificar']
    
    #obtengo datos de la base de datos
    datos = datos_bd_zona(id_zona)
    
    #diccionario de errores
    errores = {}
    
    #para control si no se cambio nada
    sin_cambios=True
    
    #validar nombre datos
    if (len(nombre.strip()) == 0):
        errores['nombre_vacio'] = 'El nombre no puede ser vacio'
        sin_cambios = False 
    elif (nombre != datos['nombre']):
        Zona_inundable.actualizarNombre(nombre, id_zona)
        errores['nombre_ok'] = 'Actualizacion de nombre exitosa'    
        sin_cambios = False
    #--------------------
    if (len(codigo.strip()) == 0):
        errores['codigo_vacio'] = 'El codigo no puede ser vacio' 
        sin_cambios = False
    elif (codigo != datos['codigo']):
        sin_cambios = False        
        if (Zona_inundable.devolverZona(codigo)) == None:
            Zona_inundable.actualizarCodigo(codigo, id_zona)
            errores['codigo_ok'] = 'Actualizacion exitosa de codigo'
        else:
            errores['codigo_repetido'] = 'El codigo ' + str(codigo) + ' ya existe en el sistema'
    #--------------------
    if (len(descripcion.strip()) == 0):
        errores['descripcion_vacio'] = 'La descripcion no puede ser vacia' 
        sin_cambios = False
    elif (descripcion != datos['descripcion']):
        Zona_inundable.actualizarDescripcion(descripcion, id_zona)
        errores['descripcion_ok'] = 'Actualizacion exitosa de descripcion'
        sin_cambios = False
    #--------------------
    if (int(estado) != datos['estado']):
        Zona_inundable.actualizarEstado(estado, id_zona)
        errores['estado_ok'] = 'Actualizacion exitosa de estado'
        sin_cambios = False
    #--------------------
    if (color != datos['color']):
        Zona_inundable.actualizarColor(color, id_zona)
        errores['color_ok'] = 'Actualizacion exitosa de color'
        sin_cambios = False
    
    if (sin_cambios):
        errores['sin_cambios'] = 'No se ingresaron datos nuevos'
    
    return render_template("zona_inundable/edit.html", title="Editar Zona", user=user, datosConfig=datosConfig, diccio=datos_bd_zona(id_zona), errores=errores)