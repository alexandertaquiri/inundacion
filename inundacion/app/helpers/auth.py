from flask import redirect, render_template, request, url_for, abort, session
from app.models.user import User



def authenticated(session):
    return session.get("user")

def authenticated_con_permisos(session, nom_permiso):
   #chequeo Logueo
   user = authenticated(session)
   if user == None:
       return None
   
   #chequeo permisos
   user_query = User.findByEmail(user)
   ok_p = User.tiene_permiso(user_query, nom_permiso)   
   if not(ok_p):
      return None
   #llega aqui si tiene permisos y retorna la fila del usuario
   return user_query 
