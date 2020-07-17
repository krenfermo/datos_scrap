# -*- coding: utf-8 -*-
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import codecs
#from conexion import Conexion
import importlib.util

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_diccionario(descripcion,tecnologias_todas):
    
    tecnologias_lista=[]
    for word in  descripcion:
        text_descripcion=str(word).upper()
        for tecno in tecnologias_todas: 
            texto_tecno=str(tecno).upper()
            #print(texto_tecno)
            #print (text_descripcion)
            
            if texto_tecno in text_descripcion: 
                tecnologias_lista.append(texto_tecno)
    tecnologias=Counter(tecnologias_lista).most_common(10)
    #tecnologias=Counter(tecnologias_lista)
    
    return(dict(tecnologias))

def crear_grafica(tecnologias,total_empleos,rubro):
    valores=dict(tecnologias)
    manzanas = valores.values()
    nombres = valores.keys()
    plt.pie(manzanas, labels=nombres, autopct="%0.1f %%")
    plt.title("Los 10 más populares en "+str(total_empleos)+" empleos", bbox={'facecolor':'0.8', 'pad':5})
    try:
        path_img=str(path)+"/webapp/app/base/static/"+str(rubro.replace(" ","-"))+'.png'
    
    except Exception as ex:
        print(ex)
    
    fig=plt.savefig(path_img)
    plt.close(fig)
    #print(nombres)

def get_info(archivo,rubro,pais):
    rubro_pais=rubro+"_"+pais
    col_list = ["DESCRIPCION"]
    #print(archivo)
    df=pd.read_csv(archivo, sep=',',encoding="utf-8",usecols=col_list)
    #list1=df["EXPERIENCIA"]
    #anios_experiencia = Counter(list1)

    df=df.drop_duplicates()
    df['DESCRIPCION'] = df['DESCRIPCION'].replace(['"'],'')
 
    categoria=rubro

    for item in sys.path:
            if "datos_scrap" in item:
                carpeta=item.replace("webapp","")
    #print(carpeta)
    baz = module_from_file("conexion", carpeta+"/conexion.py")

    #baz.announce()
    #conexion=Conexion()
    conexion=baz.Conexion()            
    cur = conexion.conn.cursor()   
    cur.execute( "SELECT id FROM `categorias` where nombre='"+str(categoria).replace("-"," ")+"'")

    catego_id=cur.fetchone()
    #print(categoria)
    cur.execute( "SELECT nombre FROM `tecnologias` where catego_id="+str(catego_id[0]))
    tecnos=cur.fetchall()
    
    if tecnos:
        pass
    else:
        return False 
    conexion.conn.close()
    cadena_tecnos=list()
    for tecnologias in tecnos:
        cadena_tecnos.append( [x.replace("\n","").lstrip().rstrip() for x in tecnologias])
    
    
    cd_tecnos=list()   
    for item in cadena_tecnos:
        tec=item[0]
        cd_tecnos.append(tec.lower())
        
    
    #print(cd_tecnos)
    tecnologias_todas=set(cd_tecnos) 
    
    #tecnologias_todas=set(tecnologias) 
    
    conjunto=df["DESCRIPCION"]

    tecnologias=get_diccionario(conjunto,tecnologias_todas)
    
    
    if len(tecnologias)==0:
        return False
    print("va graficar")
    crear_grafica(tecnologias,len(conjunto),rubro_pais)


platform=sys.platform
if platform=="linux":
    diagonal="/"
else:
    diagonal="\\"
path=Path(__file__).parent.absolute()

if __name__ == "__main__":

    get_info("DATOS_COMPUTRABAJO/2020-07-14/colombia_INGENIERO-EN-SISTEMAS_2020-07-14.csv","INGENIERO-EN-SISTEMAS","colombia")
    exit() 
    categoria=str(sys.argv[1])
    conexion=Conexion()
                
    cur = conexion.conn.cursor()   
    cur.execute( "SELECT id FROM `categorias` where nombre='"+categoria+"'")
    catego_id=cur.fetchone()
    
    cur.execute( "SELECT nombre FROM `tecnologias` where catego_id="+str(catego_id[0]))
    tecnos=cur.fetchall()
    
     
    conexion.conn.close()
    cadena_tecnos=list()
    for tecnologias in tecnos:
        cadena_tecnos.append( [x.replace("\n","").lstrip().rstrip() for x in tecnologias])
    
    
    cd_tecnos=list()   
    for item in cadena_tecnos:
        tec=item[0]
        cd_tecnos.append(tec)
        
    
    print(cd_tecnos)
    tecnologias_todas=set(cd_tecnos) 
    print(tecnologias_todas)
    exit()
    
    #archivo=str(sys.argv[1])
    #rubro=str(sys.argv[2])
    #pais=str(sys.argv[3])
   
