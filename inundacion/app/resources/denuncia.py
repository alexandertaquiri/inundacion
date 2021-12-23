from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.models.configuracion import Configuracion
from app.resources.configuracion import datosDeConfiguracion
from app.models.criterio import Criterio_ord
from app.helpers.auth import authenticated_con_permisos
from app.helpers.auth import authenticated
from datetime import date
from app.models.denuncia import Denuncia
from app.models.denunciaSeguimiento import Denuncia_seguimiento 
from app.models.denuncia_categoria import DenunciaCategoria
from sqlalchemy import desc, asc
from datetime import date, timedelta
from sqlalchemy.sql.sqltypes import DATETIME
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import query
import datetime 
import ast
from wtforms import Form, StringField, validators, ValidationError, SelectField
from wtforms.fields.simple import HiddenField


estados = ["Sin confirmar", "En curso", "Resuelta", "Cerrada"] 
categorias = [('Basural', 'Basural'), ('Alcantarilla tapada', 'Alcantarilla tapada')]

categorias1 = [('1', '1'), ('2', '2'), ('3', '3')]


def index():
    user = authenticated_con_permisos(session, "denuncia_show")
    if user == None:
        abort(401)

    criterios = {}
    criterios["index"] = "index"

    datosConfig = datosDeConfiguracion()
    page = request.args.get('page', 1, type=int)
    denuncias = Denuncia.query.paginate(page=page, per_page=datosConfig["cantidad"])
    
    # # categorias= DenunciaCategoria.categoriaConNombre("nombre")

    categorias = DenunciaCategoria.all()

    # print (categorias[0].id_categoria)

    return render_template("denuncia/index.html", categorias=categorias, criterios=criterios, denuncias=denuncias, usr=user, datosConfig=datosConfig)

def byTitulo():
    user = authenticated_con_permisos(session, "denuncia_show")
    if user == None:
        abort(401)

    criterios = {}

    datosConfig = datosDeConfiguracion()

    if request.args.get("byTitulo"):
        titulo = request.args.get("byTitulo")
    else:
        titulo = request.form.get("byTitulo")

    criterios["byTitulo"] = titulo

    page = request.args.get('page', 1, type=int)

    print (titulo)

    if (titulo != None):
        denuncias = Denuncia.query.filter(Denuncia.titulo.like('%'+titulo+'%')).paginate(page=page, per_page=datosConfig["cantidad"])

        return render_template('denuncia/index.html', criterios=criterios, denuncias=denuncias, usr=user, datosConfig=datosConfig)
    else:
         return redirect(url_for("denuncia_list"))
         
           


def estado():
    user = authenticated_con_permisos(session, "denuncia_show")
    if user == None:
        abort(401)

    criterios = {}

    datosConfig = datosDeConfiguracion()

    if request.args.get("estado"):
        estado = request.args.get("estado")
    else:
        estado = request.form.get("select")

    criterios["estado"] = estado
    page = request.args.get('page', 1, type=int)

    if (estado != "Todas"):
        denuncias = Denuncia.query.filter_by(estado = estado).paginate(page=page, per_page=datosConfig["cantidad"])
        return render_template('denuncia/index.html', criterios=criterios, denuncias=denuncias, usr=user, datosConfig=datosConfig)
    else: 
        return redirect(url_for("denuncia_list"))


def filtrarPorFecha():
    user = authenticated_con_permisos(session, "denuncia_show")
    if user == None:
        abort(401)

    criterio1= {}

    criterio2= {}

    datosConfig = datosDeConfiguracion()

    if request.args.get("fecha_inicio"):
        fechaCreacion = request.args.get("fecha_inicio")
    else:
        fechaCreacion = request.args.get("fecha_inicio")

    if request.args.get("fecha_fin"):
        fechaCierre = request.args.get("fecha_fin")
    else:
        fechaCierre = request.args.get("fecha_fin")

    criterio1["fecha_inicio"] = fechaCreacion

    criterio2["fecha_fin"] = fechaCierre
 

    page = request.args.get('page', 1, type=int)

    denuncias = db.session.query(Denuncia)

    denuncias =  BaseQuery.intersect(denuncias.filter(Denuncia.fecha_creacion >= fechaCreacion), denuncias.filter(Denuncia.fecha_creacion <= fechaCierre))

    denuncias = denuncias.paginate(page=page, per_page=datosConfig["cantidad"])
    
    print (denuncias)

    # print (fechaCreacion)

    # print (fechaCierre)

    print (criterio1)

    print (criterio2)
    
    if ( fechaCierre == '' or fechaCreacion == ''):
        return redirect(url_for("denuncia_list"))
    else:

         return render_template('denuncia/index.html', criterio1=criterio1, criterio2=criterio2, denuncias=denuncias, usr=user, datosConfig=datosConfig)

