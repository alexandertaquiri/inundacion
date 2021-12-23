from app.db import db
from flask import redirect, render_template, request, url_for, abort, session
from app.models.configuracion import Configuracion
from app.models.criterio import Criterio_ord

#importado para los permisos
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.auth import authenticated_con_permisos


import json


#Devuelve diccionario con la configuracion activa           
def datosDeConfiguracion():
   
   #lo hace la primera vez que cuando la BD esta vacia
   criterio = Criterio_ord.all()
   if criterio == []:
      lista_criterios = ['Alfabetico ascendente', 'Alfabetico descendente', 'Estado activo', 'Estado inactivo']
      for c in lista_criterios:
         Criterio_ord.create(c)
   
   #Traigo la configuracion activa
   configuracionActiva = Configuracion.activo()
   
   #la primera vez que se ejecuta la aplicacion crea la fila en la tabla de datos
   if configuracionActiva == None:
      Configuracion.create('Por defecto', 5, '#96989A,#000000,#000000','#96989A,#000000,#000000', 1, Criterio_ord.devolverCriterioConNombre(lista_criterios[0]).id)
      configuracionActiva = Configuracion.activo()
         
   #reordeno en variables para mas claridad de codigo
   nombreConf = configuracionActiva.nombre 
   lista_colores_publicos = configuracionActiva.coloresPublico.split(",")
   lista_colores_privado = configuracionActiva.coloresPrivado.split(",")
   cantidadPaginacion = configuracionActiva.elementoPorPagina
   criterio = (Criterio_ord.devolverCriterio(configuracionActiva.criterio_id)).nombre
    
    
   #creo el diccionario
   datosConfig = {}
   datosConfig["nombre"] = nombreConf 
   datosConfig["cantidad"] = cantidadPaginacion
   datosConfig["coloresPublicos"] = lista_colores_publicos
   datosConfig["coloresPrivados"] = lista_colores_privado
   datosConfig["criterioOrdenacion"] = criterio
   #retorno el diccionario
   return datosConfig


#Principal de configuracion
def index():
   
   #chequeando logueo y permisos
   user = authenticated_con_permisos(session, "configuracion")
   if user == None:
      abort(401)
   
   #configuracion activa
   config = Configuracion.activo()

   #configuracion por defecto
   config_defecto = Configuracion.por_defecto()
   
   #criterios de ordenacion
   criterios = Criterio_ord.all()
   
   datosConfig = datosDeConfiguracion()
   
   return render_template("configuracion/configuracion.html",
                          title="Menú de configuración", 
                          criterios=criterios,
                          user=user,
                          datosConfig=datosConfig
                          )

def modificar():

   #chequeando logueo y permisos
   user = authenticated_con_permisos(session, "configuracion")
   if user == None:
      abort(401)

   
   #obtengo parametros
   datos_form =request.form
   
   #actualiza el estado del viejo activo
   activ = Configuracion.activo()
   activ.estado = 0
         
   #datos para nueva configuracion  
   cadena_pub = ""
   cadena_priv = ""
 
   cadena_pub = cadena_pub + datos_form["colores_pub1"] + "," + datos_form["colores_pub2"] + "," + datos_form["colores_pub3"] 
   cadena_priv = cadena_priv + datos_form["colores_priv1"] + "," + datos_form["colores_priv2"] + "," + datos_form["colores_priv3"]
   
   nom = datos_form["nombre"]   
   cantidad = datos_form["cant_element"]
   nuevo_estado = 1
   criterio_de_ordenacion = datos_form["criterio_elegido"]

   conf_obj = Configuracion(nom, cantidad, cadena_pub, cadena_priv, nuevo_estado, criterio_de_ordenacion) 
   
   #obtengo configuracion anterior
   anterior = Configuracion.conf_anterior()

   #commit a la BD de la nueva configuracion activada y el nuevo objeto
   db.session.add(conf_obj)
   db.session.add(activ) 
   db.session.commit()
   
   #si existe una anterior la elimina (la 1era vez no existe)
   if anterior != None:
      db.session.delete(anterior)
      db.session.commit()
      
   return redirect(url_for("configuracion_index"))
   
   
def index_defecto():
   
    #chequeando logueo y permisos
   user = authenticated_con_permisos(session, "configuracion")
   if user == None:
      abort(401)


   #obtengo configuracion anterior
   anterior = Configuracion.conf_anterior()
   #desactivo configuracion
   anterior.estado = 0
   #actualizo
   db.session.add(anterior)
   db.session.commit()
       
   #configuracion por defecto
   config_defecto = Configuracion.por_defecto()
   #activo la conf por defecto
   config_defecto.estado = 1
   #actualizo 
   db.session.add(config_defecto)
   db.session.commit()
   
   return redirect(url_for("configuracion_index"))

