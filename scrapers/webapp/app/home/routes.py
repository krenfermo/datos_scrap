# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from conexion import conexion2
import requests
import unicodedata
from flask import  request, jsonify, make_response
#from config import app
from app import functions
import json
from datetime import date
from app.base.forms import CategoriaForm
from app.base.models import Categorias
from app import db

 
from . import nocache
 
 
    
@blueprint.route("/links_rotos/delete/<id>", endpoint="delete_rotos", methods=["DELETE"])
def route_borra_rotos(id):    
    #if  current_user.is_authenticated:
        #print( "delete from enlaces_rotos where id="+str(id) ) 
        delete=functions.f_delete_rotos(id)
        return jsonify('URL borrado correcto'), 201

    
@blueprint.route("/precios/", endpoint="precios", methods=["POST"])
@nocache.nocache
def route_precios():    
    #if  current_user.is_authenticated:
        codigo=request.form['codigo'] 
        precios=functions.f_precios(codigo)
        registros=int(len(precios['precios']))
         
        return render_template( "precios.html",info=precios['precios'],registros=registros )


@blueprint.route("/precios_cambiados/", endpoint="precios_cambiados", methods=["POST"])
@nocache.nocache
def route_precios_cambiados():    
    #if  current_user.is_authenticated:
        codigo=request.form['codigo'] 
        precios=functions.f_precios_cambiados(codigo)
        registros=int(len(precios['precios']))
         
        return render_template( "precios_cambiados.html",info=precios['precios'],registros=registros )

    




@blueprint.route('/index')
@login_required
def index():
    
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    return render_template('index.html')


@blueprint.route('/colombia')
@login_required
def colombia():
    
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))
    
    return render_template('colombia.html',fecha=date.today())


@blueprint.route('/categorias', methods=['GET', 'POST'])
@login_required
def categorias():
    catego_form = CategoriaForm(request.form)
    
    
    if 'nombre' in request.form :
        
        nombre  = request.form['nombre']
        catego = Categorias.query.filter_by(nombre=nombre).first()
        
        if catego:
            return render_template( 'categorias.html', nombre=nombre,msg_error='Categoría existe¡¡',form=catego_form)
        catego = Categorias(nombre)
 
        db.session.add(catego)
        db.session.commit()
        return render_template( 'categorias.html',nombre=nombre, msg='Categoría creada¡¡',form=catego_form)
    return render_template( 'categorias.html',form=catego_form)

        
    


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:
        print(requests)
 
        if template=='tables.html':
            #info = requests.get('http://localhost:5000/links_rotos/')
            #info = unicodedata.normalize('NFKD', info).encode('ascii','ignore')
            
            #info = json.loads(info)
            #cur = conexion.miConexion.cursor() 
            
            conn=conexion2.Conexion()
            
            cur = conn.conn.cursor()   
            cur.execute( "select * from enlaces_rotos;" ) 
            
            rotos=cur.fetchall()
            
            conn.conn.close()
         
            info= {"rotos": [{"id": x[0], "url": x[1], "fecha_encontrado": x[2], "bodega": x[3]} for x in rotos]}
      
            #print(info['rotos'])
            registros=int(len(info['rotos']))
            return render_template( template,info=info['rotos'],registros=registros )  
        
        
        if template=='precios.html':
            #info = requests.get('http://localhost:5000/links_rotos/')
            #info = unicodedata.normalize('NFKD', info).encode('ascii','ignore')
            
            #info = json.loads(info)
            
          
            #print(info['rotos'])
            
            return render_template( template  )   
        
        if template=='precios_cambiados.html':

            conn=conexion2.Conexion()
            
            cur = conn.conn.cursor()   
            cur.execute( "select * from precios_cambiados;" ) 
            
            rotos=cur.fetchall()
            
            conn.conn.close()
         
         
            info= {"precios_cambiados": [{"id": x[0], "precio": x[1], "fecha_actualizacion": x[2], "bodega": x[3], "codigo": x[4], "codigo_prov": x[5], "costo": x[6], "precio_prov": x[7]} for x in rotos]}
      
            print(info['precios_cambiados'])
            registros=int(len(info['precios_cambiados']))
            return render_template( template,info=info['precios_cambiados'],registros=registros )  
        
            
        if not template.endswith( '.html' ):
            template += '.html'

        return render_template( template)    

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except Exception as err:
        #return render_template('page-500.html'), 500
        print(err)
        pass
