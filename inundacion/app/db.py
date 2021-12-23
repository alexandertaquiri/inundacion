#configurando base con SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

#instancio
db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    config_db(app)
    

#funcion para configurar base de datos
def config_db(app):
    @app.before_first_request
    def init_database():
        db.create_all() 
    
    #para limpiar la sesion. Es buena practica
    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()   
