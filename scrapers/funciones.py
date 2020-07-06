# -*- coding: utf-8 -*-
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import codecs

def get_diccionario(descripcion,tecnologias_todas):
    tecnologias_lista=[]
    for word in  descripcion:
        for tecno in tecnologias_todas: 
            if tecno in word: 
                tecnologias_lista.append(tecno)
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
    #plt.show()
    fig=plt.savefig(str(Path(__file__).parent.absolute())+diagonal+rubro+'.png')
    plt.close(fig)

def get_info(archivo,rubro):
    col_list = ["DESCRIPCION", "EXPERIENCIA"]
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
        archivo_tecnologias=str(Path(__file__).parent.absolute())+diagonal+"dict_"+str(rubro)+".txt"
    #with codecs.open(str(Path(__file__).parent.absolute())+diagonal+"dict_"+str(rubro)+".txt", "r", encoding="ISO-8859-1",errors='ignore') as f:
    #    data = f.readlines()
    tecnos_df=pd.read_csv(archivo_tecnologias, sep=',',encoding = "utf-8")
    tecnologias=list(tecnos_df.columns)
    
    #tecnologias = data[0].split(",")
    tecnologias= [x.replace("\n","").lstrip().rstrip() for x in tecnologias]

    #tecnologias=map(str.strip, tecnologias)
    tecnologias_todas=set(tecnologias) 
 
    conjunto=df["DESCRIPCION"]

    tecnologias=get_diccionario(conjunto,tecnologias_todas)
    crear_grafica(tecnologias,len(conjunto),"marketing")


platform=sys.platform
if platform=="linux":
    diagonal="/"
else:
    diagonal="\\"

if __name__ == "__main__":
    archivo=str(sys.argv[1])
    get_info(archivo,"marketing")
 
