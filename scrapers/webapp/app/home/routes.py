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
from datetime import date,datetime
from app.base.forms import CategoriaForm,TecnologiaForm
from app.base.models import Categorias,Tecnologias
from app import db
from pathlib import Path
 
from . import nocache
 
from os import listdir
from os.path import isfile, isdir
import os,sys
import platform
from os import remove

import importlib.util
import os, time
import platform

def creation_date(path_to_file):

    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

#sys.path.insert(1,'.')
def creation_date(path_to_file):

    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def ls1(path,pais):    
    return [obj.replace(".png","").replace("_"+pais,"") for obj in listdir(path) if isfile(path + obj)and pais in obj]

 
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
    path=Path(__file__).parent.absolute()
    path=str(path).split("/")
    path=path[:-1]
    path="/".join(path)
    
    fotos=ls1(str(path)+"/base/static/","colombia")
    print(fotos)
    item_fotos=list()
    for item in fotos:
        
        fecha_archivo=datetime.fromtimestamp(creation_date(str(path)+"/base/static/"+item+"_colombia.png"))
        fecha_archivo=str(fecha_archivo).split(" ")[0]
        item_fotos.append({"foto":item,"fecha":fecha_archivo})
    
    return render_template('colombia.html',fotos=item_fotos,pais="colombia",nombre="Colombia")


@blueprint.route('/argentina')
@login_required
def argentina():
    
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))
    path=Path(__file__).parent.absolute()
    path=str(path).split("/")
    path=path[:-1]
    path="/".join(path)
    
    fotos=ls1(str(path)+"/base/static/","argentina")
    #print(fotos)
    item_fotos=list()
    for item in fotos:
        
        fecha_archivo=datetime.fromtimestamp(creation_date(str(path)+"/base/static/"+item+"_argentina.png"))
        fecha_archivo=str(fecha_archivo).split(" ")[0]
        item_fotos.append({"foto":item,"fecha":fecha_archivo})
    #item_fotos=set(item_fotos)
    #print(item_fotos)
    return render_template('colombia.html',fotos=item_fotos,pais="argentina",nombre="Argentina")




@blueprint.route('/scrapers', methods=['GET', 'POST'])
@login_required
def scrapers():
    import locale
    locale.setlocale(locale.LC_TIME,'es_CR.UTF-8')
    date_format = locale.nl_langinfo(locale.D_FMT)
    
    result2=""
    path=Path(__file__).parent.absolute()
    path=str(path).replace("webapp/app/home","")
    fecha=os.listdir(str(path)+"DATOS_COMPUTRABAJO/")
    
    leng=len(fecha)
    carpeta=max(fecha)
    d = time.ctime(os.path.getmtime(str(path)+"DATOS_COMPUTRABAJO/"+str(carpeta)))
    
    result2="Actualizados : %s" % d
    
    if 'scrap' in request.form :
        print ("lanza scrapers")
        
        activate_this_file = "app/home/activar_env.py"
        import subprocess

        result2 = subprocess.run(['pwd'], stdout=subprocess.PIPE)
                
        path=result2.stdout.decode('utf-8').replace("/webapp\n","/webapp/")
        #print(path+activate_this_file)
        activar=path+activate_this_file
        #execfile(activate_this_file, dict(__file__=activate_this_file))
        exec(compile(open(activar, "rb").read(), activar, 'exec'),        dict(__file__=activar))
    return render_template( 'scrapers.html',result2=result2)
 

