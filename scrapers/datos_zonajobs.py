import requests
from pathlib import Path
from bs4 import BeautifulSoup
import sys
import math
import time
from datetime import datetime
import cloudscraper
import codecs
from funciones import get_info
from conexion import Conexion
import os

def my_round(i):
    f = math.floor(i)
    return f if i - f < 0.5 else f+1

def quitar_signos(s):
    replacements = (
        (",", ""),
        ("\"", ""),
         
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s
  
def paginas2(soup):
     
    try:        
        Total_pages = soup.find('div', class_='listado-empleos col-sm-9 col-md-9')
        Total_pages = Total_pages.find('h1').find('strong').text 
    except:
          
        print('error pagina') 
        return "error"
     
        
        
        
    print(str(Total_pages)+ " resultados")
 
        
    Total_pages=int(Total_pages)/25
    #print(Total_pages)
    Total_pages=my_round(Total_pages+0.5)

    if Total_pages:
        return(Total_pages)
    else:
        return "error" 





def cuerpo(Total_paginas,trabajo,f,scraper):
    for pages in range(1,Total_paginas+1) :
             
            print("pagina: "+str(pages))
            
            URL="https://www.zonajobs.com.ar/ofertas-de-trabajo-"+str(trabajo)+"-pagina-"+str(pages)+".html"
            print(URL)
            # Get login csrf token
            result = scraper.get(URL, allow_redirects=True)

            #guardo en soup todo el codigo fuente para extraer los valores de la sesion
            soup = BeautifulSoup(result.content, 'html.parser')
            
            
            trabajos=soup.find('div',class_='aviso-no-sponsor')
            
            try:
                homes=trabajos.find_all('div',class_='aviso aviso-home clearfix')
                
            except:
                print("error home")
            try:
                destacados=trabajos.find_all('div',class_='aviso aviso-destacado clearfix')
            except:
                print("error destacados")
            try:
                simples=trabajos.find_all('div',class_='aviso aviso-simple clearfix')
            except:
                print("error simples")
            lista_trabajos=[]
            #print("HOMES:")
            for item in homes:                
                #print(item.find('a')["href"])
                lista_trabajos.append(item.find('a')["href"])
            #print("DESTACATDOS:")    
            for item in destacados:
                #print(item["id"])
                lista_trabajos.append(item["id"])
            
            
            #print("SIMPLES:")    
            for item in simples:
                #print(item["id"])
                lista_trabajos.append(item["id"])
            #time.sleep(1)
                
                
               
            
            for item in lista_trabajos:
                #time.sleep(1)    
                #print(item)            
                
                navega_cada_pagina_2("https://www.zonajobs.com.ar"+str(item),f)
                
                
                
                 


def navega_cada_pagina_2(pagina,f):    
    
    #print(pagina)  
    headers = {
"Upgrade-Insecure-Requests":"1",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",


"Sec-Fetch-Dest":"document",
 
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}


    scraper = cloudscraper.create_scraper()   
    
    result =  scraper.get(pagina, headers=headers)    
    
     
    soup = BeautifulSoup(result.content, 'html.parser')

    
    try:
        nombre = soup.find('h1', class_='aviso_title')
        nombre=nombre.text.lstrip().rstrip()
    except:
        nombre="S/D"
    #print(nombre)
    
 
    
    try:    
        descripcion = soup.find('div', class_='aviso_description')
        descripcion=descripcion.text.lstrip().rstrip()
    except:
        descripcion="S/D"
    
    #print(descripcion)



    #time.sleep(1)
     
        
    f.write("\""+pagina.lstrip().rstrip()+"\",")
    f.write("\""+quitar_signos(nombre)+"\",")
    
    
    f.write("\""+quitar_signos(descripcion)+"\"\n")
    


def zonajobs():
    conexion=Conexion()
                
    cur = conexion.conn.cursor()   
    cur.execute( "SELECT nombre FROM `categorias`")
    categorias=cur.fetchall()
    print(categorias)

    conexion.conn.close()   
    paises=["argentina"]
    for pais in paises:
        for catego in categorias:
            #if "DISE" in catego[0]:continue
            #if "MARKE" in catego[0]:continue
            
            print(catego[0].replace(" ","-"))
            trabajo=str(catego[0].replace(" ","-"))

            #trabajo=sys.argv[1].replace(" ","-")

              
            LOGIN_URL="https://www.zonajobs.com.ar/ofertas-de-trabajo-"+str(trabajo)+"-pagina-1.html"

            print(LOGIN_URL)

            scraper = cloudscraper.create_scraper() 
            # Get login csrf token
            result = scraper.get(LOGIN_URL, allow_redirects=True)


            #guardo en soup todo el codigo fuente para extraer los valores de la sesion
            soup = BeautifulSoup(result.content, 'html.parser')


            Total_paginas=paginas2(soup)
            if Total_paginas=="error":
                return 1
            print(str(Total_paginas)+" paginas")
            platform=sys.platform
            if platform=="linux":
                diagonal="/"
            else:
                diagonal="\\"

            formato1 = "%Y-%m-%d"
            #formato1 = "%Y-%m-%d %H"
            hoy = datetime.today()
            hoy = hoy.strftime(formato1)  
            path=Path(__file__).parent.absolute()

            path=str(path)+diagonal+"DATOS_COMPUTRABAJO"
            if os.path.exists(path):
                pass
            else:     
                os.mkdir(path)
                
            path=str(path)+diagonal+hoy
            print(path)
            if os.path.exists(path):
                print("CARPETA YA EXISTIA Y NO LA CREA")
            else:
                
                os.mkdir(path)
                print("CARPETA CREADA")
                
            archivo_ruta=path+diagonal+pais+"_"+trabajo+"_"+hoy+".csv"
            if os.path.exists(archivo_ruta):
                
                f= open(archivo_ruta,"a+")
            else:
                f= open(archivo_ruta,"a+")
                f.write("\"URL\","+"\"NOMBRE\","+"\"DESCRIPCION\"\n")

            cuerpo(Total_paginas,trabajo,f,scraper)
            f.close()
            print("llega a info")
            get_info(archivo_ruta,trabajo,pais)
    return 0