def delete():

    user = authenticated_con_permisos(session, "denuncia_destroy")

    if user == None:
        abort(401)

    idBorrar = request.form.get("idBorrar")
    denuncia = Denuncia.query.get(idBorrar)
    Denuncia.delete(denuncia)
    
    return redirect(url_for("denuncia_list")) 

#new para agregar una nueva denuncia
def new():
    #chequeando logueo y permisos
    user = authenticated_con_permisos(session, "denuncia_new")
    if user == None:
        abort(401)
        
    #obtengo los datos de la configuracion 
    datosConfig = datosDeConfiguracion()

    page = request.args.get('page', 1, type=int)

    users = User.query.paginate(page=page, per_page=datosConfig["cantidad"])

    categorias = DenunciaCategoria.query.paginate(page=page, per_page=datosConfig["cantidad"])

    datos = ast.literal_eval(request.args.get("datos")) if request.args.get("datos") else " "
   
    categorias_all = DenunciaCategoria.all()

    print (categorias_all[0].id_categoria)

    print (categorias_all[0].nombre)



    return render_template("denuncia/new.html", categorias_all=categorias_all, categorias=categorias, users=users, usr=user, datos=datos, datosConfig=datosConfig)

def create():
    #creamos la denuncia
    Denuncia.crear(
        request.form.get("titulo"),
        request.form.get("id_categoria"),
        request.form.get("descripcion"),
        request.form.get("latitud"),
        request.form.get("longitud"),
        request.form.get("asignado_a"),
        request.form.get("apellido_denunciante"),
        request.form.get("nombre_denunciante"),
        request.form.get("tel_cel_denunciante"),
        request.form.get("email_denunciante")
    ) 

    return redirect(url_for("denuncia_list"))

def obtenerDiccionario(d):
    diccionario={}
    diccionario["id"]=d.id
    diccionario["nombre_denunciante"]=d.nombre_denunciante
    diccionario["apellido_denunciante"]=d.apellido_denunciante
    diccionario["descripcion"]=d.descripcion
    diccionario["titulo"]=d.titulo
    diccionario["categoria_id"]=d.categoria_id
    diccionario["tel_cel_denunciante"]=d.tel_cel_denunciante
    diccionario["email_denunciante"]=d.email_denunciante
    diccionario["longitud"]=d.longitud
    diccionario["latitud"]=d.latitud
    diccionario["asignado_a"]=d.asignado_a
    diccionario["estado"]=d.estado
   
    return diccionario

def viewModify():
    # user=User.getAll()
    # print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    # print(user)
    # denuncia = Denuncia.query.filter_by(id = request.form.get("idModificar")).first()
    # print(denuncia)
    # diccionario = obtenerDiccionario(denuncia)
    # errores = ast.literal_eval(request.args.get("errores")) if request.args.get("errores") else " "
    # return render_template("denuncia/viewModify.html",errores=errores, datos=diccionario, users=user, datosConfig=datosDeConfiguracion())
    user=User.getAll()
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    print(user)
    #gategorias=DenunciaCategoria.all()
    denuncia = Denuncia.query.filter_by(id = request.form.get("idModificar")).first()
    print(denuncia)
    diccionario = obtenerDiccionario(denuncia)
    errores = ast.literal_eval(request.args.get("errores")) if request.args.get("errores") else " "

    page = request.args.get('page', 1, type=int)
    datosConfig = datosDeConfiguracion()
    categorias = DenunciaCategoria.query.paginate(page=page, per_page=datosConfig["cantidad"])
    categorias_all = DenunciaCategoria.all()

    return render_template("denuncia/viewModify.html",errores=errores, denuncia=denuncia,categorias=categorias, categorias_all=categorias_all, datos=diccionario, users=user, datosConfig=datosDeConfiguracion())


