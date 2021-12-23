from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.configuracion import Configuracion
from app.models.denuncia_categoria import DenunciaCategoria
from app.resources.configuracion import datosDeConfiguracion
from app.models.criterio import Criterio_ord
from app.helpers.auth import authenticated_con_permisos
from app.helpers.auth import authenticated
from app.models.denuncia import Denuncia 
from sqlalchemy import desc, asc
from datetime import date, timedelta

from sqlalchemy.orm import query
 
import ast

def new():
    user = authenticated(session)
    if not authenticated(session):
        abort(401)

    datosConfig = datosDeConfiguracion()

    categorias= DenunciaCategoria.get_by_id(request.args.get("id"))

    page = request.args.get('page', 1, type=int)

    datos = ast.literal_eval(request.args.get("datos")) if request.args.get("datos") else " "

    return render_template("denuncia/new.html", categorias=categorias, usr=user, datos=datos, datosConfig=datosConfig)

def create():
    user = authenticated(session)
    
    if not authenticated(session):

        abort(401)
 
    #creamos la denuncia
    DenunciaCategoria.crear(
        request.form.get("nombre")
         ) 

    return redirect(url_for("denuncia_list"))
     
    



