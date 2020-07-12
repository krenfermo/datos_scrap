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
from app.base.forms import CategoriaForm,TecnologiaForm
from app.base.models import Categorias,Tecnologias
from app import db

 
from . import nocache
 
 
    
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
    categorias = Categorias.query.order_by(Categorias.nombre.asc()).all()
    
    if 'nombre' in request.form :
        
        nombre  = request.form['nombre']
        nombre=nombre.upper()
        catego = Categorias.query.filter_by(nombre=nombre).first()
        
        if catego:
            return render_template( 'categorias.html', nombre=nombre,msg_error='Categoría existe¡¡',form=catego_form, categorias=categorias)
        
        catego = Categorias(nombre)
 
        db.session.add(catego)
        db.session.commit()
        categorias = Categorias.query.order_by(Categorias.nombre.asc()).all()
        return render_template( 'categorias.html',nombre=nombre, msg='Categoría creada¡¡',form=catego_form, categorias=categorias)
        
        

    return render_template( 'categorias.html',form=catego_form, categorias=categorias)

        
    
@blueprint.route("/categorias/delete/<nombre>", endpoint="delete_rotos", methods=["DELETE"])
def route_borra_catego(nombre):    
    #if  current_user.is_authenticated:
        #print( "delete from enlaces_rotos where id="+str(id) ) 

        catego = Categorias.query.filter_by(nombre=nombre).first()
        db.session.delete(catego)
        db.session.commit()
        return jsonify('URL borrado correcto'), 201

    

@blueprint.route('/tecnologias', methods=['GET', 'POST'])
@login_required
def tecnologias():
    tecno_form = TecnologiaForm(request.form)
    
    if 'nombre' in request.form :
        
        nombre  = request.form['nombre']
        categoria_id  = request.form['categoria']
        nombre=nombre.upper()
        catego = Categorias.query.filter_by(id=categoria_id).first()
        if catego is None:
            return render_template( 'tecnologias.html',msg_error='Selecciona Categoria¡¡',form=tecno_form)
        tecno = Tecnologias.query.filter_by(nombre=nombre).filter_by(catego_id=categoria_id).first()
        
        print("pasa")
        if tecno:
            return render_template( 'tecnologias.html', nombre=nombre,categoria=catego,msg_error='Tecnología existe ',form=tecno_form, tecno=tecno)
        print(catego)
        tecno = Tecnologias(nombre,categoria_id)
        print("va guardar")
        db.session.add(tecno)
        db.session.commit()
        
        return render_template( 'tecnologias.html',nombre=nombre, msg='Categoría creada¡¡',form=tecno_form)
        
        

    return render_template( 'tecnologias.html',form=tecno_form)


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