def modify():
    
    user = authenticated_con_permisos(session, "denuncia_update")
    if user == None:
        abort(401)

    errores = {}
    diccionario ={}
    
    diccionario["id"] = request.form.get("idModificar")
    print("###########################")
    print(diccionario)
    denuncia = Denuncia.query.get(request.form.get("idModificar"))

    nombre = request.form.get("nombre_denunciante")
    errorNombre = Denuncia.validarNombre(nombre)
    if errorNombre is not None:
        errores["error_nombre"] = errorNombre
    else:
        denuncia.nombre_denunciante = nombre  
     
    #denuncia.nombre_denunciante = nombre


        

    apellido = request.form.get("apellido_denunciante")
    errorApellido = Denuncia.validarApellido(apellido)
    if errorApellido is not None:
        errores["error_apellido"] = errorApellido
    else:
        denuncia.apellido_denunciante = apellido 
    #denuncia.apellido_denunciante = apellido

    telefono = request.form.get("tel_cel_denunciante")
    errorTelefono = Denuncia.validarTelefono(telefono)
    if errorTelefono is not None:
        errores["error_telefono"] = errorTelefono
    else:
        denuncia.tel_cel_denunciante = telefono 
    #denuncia.tel_cel_denunciante = telefono

    email = request.form.get("email_denunciante")
    
    denuncia.email_denunciante =email 

    descrip = request.form.get("descripcion")
    # diccionario["descripcion"] = titulo_d
    denuncia.descripcion = descrip


    titulo_d = request.form.get("titulo")
    # diccionario["titulo"] = titulo_d
    denuncia.titulo = titulo_d

    categ= request.form.get("categoria_id")
    # diccionario["categoria"]=categ

    denuncia.categoria_id = categ

    lat= request.form.get("latitud")
    # diccionario["latitud"]=lat
    denuncia.latitud = lat

    long= request.form.get("longitud")
    # diccionario["latitud"]=long
    denuncia.longitud = long

    usr = request.form.get("select")
    denuncia.asignado_a = usr
    if usr is not None:
        if denuncia.intentos_comunicacion == 3:
            denuncia.estado ="cerrado"
        else:
            denuncia.estado= "en curso"    

    #est=request.form.get("sel")
    #denuncia.estado = est


    if errores:
        db.session.rollback()
        return render_template("denuncia/viewModify.html", errores=errores, datos=diccionario, datosConfig=datosDeConfiguracion())
    else:
        db.session.commit()
        return redirect(url_for("denuncia_list")) 



def revision():
    user = authenticated_con_permisos(session, "denuncia_show")
    if user == None:
        abort(401)

    datosConfig = datosDeConfiguracion()
    #user= User.findById(request.args.get("user_id"))
    denuncias= Denuncia.findById(request.args.get("id"))#solo traigo de la base de datos  los datos de una denuncia
    
    


    #denuncias = Denuncia.query.paginate(page=page, per_page=datosConfig["cantidad"])
    return render_template("denuncia/revision.html", denuncias=denuncias, usr=user, datosConfig=datosDeConfiguracion())              

def incrementarIntentos():
    user = authenticated_con_permisos(session, "denuncia_show")
    if user == None:
        abort(401)
   
    
    denuncias= Denuncia.findById(request.args.get("id"))#solo traigo de la base de datos  los datos de una denuncia
    if denuncias.intentos_comunicacion == 3:
        denuncias.estado="cerrado"
        denuncias.fecha_cierre=date.today()
        
        descripcion="No fue posible contactar al denunciante"
        autorSegui=user.username
        seguimiento=Denuncia_seguimiento.crear(descripcion, autorSegui)
        Denuncia.asignarSeguimiento(seguimiento.id, denuncias.id)

    else :   
        denuncias.intentos_comunicacion= denuncias.intentos_comunicacion + 1
    db.session.commit()
    return render_template("denuncia/revision.html", denuncias=denuncias, usr=user, datosConfig=datosDeConfiguracion())

def resolver():
    user = authenticated_con_permisos(session, "denuncia_show")
    if user == None:
        abort(401)
   
    
    denuncias= Denuncia.findById(request.args.get("id"))#solo traigo de la base de datos  los datos de una denuncia
    if denuncias.estado!= 'resuelta':
        denuncias.estado="resuelta"
        denuncias.fecha_cierre=date.today()
        
        descripcion="Denuncia resuelta exitosamente"
        autorSegui=user.username
        seguimiento=Denuncia_seguimiento.crear(descripcion, autorSegui)
        Denuncia.asignarSeguimiento(seguimiento.id, denuncias.id)
        db.session.commit()
    return render_template("denuncia/revision.html", denuncias=denuncias, usr=user, datosConfig=datosDeConfiguracion())


class ValidarFormulario(Form):
    def length(min=1, max=30):
        message = 'Debe tener entre %d y %d caracteres' % (min, max)

        def _length(form, field):
            l = field.data and len(field.data) or 0
            if l < min or max != -1 and l > max:
                raise ValidationError(message)

        return _length
    id = HiddenField('')
    titulo = StringField('Titulo', [validators.DataRequired("Campo requerido"), length(max=25)])
    categoria_id = SelectField('Categoria', [validators.DataRequired("Campo requerido")], choices=categorias1)
    descripcion = StringField('Descripción', [validators.DataRequired("Campo requerido"), length(max=60)])
    latitud = StringField('Latitud', [validators.DataRequired("Campo requerido")])
    longitud = StringField('Longitud', [validators.DataRequired("Campo requerido")])
    apellido_denunciante = StringField('Apellido', [validators.DataRequired("Campo requerido"), length(max=25)])
    nombre_denunciante = StringField('Nombre', [validators.DataRequired("Campo requerido"), length(max=25)])
    tel_cel_denunciante = StringField('Telefono/Celular', [validators.DataRequired("Campo requerido"), length(max=25)])
    email_denunciante = StringField('Email', [validators.DataRequired("Campo requerido"), validators.Email("Formato de email inválido.")])

                











