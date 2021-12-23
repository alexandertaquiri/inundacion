from os import path, environ, urandom
from flask import Flask, render_template, g, Blueprint, make_response, request, session
from oauthlib import oauth2
from flask_session import Session
from config import config
from app import db
# from app.resources import denuncia, user
from app.resources import denuncia
from app.resources import user
from app.resources import auth

from app.resources import puntosEncuentro
from app.resources import recorridosEvacuacion
from app.resources import configuracion
from app.resources import zona_inundable
from app.resources import denunciaSeguimiento
from app.resources.api.denuncias import denuncia_api 
from app.resources.api.categorias import categoria_api 
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.resources.api import denuncias 
from app.resources.api import zonas_inundables
from flask_cors import CORS
from app.resources.api.user import user_api
from app.resources.api import recorridos_evacuacion
from app.resources.api import puntos_encuentro
from app.resources.api import configuracion_api
from app.resources import auth_google


#para debugear consultas a la base de datos en terminal
#import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# #---------




def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    
    
    
    



    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    # Carga de la configuración
    cors = CORS(app,resources={r"/*":{"origins":"*"}})
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    #app.config["SESSION_TYPE"] = "filesystem"
    #Session(app)

    # Configure db
    db.init_app(app)

    
    

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    # app.add_url_rule("/iniciar_sesion", "auth_home", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )
    
    #Autenticacion Google
    app.add_url_rule("/iniciar_sesion_google", "auth_login_google", auth_google.login)
    app.add_url_rule(
        "/login/callback", "auth_callback", auth_google.callback, methods=["GET"]
    )
    
    # Rutas de Puntos de encuentro
    app.add_url_rule("/puntosEncuentro/index", "puntosEncuentro_list", puntosEncuentro.list, methods=["POST", "GET"])
    app.add_url_rule("/puntosEncuentro/create", "puntosEncuentro_create", puntosEncuentro.create, methods=["POST", "GET"])
    app.add_url_rule("/puntosEncuentro/nuevo", "puntosEncuentro_new", puntosEncuentro.new)
    app.add_url_rule("/puntosEncuentro/delete", "puntosEncuentro_delete", puntosEncuentro.delete, methods=["POST", "GET"])
    app.add_url_rule("/puntosEncuentro/viewModify", "puntosEncuentro_viewModify", puntosEncuentro.viewModify, methods=["POST", "GET"])
    app.add_url_rule("/puntosEncuentro/modify", "puntosEncuentro_modify", puntosEncuentro.modify, methods=["POST", "GET"])
    app.add_url_rule("/puntosEncuentro/byNombre", "puntosEncuentro_byNombre", puntosEncuentro.byNombre, methods=["POST", "GET"])
    app.add_url_rule("/puntosEncuentro/estado", "puntosEncuentro_estado", puntosEncuentro.estado, methods=["POST", "GET"])


    # Rutas de denuncias

    #app.add_url_rule("/denuncias", "denuncia_create", denuncia.create, methods=["POST"])
    #app.add_url_rule("/denuncias", "denuncia_nueva", denuncia.nueva)
    app.add_url_rule("/denuncias/index", "denuncia_list", denuncia.index, methods=["POST", "GET"])
    app.add_url_rule("/denuncias/new", "denuncia_new", denuncia.new, methods=["POST", "GET"])
    app.add_url_rule("/denuncias", "denuncia_create", denuncia.create, methods=["POST"])
    app.add_url_rule("/denuncias/viewModify", "denuncia_viewModify", denuncia.viewModify, methods=["POST", "GET"]) 
    app.add_url_rule("/denuncias/modify", "denuncia_modify", denuncia.modify, methods=["POST", "GET"])
    app.add_url_rule("/denuncias", "denuncia_create", denuncia.create, methods=["POST"]) 
    app.add_url_rule("/denuncias/byTitulo", "denuncia_byTitulo", denuncia.byTitulo, methods=["POST", "GET"])
    app.add_url_rule("/denuncias/estado", "denuncia_estado", denuncia.estado, methods=["POST", "GET"])
    app.add_url_rule("/denuncias/filtrarPorFecha", "denuncia_filtrarPorFecha", denuncia.filtrarPorFecha, methods=["POST", "GET"])
    app.add_url_rule("/denuncias/delete", "denuncia_delete", denuncia.delete, methods=["POST", "GET"])
    app.add_url_rule("/denuncias/revision", "denuncia_revision", denuncia.revision, methods=["POST", "GET"])
    app.add_url_rule("/denuncias/incrementarIntentos", "denuncia_incrementar", denuncia.incrementarIntentos, methods=["POST", "GET"])
    app.add_url_rule("/denuncias/resolver", "denuncia_resolver", denuncia.resolver, methods=["POST", "GET"])

    #Rutas de seguimiento
    app.add_url_rule("/seguimiento/index", "seguimiento_list", denunciaSeguimiento.index, methods=["POST","GET"])
    app.add_url_rule("/seguimiento/new", "seguimiento_new", denunciaSeguimiento.new, methods=["POST","GET"] )
    app.add_url_rule("/seguimiento", "seguimiento_create", denunciaSeguimiento.create, methods=["POST","GET"])

    #Rutas API de recorridos
    app.add_url_rule("/api/recorridos-evacuacion/<int:pagina>", "recorridosAll", recorridos_evacuacion.recorridosAll, methods=["GET"])

    #Rutas API puntos de encuentro
    app.add_url_rule("/api/puntos-encuentro/<int:pagina>", "puntosAll", puntos_encuentro.puntosAll, methods=["GET"])

    # Rutas de Usuarios
    app.add_url_rule("/usuarios/perfil", "user_perfil", user.perfil, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/create", "user_create", user.create, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/modificar", "user_modificar", user.modificar, methods=["POST", "GET"])

    #Usuario creado GOOGLE
    app.add_url_rule("/usuarios/create_google", "user_create_google", user.create_google, methods=["POST", "GET"])


    # Nueva ruta para la confirmacion de modificacion
    app.add_url_rule("/usuarios/modificarConfirm", "user_modificar_confirm", user.modificar_confirm, methods=["POST"])
    app.add_url_rule("/usuarios/index", "user_list", user.index, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/byNombre", "user_byNombre", user.byNombre, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/estado", "user_estado", user.estado, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/delete", "user_delete", user.delete, methods=["POST", "GET"])

    
    
    #ruta para activacion y desactivacion de usuario
    app.add_url_rule("/usuarios/cambiarEstado", "activar_desactivar", user.activar_desactivar, methods=["POST", "GET"])
    
    #Ruta configuracion
    app.add_url_rule("/configuracion", "configuracion_index", configuracion.index)
    app.add_url_rule("/configuracion", "configuracion_modificada", configuracion.modificar, methods=["POST"])    
    app.add_url_rule("/configuracion/defecto", "configuracion_defecto", configuracion.index_defecto)
    
    #Ruta configuracion API
    app.add_url_rule("/api/configuracion-api/", "configuracion_api", configuracion_api.api_configuracion, methods=["GET"])
    

    #Rutas de zona inundable API
    app.add_url_rule("/api/zonas-inundables/<int:idZona>", "zona_api", zonas_inundables.apiZona, methods=["GET"])
    app.add_url_rule("/api/zonas-inundables-all/<int:pagina>", "zona_api_all", zonas_inundables.apiZonaAll, methods=["GET"])
    
    #Ruta de zona inundable
    app.add_url_rule("/zona_inundable", "zona_index", zona_inundable.index, methods=["POST", "GET"])
    app.add_url_rule("/zona_inundable/new", "zona_new", zona_inundable.new, methods=["POST", "GET"])
    app.add_url_rule("/zona_inundable/create", "zona_create", zona_inundable.create, methods=["POST", "GET"])
    app.add_url_rule("/zona_inundable/byNombre", "zona_byNombre", zona_inundable.byNombre, methods=["POST", "GET"])    
    app.add_url_rule("/zona_inundable/estado", "zona_estado", zona_inundable.estado, methods=["POST", "GET"])
    app.add_url_rule("/zona_inundable/delete", "zona_delete", zona_inundable.delete, methods=["POST", "GET"])
    app.add_url_rule("/zona_inundable/visualizar", "zona_visualizar", zona_inundable.visualizar, methods=["POST", "GET"])
    app.add_url_rule("/zona_inundable/modificar", "zona_modificar", zona_inundable.modificar, methods=["POST", "GET"])
    app.add_url_rule("/zona_inundable/modificar_confirm", "zona_modificar_confirm", zona_inundable.modificar_confirm, methods=["POST", "GET"])


    #Rutas Recorridos
    app.add_url_rule("/recorridosEvacuacion/index", "recorridosEvacuacion_list", recorridosEvacuacion.list, methods=["POST", "GET"])
    app.add_url_rule("/recorridosEvacuacion/create", "recorridosEvacuacion_create", recorridosEvacuacion.create, methods=["POST", "GET"])
    app.add_url_rule("/recorridosEvacuacion/nuevo", "recorridosEvacuacion_new", recorridosEvacuacion.new)
    app.add_url_rule("/recorridosEvacuacion/delete", "recorridosEvacuacion_delete", recorridosEvacuacion.delete, methods=["POST", "GET"])
    app.add_url_rule("/recorridosEvacuacion/viewModify", "recorridosEvacuacion_viewModify", recorridosEvacuacion.viewModify, methods=["POST", "GET"])
    app.add_url_rule("/recorridosEvacuacion/byNombre", "recorridosEvacuacion_byNombre", recorridosEvacuacion.byNombre, methods=["POST", "GET"])
    app.add_url_rule("/recorridosEvacuacion/estado", "recorridosEvacuacion_estado", recorridosEvacuacion.estado, methods=["POST", "GET"])
    app.add_url_rule("/recorridosEvacuacion/modify", "recorridosEvacuacion_modify", recorridosEvacuacion.modify, methods=["POST", "GET"])


    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        #return render_template("home.html")
        
        datosConfig = configuracion.datosDeConfiguracion()        
        
        # Ejemplo cookies
        resp = make_response(render_template("home.html", datosConfig=datosConfig))
        # resp = make_response(render_template("auth/home"))
        resp.set_cookie('ejemplo_cookie', 'Hola clase')
        
        visitas = 0
        if request.cookies.get('visitas'):
            visitas = request.cookies.get('visitas')
        resp.set_cookie('visitas', str(int(visitas)+1))
        
        return resp


    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(denuncia_api)
    api.register_blueprint(user_api)
    api.register_blueprint(categoria_api)

    app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    # Rutas de API-REST (usando Blueprints)
    #api = Blueprint("api", __name__, url_prefix="/api")
    
    #app.register_blueprint(api)

    

    return app
