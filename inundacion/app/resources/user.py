from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.models.configuracion import Configuracion
from app.resources.configuracion import datosDeConfiguracion
from app.models.criterio import Criterio_ord
from app.helpers.auth import authenticated_con_permisos
from app.helpers.auth import authenticated
from sqlalchemy import desc, asc
 
import ast


def index():
    user = authenticated_con_permisos(session, "user_show")
    if user == None:
        abort(401)
            
    datosConfig = datosDeConfiguracion()
    
    page = request.args.get('page', 1, type=int)

    users = User.query.paginate(page=page, per_page=datosConfig["cantidad"])

    return render_template('user/index.html', users=users, usr=user, datosConfig=datosConfig)        


def byNombre():
    user = authenticated_con_permisos(session, "user_show")
    if user == None:
        abort(401)

    datosConfig = datosDeConfiguracion()

    username = request.args.get("byNombre")


    page = request.args.get('page', 1, type=int)
    # users = User.query.filter_by(username = username).paginate(page=page, per_page=datosConfig["cantidad"])
    users = User.query.filter(User.username.like('%'+username+'%')).paginate(page=page, per_page=datosConfig["cantidad"])
    return render_template('user/index.html', users=users, usr=user, datosConfig=datosConfig)


def estado():
    user = authenticated_con_permisos(session, "user_show")
    if user == None:
        abort(401)

    datosConfig = datosDeConfiguracion()

    estado = request.form.get("select")
    page = request.args.get('page', 1, type=int)
    if (estado != "Todos"):
        users = User.query.filter_by(activo = estado).paginate(page=page, per_page=datosConfig["cantidad"])
    else: 
        users = User.query.paginate(page=page, per_page=datosConfig["cantidad"])  
    return render_template('user/index.html', users=users, usr=user, datosConfig=datosConfig)


def new():  
    # user = authenticated_con_permisos(session, "user_new")
    # if user == None:
    #     abort(401)
    

    roles=Rol.getAll()
    errores = ast.literal_eval(request.args.get("errores")) if request.args.get("errores") else " "
    datos = ast.literal_eval(request.args.get("datos")) if request.args.get("datos") else " "
    return render_template("user/new.html", roles=roles, errores=errores, datos=datos, datosConfig=datosDeConfiguracion())


#creo un usuario, validando que no exista en la base de datos.
#con el email y/o nombre de usuario
def create():
    user = authenticated_con_permisos(session, "user_create")
    if user == None:
        abort(401)

    roles=Rol.getAll()

    errores = User.exist(request.form.get("username"), request.form.get("email"))
    datos = request.form.to_dict()
    
    if errores:
        db.session.rollback()
        return redirect(url_for("user_new", roles=roles, errores=errores, datos=datos, datosConfig=datosDeConfiguracion()))

    errores = User.validar(request.form)

    if errores:
        db.session.rollback()
        return redirect(url_for("user_new", roles=roles, errores=errores, datos=datos, datosConfig=datosDeConfiguracion()))
    
    User.crear(
        request.form.get("first_name"),
        request.form.get("last_name"),
        request.form.get("username"), 
        request.form.get("password"),
        request.form.get("estado"),
        request.form.get("email")
    ) 
    
    for rol in request.form.getlist("list_checkbox"):  
        User.asignarRol(rol, request.form.get("email"))
    return redirect(url_for("user_list")) 

 
def modificar():
    user = authenticated_con_permisos(session, "user_update")
    if user == None:
        abort(401)

    errores = ast.literal_eval(request.args.get("errores")) if request.args.get("errores") else " "
    users= User.findById(request.args.get('id'))
    confirmacionPassword = users.password
    roles = Rol.getAll()
    return render_template("user/edit.html", users=users, roles=roles, errores=errores, confirmacionPassword=confirmacionPassword, usr=user,  datosConfig=datosDeConfiguracion())  

