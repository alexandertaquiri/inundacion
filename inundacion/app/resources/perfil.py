from app.db import db

from flask import redirect, render_template, request, url_for, session, abort
from app.models.user import User
from app.helpers.auth import authenticated

# Protected resources

def perfil():
    
    if not authenticated(session):
        abort(401)

    return render_template("user/perfil.html")


