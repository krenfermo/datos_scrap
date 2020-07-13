# -*- coding: utf-8 -*-
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import codecs
from conexion import Conexion

def get_diccionario(descripcion,tecnologias_todas):
    tecnologias_lista=[]
    for word in  descripcion:
        text_descripcion=word.upper()
        for tecno in tecnologias_todas: 
            texto_tecno=tecno.upper()
            if texto_tecno in text_descripcion: 
                tecnologias_lista.append(texto_tecno)
    tecnologias=Counter(tecnologias_lista).most_common(10)
    #tecnologias=Counter(tecnologias_lista)
    print(dict(tecnologias))
    return(dict(tecnologias))

def crear_grafica(tecnologias,total_empleos,rubro):
    valores=dict(tecnologias)
    manzanas = valores.values()
    nombres = valores.keys()
    plt.pie(manzanas, labels=nombres, autopct="%0.1f %%")
    plt.title("Los 10 más populares en "+str(total_empleos)+" empleos", bbox={'facecolor':'0.8', 'pad':5})
    path_img=str(path)+"/webapp/app/base/static/"+str(rubro.replace(" ","_"))+'.png'
    fig=plt.savefig(path_img)
    plt.close(fig)

def get_info(archivo,rubro,pais):
    rubro_pais=rubro+"_"+pais
    col_list = ["DESCRIPCION", "EXPERIENCIA"]
    print("llega")
    df=pd.read_csv(archivo, sep=',',encoding="utf-8",usecols=col_list)
    list1=df["EXPERIENCIA"]
    anios_experiencia = Counter(list1)

    df=df.drop_duplicates()

    descripcion_todas=[]
    descripcion_1=[]
    descripcion_2=[]
    descripcion_3=[]
    descripcion_4=[]
    descripcion_5=[]
    descripcion_6=[]
    descripcion_nada=[]
    contador=0

    for descr in  df["DESCRIPCION"]:
      
        experiencia=str(df["EXPERIENCIA"].values[contador])
        if experiencia=="1":
            descripcion_1.append(descr)
        if experiencia=="2" or experiencia=="3":
            descripcion_2.append(descr)
        if experiencia=="4" or  experiencia=="5":
            descripcion_3.append(descr)
        if experiencia=="6":
            descripcion_4.append(descr)
        if experiencia=="N/D":
            descripcion_nada.append(descr)
        contador+=1
    #archivo_tecnologias=str(Path(__file__).parent.absolute())+diagonal+"dict_"+str(rubro)+".txt"
 
    
    #tecnos_df=pd.read_csv(archivo_tecnologias, sep=',',encoding = "utf-8")
    #tecnologias=list(tecnos_df.columns)
    
    
    #tecnologias= [x.replace("\n","").lstrip().rstrip() for x in tecnologias]

    #tecnologias=map(str.strip, tecnologias)
    
    categoria=rubro
    conexion=Conexion()
                
    cur = conexion.conn.cursor()   
    cur.execute( "SELECT id FROM `categorias` where nombre='"+str(categoria).replace("-"," ")+"'")

    catego_id=cur.fetchone()
    print(categoria)
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
        
    
    print(cd_tecnos)
    tecnologias_todas=set(cd_tecnos) 
    #print(tecnologias)
    #tecnologias_todas=set(tecnologias) 
    
    conjunto=df["DESCRIPCION"]

    tecnologias=get_diccionario(conjunto,tecnologias_todas)
    if len(tecnologias)==0:
        return False
    crear_grafica(tecnologias,len(conjunto),rubro_pais)


platform=sys.platform
if platform=="linux":
    diagonal="/"
else:
    diagonal="\\"
path=Path(__file__).parent.absolute()

if __name__ == "__main__":
    get_info("DATOS_COMPUTRABAJO/2020-07-12/argentina_DISEÑO-DIGITAL_2020-07-12.csv","DISEÑO-DIGITAL","argentina")
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
   