def modificar_confirm():
    user = authenticated_con_permisos(session, "user_update")
    if user == None:
        abort(401)

    roles=Rol.getAll()
    errores = {}
    diccionario = {}
    
    id = request.form.get("idModificar")
    diccionario["id"] = id
    usuario = User.query.filter_by(id = id).first()
    diccionario["activo"] = usuario.activo
    diccionario["roles"] = usuario.roles
    
    first_name = request.form.get("first_name")
    if usuario.first_name != first_name:
        diccionario["first_name"] = first_name
        errorFirstName = User.validarString(first_name)
        if not errorFirstName:
            errores["error_nombreCompleto"] = "El nombre es incorrecto"
        else:
            usuario.first_name = first_name
    else:
        diccionario["first_name"] = usuario.first_name


    last_name = request.form.get("last_name")
    if usuario.last_name != last_name:
        diccionario["last_name"] = last_name
        errorLastName = User.validarString(last_name)
        if not errorLastName:
            errores["error_nombreCompleto"] = "El nombre es incorrecto"
        else:
            usuario.last_name = last_name
    else:
        diccionario["last_name"] = usuario.last_name


    username = request.form.get("username")
    if usuario.username != username:
        diccionario["username"] = username
        if not User.existUsername(username):
            errorUsername = User.validarString(username)
            if not errorUsername:
                errores["error_username"] = "El nombre de usuario es incorrecto"
            else:
                usuario.username = username
        else:
            errores["error_username"] = "El nombre de usuario ya existe"
    else:
        diccionario["username"] = usuario.username


    email = request.form.get("email")
    if usuario.email != email:
        diccionario["email"] = email
        if not User.existEmail(email):
            if not User.validarEmail(email):
                errores["error_email"] = "El email es incorrecto"
            else:
                usuario.email = email
        else:
            errores["error_email"] = "El email ya existe en otro usuario"
    else:
        diccionario["email"] = usuario.email


    password = request.form.get("password")
    confirmacionPassword = request.form.get("confirmacionPassword")
    diccionario["password"] = password
    if (password != (confirmacionPassword)):
        errores["error_password"] = "Las contraseñas ingresadas no coinciden"
    else:
        usuario.password = password


    if len(request.form.getlist("lista_eliminar")) == len(usuario.roles):
        if len(request.form.getlist("lista_agregar")) == 0:
            errores["error_roles"] = "El usuario debe tener un rol como mínimo"


    if errores:
        db.session.rollback()
        return render_template("user/edit.html", users=diccionario, roles=roles, errores=errores, confirmacionPassword=confirmacionPassword, usr=user, datosConfig=datosDeConfiguracion())
    else:
        db.session.commit()
        #obtengo parametros    
        lista_roles_eliminar = request.form.getlist("lista_eliminar")
        lista_roles_agregar = request.form.getlist("lista_agregar")
    
        #agregando 
        if len(lista_roles_agregar) > 0:
            for r in lista_roles_agregar:
                User.asignarRol(r, usuario.email)
    
        lista_roles_actuales = usuario.roles.copy()
    
        #eliminando y volviendo a cargar los anteriores
        if len(lista_roles_eliminar) > 0:
            usuario.roles = []
            db.session.commit()
    
            for rolBackup in lista_roles_actuales:
                if rolBackup.nombre not in lista_roles_eliminar:
                    User.asignarRol(rolBackup.nombre, usuario.email)
        
        return redirect(url_for("user_list"))


def perfil():
    # user = authenticated_con_permisos(session, "user_show")
    email = authenticated(session)
    user = User.findByEmail(email)
    return render_template("user/perfil.html", users=user, datosConfig=datosDeConfiguracion())


def delete():
    user = authenticated_con_permisos(session, "user_destroy")
    if user == None:
        abort(401)

    idBorrar = request.form.get("idBorrar")
    user = User.query.get(idBorrar)
    User.delete(user)
    
    return redirect(url_for("user_list"))

    
def activar_desactivar():

    #chequeando logueo y permisos
    user = authenticated_con_permisos(session, "user_update")
    if user == None:
        abort(401)

    #realizando consulta para que devuelva los usuarios
    usr = User.findById(request.args.get('id'))
    
    if usr.activo == 0:
        usr.activo = 1
    else:    
        usr.activo = 0
    
    #actualizo base de datos     
    db.session.commit()
    
    return redirect(url_for("user_list"))
    #return render_template("configuracion/pruebaConf.html", usr=usr, email=datos_form)

def create_google():
    datos = request.form.to_dict()
    
    # if errores:
    #     db.session.rollback()
    #     return redirect(url_for("user_new", roles=roles, errores=errores, datos=datos, datosConfig=datosDeConfiguracion()))

    # errores = User.validar(request.form)

    # if errores:
    #     db.session.rollback()
    #     return redirect(url_for("user_new", roles=roles, errores=errores, datos=datos, datosConfig=datosDeConfiguracion()))
    
    errores = User.exist(request.form.get("username"), request.form.get("email"))
    if errores:
        db.session.rollback()
        return render_template("auth_google/registrar.html", first_name=request.form.get("first_name"), last_name=request.form.get("last_name"), users_email=request.form.get("email"), username=request.form.get("username"), errores=errores, datosConfig = datosDeConfiguracion())
    
    errores = User.validar_registro_google(request.form)    
    if errores:
        db.session.rollback()
        return render_template("auth_google/registrar.html", first_name=request.form.get("first_name"), last_name=request.form.get("last_name"), users_email=request.form.get("email"), username=request.form.get("username"), errores=errores, datosConfig = datosDeConfiguracion())

        
    User.crear(
        request.form.get("first_name"),
        request.form.get("last_name"),
        request.form.get("username"), 
        request.form.get("password"),
        request.form.get("estado"),
        request.form.get("email")
    )
     
    flash("Carga exitosa")
    return redirect(url_for("home"))  