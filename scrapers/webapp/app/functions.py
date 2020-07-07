
import random
 


import json

from datetime import datetime,date,timedelta
#import jsonpickle
from conexion import conexion2

from json import JSONEncoder
 

class setEncoder(JSONEncoder):
        def default(self, obj):
            return list(obj)

def f_delete_rotos(id):
    conn=conexion2.Conexion()
            
    cur = conn.conn.cursor()   
    cur.execute( "delete from enlaces_rotos where id="+str(id) ) 
    conn.conn.commit()
    
    
    conn.conn.close()

    return True

def f_precios(codigo):
      
    formato1_anio = "%Y"
    formato1_mes = "%m"
     
 
    fecha_actual=datetime.today()
    fecha_actual_anio=fecha_actual.strftime(formato1_anio) 
    fecha_actual_mes=fecha_actual.strftime(formato1_mes) 
  
    
    
    minimo=int(fecha_actual_anio)-1
    minimo=str(minimo)+"-"+str(fecha_actual_mes)
    
    
    
    maximo=int(fecha_actual_anio)
    
    
    if fecha_actual_mes=='01':
        mes='02'
        
    if fecha_actual_mes=='02':
        mes='03'
        
    if fecha_actual_mes=='03':
        mes='04'
        
    if fecha_actual_mes=='04':
        mes='05'
        
    if fecha_actual_mes=='05':
        mes='06'
        
    if fecha_actual_mes=='06':
        mes='07'
        
    if fecha_actual_mes=='07':
        mes='08'
        
    if fecha_actual_mes=='08':
        mes='09'    
    
    if fecha_actual_mes=='09':
        mes='10'
        
    if fecha_actual_mes=='10':
        mes='11'
    
    if fecha_actual_mes=='11':
        mes='12'
    
    if fecha_actual_mes=='12':
        mes='13'
        
    maximo=str(maximo)+"-"+str(mes)
    
    


    conn=conexion2.Conexion()
            
    cur = conn.conn.cursor()   
   
    #print( "SELECT * FROM `precios_historico` where (codigo like \'%"+str(codigo)+"%\' or codigo_prov like \'%"+str(codigo)+"%\')  and `fecha_actualizacion` BETWEEN  \'"+str(minimo)+"%\' AND \'"+str(maximo)+"%\'")
    cur.execute( "SELECT * FROM `precios_historico` where (codigo like \'%"+str(codigo)+"%\' or codigo_prov like \'%"+str(codigo)+"%\')  and `fecha_actualizacion` BETWEEN  \'"+str(minimo)+"%\' AND \'"+str(maximo)+"%\'")
    precios=cur.fetchall()
    #print(precios)
    conn.conn.close()   
    return  {"precios": [{"id": x[0], "precio": x[1], "fecha_actualizacion": x[2], "bodega": x[3], "codigo": x[4], "codigo_prov": x[5], "costo": x[6], "precio_prov": x[7]} for x in precios]}
    
    



def f_precios_cambiados(codigo):
      
  

    conn=conexion2.Conexion()
            
    cur = conn.conn.cursor()   
   
    #print( "SELECT * FROM `precios_historico` where (codigo like \'%"+str(codigo)+"%\' or codigo_prov like \'%"+str(codigo)+"%\')  and `fecha_actualizacion` BETWEEN  \'"+str(minimo)+"%\' AND \'"+str(maximo)+"%\'")
    cur.execute( "SELECT * FROM `precios_cambiados` where (codigo like \'%"+str(codigo)+"%\' or codigo_prov like \'%"+str(codigo)+"%\') ")
    precios=cur.fetchall()
    #print(precios)
    conn.conn.close()   
    return  {"precios": [{"id": x[0], "precio": x[1], "fecha_actualizacion": x[2], "bodega": x[3], "codigo": x[4], "codigo_prov": x[5], "costo": x[6], "precio_prov": x[7]} for x in precios]}
    
    
     