from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import DATETIME, Date
from app.db import db
from sqlalchemy import update
from app.models.rol import Rol
from flask import session
from datetime import date
from sqlalchemy import and_
import datetime
import re
import json


roles = db.Table('usuario_tiene_rol',
              Column('users_id', Integer, ForeignKey('users.id'), primary_key=True),
              Column('rol_id', Integer,  ForeignKey('rol.id'), primary_key=True )
            )

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(30), unique=True)
    password = Column(String(30))
    activo = Column(Integer)
    username = Column(String(30), unique=True)
    update_at = Column(DATETIME, nullable=True)
    create_at = Column(DATETIME,default=datetime.datetime.utcnow)
    roles = relationship('Rol', secondary=roles, backref= backref(
        'usuarios_con_el_rol', lazy=True), lazy='subquery')
       
    #Constructor
    def __init__(self, first_name=None, last_name=None, username=None, password=None, activo=None, email=None, update_at=None, create_at=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.activo = activo
        self.email = email
        self.update_at = update_at
        self.create_at = create_at

    def findByEmail(email):
        return User.query.filter_by(email = email).first() 

    def get_roles(use_id):
        return roles.query.filter_by(user_id = use_id) 

    def findById(use_id):
        return User.query.filter_by(id = use_id).first()

    def asignarRol(nombre, email):
        user = User.findByEmail(email)
        rol = Rol.get_by_nombre(nombre)
        user.roles.append(rol)
        db.session.commit()
                      
    def getIdUser(user_id):
        return User.query.get(user_id)

    def getAll():
        users = User.query.all()
        return users 
           
    def esAdministrador(user):
        res = false
        for rol in user.roles:
            if rol.id == 1:
                res = True
        return res  

    def tiene_rol(user, nombre_rol):
        res = False
        for rol in user.roles:
            if rol.nombre == nombre_rol:
                res = True
        return res        

    def tiene_permiso(user, nombre_permiso):
        res = False
        for rol in user.roles:
            for permiso in rol.permisos:
                if permiso.nombre == nombre_permiso:
                    res = True
        return res    

    def existUsername(username):
        elemento = User.query.filter_by(username = username).first()
        if elemento is not None:
            return True
        return False

    def existEmail(email):
        elemento = User.query.filter_by(email = email).first()
        if elemento is not None:
            return True
        return False

    def exist(username, email):
        errores = {}

        username_result = User.query.filter_by(username = username).first()
        email_result = User.findByEmail(email)

        if ( (username_result is not None ) ):
            errores["error_username"] = "El nombre de usuario ya existe"  

        if ( (email_result is not None ) ):
            errores["error_email"] = "El email ya existe"

        return errores 

    

    def validarStringNombre(nombre):
        ok = True
        validador_string = r"^[a-zA-Záéíóú ]+$"
        if ( ( not re.match(validador_string, nombre) ) | (not 3 <= len(nombre) <= 30) ) :
            ok = False
        return ok 

    def validarString(nombre):
        ok = True
        if not 3 <= len(nombre) <= 30:
            ok = False
        return ok     

    def validarEmail(email):
        validador_email = r"^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+([.]\w{2,4})+$"
        if not re.match(validador_email, email):
            return False
        return True

    def validar(form):
        errores = {}

        if not (User.validarStringNombre(form.get("first_name"))):
            errores["error_nombreCompleto"] = "El nombre es incorrecto"

        if not (User.validarStringNombre(form.get("last_name"))):
            errores["error_nombreCompleto"] = "El nombre es incorrecto"

        if not (User.validarString(form.get("username"))):
            errores["error_username"] = "El nombre de usuario es incorrecto"

        email = form.get("email")
        if not User.validarEmail(email):
            errores["error_email"] = "El email es incorrecto"
        
        if (form.get("password") != (form.get("confirmacionPassword"))):
            errores["error_password"] = "Las contraseñas ingresadas no coinciden"

        if len(form.getlist("list_checkbox")) == 0:
            errores["error_roles"] = "Se debe seleccionar un rol como mínimo"
        
        return errores    


    def validar_registro_google(form):
        errores = {}

        if not (User.validarStringNombre(form.get("first_name").strip())):
            errores["error_nombreCompleto"] = "El nombre es incorrecto"

        if not (User.validarStringNombre(form.get("last_name").strip())):
            errores["error_nombreCompleto"] = "El nombre es incorrecto"

        if not (User.validarString(form.get("username").strip())):
            errores["error_username"] = "El nombre de usuario es incorrecto"

        # email = form.get("email")
        # if not User.validarEmail(email):
        #     errores["error_email"] = "El email es incorrecto"
        
        if (form.get("password").strip() != (form.get("confirmacionPassword").strip())):
            errores["error_password"] = "Las contraseñas ingresadas no coinciden"
        elif not (User.validarString(form.get("password").strip())):
            errores["error_password"] = "Ingrese contraseña válida"

        # if len(form.getlist("list_checkbox")) == 0:
        #     errores["error_roles"] = "Se debe seleccionar un rol como mínimo"
        
        return errores      



    ########################CREAR USUARIO#####################################    

    def crear(first_name, last_name, username, password, activo, email):
        user=User(first_name=first_name, last_name=last_name, username=username, password=password, activo=activo, email=email, update_at=date.today().strftime('%Y-%m-%d %H:%M:%S'), create_at=date.today().strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(user)
        db.session.commit()    


    def delete(user):
        db.session.delete(user)
        db.session.commit()  

    @staticmethod
    def new_usuario_from_api(user):
        fecha=date.today()
        fecha2=date.today()
        user.update_at=fecha
        user.create_at=fecha2
        db.session.add(user)
        db.session.commit()

   
    


    def as_dict(self):
        return{ "first_name" :self.first_name,
        "last_name" :self.last_name,
        "username" :self.username,
        "password" : self.password,
        "activo" : self.activo,
        "email" :self.email,
        "update_at" : self.update_at,
        "create_at" :self.create_at
  }

             