@blueprint.route('/configuracion', methods=['GET', 'POST'])
@login_required
def configuracion():
    msg_error=""
    
    if 'select_categorias' in request.form :
        select_categorias  = request.form['select_categorias']
        
        if select_categorias=="null":
            msg_error="Selecciona categoría"
        path=Path(__file__).parent.absolute()
        path=str(path).replace("webapp/app/home","")
        
        select_categorias=select_categorias.replace("_","-").replace(" ","-")
        
        fecha=os.listdir(str(path)+"DATOS_COMPUTRABAJO/")
        mayor=""
        leng=len(fecha)
        carpeta=max(fecha)
        
        archivos=list()
        paises=["colombia","argentina"]
        for pais in paises:
            archivo=str(path)+"DATOS_COMPUTRABAJO/"+carpeta+"/"+pais+"_"+str(select_categorias).replace(" ","-")+"_"+carpeta+".csv"
            print(select_categorias)
            if os.path.exists(archivo):
                archivos.append(archivo)
        
        for item in sys.path:
            if "datos_scrap" in item:
                carpeta=item.replace("webapp","")
        
        #sys.path.insert(1,carpeta)
        baz = module_from_file("funciones", carpeta+"/funciones.py")
        
        for item in archivos:
            if "colombia" in item:
        
        
                llama=baz.get_info(item,select_categorias,"colombia")    
            if "argentina" in item:
         
                llama=baz.get_info(item,select_categorias,"argentina")

        
    categorias = Categorias.query.order_by(Categorias.nombre.asc()).all()
    return render_template( 'configuracion.html',categorias=categorias,msg_error=msg_error)


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
        path=Path(__file__).parent.absolute()
        path=str(path).replace("webapp/app/home","webapp/app/")
        path=str(path)+"base/static/"
        paises=["colombia","argentina"]
        for pais in paises:
            archivo=str(path)+str(nombre).replace(" ","-")+"_"+pais+".png"
            if os.path.exists(archivo):
                print(archivo)
                remove(archivo)
        

        db.session.delete(catego)
        db.session.commit()
        

        
        return jsonify('URL borrado correcto'), 201


@blueprint.route("/getTecnologias/<id>", methods=["POST","GET"])
def route_get_tecnos(id):    
    #if  current_user.is_authenticated:
        #print( "delete from enlaces_rotos where id="+str(id) ) 

        tecnos = Tecnologias.query.filter_by(catego_id=id).order_by(Tecnologias.nombre.asc()).all()
        tecnologias=""
        for item in tecnos:
            tecnologias+=str(item)+","
        tecnologias=tecnologias[:-1]
       
        json_string = json.loads(json.dumps(tecnologias))
        
        return jsonify(json_string), 201


    
@blueprint.route("/tecnologias/delete/<nombre>", endpoint="delete_tecnologias", methods=["DELETE"])
def route_borra_tecnos(nombre):    
    #if  current_user.is_authenticated:
        #print( "delete from enlaces_rotos where id="+str(id) ) 

        tecno = Tecnologias.query.filter_by(nombre=nombre).first()
        db.session.delete(tecno)
        db.session.commit()
        return jsonify('URL borrado correcto'), 201
   

@blueprint.route('/tecnologias', methods=['GET', 'POST'])
@login_required
def tecnologias():
    tecno_form = TecnologiaForm(request.form)
    
    if 'nombre' in request.form :
        
        nombre  = request.form['nombre']
        nombres=nombre.split(",")
        todos_nombres=list()
        for item in nombres:
            todos_nombres.append(item.rstrip().lstrip())
        nombres=set(todos_nombres)
        for nombre in nombres:
            categoria_id  = request.form['categoria']
            nombre=nombre.upper()
            catego = Categorias.query.filter_by(id=categoria_id).first()
            tecnologias=Tecnologias.query.all()
            if catego is None:
                return render_template( 'tecnologias.html',msg_error='Selecciona Categoria',form=tecno_form)
            tecno = Tecnologias.query.filter_by(nombre=nombre).filter_by(catego_id=categoria_id).first()
            
            
            if tecno:
                continue
                return render_template( 'tecnologias.html', nombre=nombre,categoria=catego,msg_error='Tecnología existe ',form=tecno_form, tecno=tecno)
            
            tecno = Tecnologias(nombre,categoria_id)
            
            db.session.add(tecno)
            db.session.commit()
        tecnologias=Tecnologias.query.filter_by(catego_id=categoria_id).order_by(Tecnologias.nombre.asc()).all()
        registros=str(len(tecnologias)) +" registros"
        return render_template( 'tecnologias.html',nombre=nombre,registros=registros,tecnologias=tecnologias, msg='Tecnología creada¡¡',form=tecno_form)
        
        

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
