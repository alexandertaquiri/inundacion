from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.models.configuracion import Configuracion
from app.resources.configuracion import datosDeConfiguracion
from app.models.criterio import Criterio_ord
from app.helpers.auth import authenticated_con_permisos
from app.helpers.auth import authenticated
from app.models.denunciaSeguimiento import Denuncia_seguimiento
from app.models.denuncia import Denuncia 
from sqlalchemy import desc, asc
from datetime import date, timedelta
from app.resources.denuncia import revision


from sqlalchemy.orm import query
 
import ast

def index():
    user = authenticated_con_permisos(session, "denuncia_show")
    if user == None:
        abort(401)

        
       
    denuncias=Denuncia.findById(request.args.get("id"))
    
    
    datosConfig = datosDeConfiguracion()
    
    

    return render_template("denunciaSeguimiento/index.html", denuncias=denuncias, datosConfig=datosConfig)

def new():
    user = authenticated(session)
    if not authenticated(session):
        abort(401)

    datosConfig = datosDeConfiguracion()
    denuncias= Denuncia.findById(request.args.get("id"))

    page = request.args.get('page', 1, type=int)

    users = User.query.paginate(page=page, per_page=datosConfig["cantidad"])

    datos = ast.literal_eval(request.args.get("datos")) if request.args.get("datos") else " "


    return render_template("denunciaSeguimiento/new.html", users=users, denuncias=denuncias, usr=user, datos=datos, datosConfig=datosConfig)

def create():
     user = authenticated(session)
    
     if not authenticated(session):

        abort(401)
 
     datosConfig = datosDeConfiguracion()  
     denuncias= Denuncia.findById(request.form.get("id"))
     
     
     seguimiento =Denuncia_seguimiento.crear(
        request.form.get("descripcion"),
        request.form.get("autor")
     )
     
     Denuncia.asignarSeguimiento(seguimiento.id, denuncias.id)
    


#        return render_template("denuncia/revision.html", denuncias=denuncias, usr=user, datosConfig=datosDeConfiguracion())
    # return redirect(url_for("seguimiento_list"))
     return render_template("denunciaSeguimiento/index.html", denuncias=denuncias, datosConfig=datosConfig)