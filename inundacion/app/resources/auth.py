from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User


def login():

    # return render_template("home")
    return render_template("auth/login.html")



def authenticate():
#------------ Lo antiguo --------------------    
#    conn = connection()
#    params = request.form
#    user = User.find_by_email_and_pass(conn, params["email"], params["password"])
#-------------------------------------------

    #trae parametros del formulario
    params = request.form
    
    #haciendo una especie de where entre lo sacado del formulario y la base 
    #(esto podria mejorarse y hacerse en el modelo obteniendolo de una clase pasando los parametros... por ejemplo user= AuthenticateUser.run(params))
    user = User.query.filter(User.email == params["email"]).filter(User.password == params ["password"]).first() #se queda con la 1er tupla que cumple
    
    if not user:
        flash("Usuario o clave incorrecto.")
        #return redirect(url_for("auth_login"))
        #return redirect(url_for("home"))
    elif (user.activo == 1):
        session["user"] = user.email #guarda en la sesion el contexto
        flash("La sesión se inició correctamente.")
    else:
        flash("No puede iniciar sesion porque aun se encuentra inactivo. Aguarde a ser activado o contactese con el Administrador")            
    
    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    #return redirect(url_for("auth_login"))
    return redirect(url_for("home"))
