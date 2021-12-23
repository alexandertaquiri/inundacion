from flask import redirect, render_template, request, url_for, abort, session, flash, Flask
#from app.db import connection
from app.models.user import User
from app.resources.configuracion import datosDeConfiguracion
from os import environ

import requests
from oauthlib.oauth2 import WebApplicationClient

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import json

# Google Configuration
GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
#OAUTHLIB_INSECURE_TRANSPORT = environ.get("OAUTHLIB_INSECURE_TRANSPORT", None) 

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
        
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://127.0.0.1:5000/login/callback",
        scope=["openid", "email", "profile"],
    )
    
   # url_for('request_uri', _external=True, _scheme='https', viewarg1=1)
    
    
    
    print("llega al redirect")
    return redirect(request_uri)

# @app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        first_name = userinfo_response.json()["given_name"]
        last_name = userinfo_response.json()["family_name"]
        users_email = userinfo_response.json()["email"]
        #unique_id = userinfo_response.json()["sub"]
        #picture = userinfo_response.json()["picture"]
    else:
        return "User email not available or not verified by Google.", 400
        
    # Create a user in your db with the information provided
    # by Google
    # user = User(
    #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    # )

    # Doesn't exist? Add it to the database.
    errores = {}
    username = " "
    print (userinfo_response.json())
    if not User.existEmail(users_email):
#       User.crear(first_name, last_name,"","", 0, users_email)
        return render_template("auth_google/registrar.html", first_name=first_name, last_name=last_name, users_email=users_email, username=username, errores=errores, datosConfig = datosDeConfiguracion())
    else:
        # Send user back to homepage
        user = User.findByEmail(users_email)
        if user.activo == 1:
            session["user"] = user.email #guarda en la sesion el contexto
            flash("La sesión se inició correctamente.")
        else:
            flash("No puede iniciar sesión porque aún se encuentra inactivo. Aguarde a ser activado o contáctese con el Administrador")            
        return redirect(url_for("home"))
 
    # Begin user session by logging the user in
    # login_user(user)

    


def bienvenido():
    return render_template("auth_google/bienvenido.html")


# def authenticate():
#     conn = connection()
#     params = request.form

#     user = User.find_by_email_and_pass(conn, params["email"], params["password"])

#     if not user:
#         flash("Usuario o clave incorrecto.")
#         return redirect(url_for("auth_login"))

#     session["user"] = user["email"]
#     flash("La sesión se inició correctamente.")

#     return redirect(url_for("home"))


# def logout():
#     logout_user()
#     return redirect(url_for("index"))