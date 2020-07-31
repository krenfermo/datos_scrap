
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import math
import time
import sys
import os

from datetime import datetime
from pathlib import Path
import cloudscraper
import codecs
import re
from funciones import get_info
from conexion import Conexion

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def my_round(i):
    f = math.floor(i)
    return f if i - f < 0.5 else f+1

def navega_page(pagina):
     
    #print(pagina)
    #headers = {'User-Agent': 'Mozilla/5.0'}
    headers = {
            "Upgrade-Insecure-Requests":"1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",


            "Sec-Fetch-Dest":"document",
            
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            }

    # Returns a requests.models.Response object
    scraper = cloudscraper.create_scraper()   
    
    page =  scraper.get(pagina, headers=headers)
    #page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='content-result cont-search-list')
    
    return soup


 


def navega_cada_pagina(pagina,scraper,f):
     
    #print(pagina)
     
    
    headers = {
    "Upgrade-Insecure-Requests":"1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",


    "Sec-Fetch-Dest":"document",
    
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
   
    page =  scraper.get(pagina, headers=headers)
    #page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    extraccion(soup,pagina,f)
     
        
def genera_archivo(texto)  :
    archivo= codecs.open(path+"\\"+"URL_.html","w+","utf-8")
    archivo.write(str(texto))
    archivo.close() 


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("Á", "A"),
        ("É", "E"),
        ("Í", "I"),
        ("Ó", "O"),
        ("Ú", "U"),
        ("Ñ", "N"),
        ("ñ", "n"),
        ("Ü", "U"),
        ("ü", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def quitar_signos(s):
    replacements = (
        (",", ""),
        ("\"", ""),
         
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s
    

def extraccion(soup,pagina,f):
    try:
        nombre = soup.find('article', id='ContentPlaceHolder1_hidCompany') 
        nombre=nombre.find('h1').text.lstrip().rstrip()
        
 
        
        
    except:
        return False
       
  
    try:    
        Descripcion = soup.find('ul', class_='p0 m0')
        #"<h3>Requerimientos</h3>"
        if "<h3>Requerimientos</h3>" in str(Descripcion):
            
            Descripcion2_lista=str(Descripcion).split("<h3>Requerimientos</h3>")
            #print("entra1") 
            Descripcion2=Descripcion2_lista[0]
            Descripcion2=str(Descripcion2).split('<h3 class="mt0">Descripción</h3>')
            #print("entra1") 
            #print(Descripcion2)
            Descripcion2 = cleanhtml(str(Descripcion2[1]))
            #print("entra1") 
            Descripcion2=Descripcion2.lstrip().rstrip()
            #print("entra1") 
            Descripcion=Descripcion2.replace("\"","")
            #print("entra1") 

        else:
           
            Descripcion=Descripcion.text
            
            
    except Exception as e:
        #print( "<p>Error: %s</p>" % str(e) )
        #print("error")
        Descripcion="N/D"   
        
   
           
    f.write("\""+pagina.lstrip().rstrip()+"\",")
    f.write("\""+quitar_signos(nombre)+"\",")
    f.write("\""+str(Descripcion)+"\"\n")
 
        

def cuerpo(URL,ext_dominio,buscar,f): 
        soup=navega_page(URL)
        
        try:
            #print("entra")    
            #no_results=soup.find('div', class_='content-errors')
            if "No se ha encontrado ofertas" in str(soup):
                #print("No se ha encontrado ofertas de trabajo con los filtros actuales")
                return False
            Total_pages = soup.find('div', class_='breadtitle_mvl')
            
            Total_pages=Total_pages.find('span').text.replace(",","")
             
            #print(str(Total_pages)+" resultados")
            Total_pages=int(Total_pages)/20
            #print(Total_pages)
            Total_pages=my_round(Total_pages+0.5)


            #print(str(Total_pages) + " paginas" )
            
            
            
        except:
             print("error")
             return False
        
        
        for pages in range(1,Total_pages+1) :
            list_url=list()
            URL2="https://www.computrabajo.com."+ext_dominio+"/trabajo-de-"+str(buscar)+"?p="+str(pages)+"&q="+str(buscar)   
 
            #print("PAGINA:"+ str(pages))
            soup =  navega_page(URL2)
 
            
            results = soup.find('div', id='p_ofertas')
            
            elements = results.select('div[class*="bRS bClick"]')
            
            
            #print(elements)
            for job_elem in elements:
                
                
                a_href = job_elem.find('a', class_='js-o-link')
                
                #print(a_href)
                if a_href["href"]==None:
                    #print("continua")
                    continue        
               
                list_url.append("https://www.computrabajo.com."+ext_dominio+str(a_href["href"]))
                
                 
            
            for item in list_url:
                scraper = cloudscraper.create_scraper() 
                navega_cada_pagina(item,scraper,f)
                
                #print (item)
                


#https://www.computrabajo.com.ar/trabajo-de-marketing?p=1&q=marketing
def computrabajo():
    print("computrbajo")
    conexion=Conexion()
                
    cur = conexion.conn.cursor()   
    cur.execute( "SELECT nombre FROM `categorias`")
    categorias=cur.fetchall()
    #print(categorias)

    conexion.conn.close()   
    paises=["colombia","argentina"]
    for pais in paises:
        for catego in categorias:
            #if "INGE" in catego[0]:continue
            #if "MARKE" in catego[0]:continue
            #print(catego[0].replace(" ","-"))
            buscar=str(catego[0].replace(" ","-"))

            #buscar=str(sys.argv[1]).replace(" ","-")
            #pais=str(sys.argv[2])

            ext_dominio=""
            if pais=="colombia":
                ext_dominio="co"
            if pais=="argentina":
                ext_dominio="ar"

            path=Path(__file__).parent.absolute()
            platform=sys.platform
            if platform=="linux":
                diagonal="/"
            else:
                diagonal="\\"

            pagina_inicial=1
            URL="https://www.computrabajo.com."+ext_dominio+"/trabajo-de-"+str(buscar)+"?p="+str(pagina_inicial)+"&q="+str(buscar)   

            formato1 = "%Y-%m-%d"
            #formato1 = "%Y-%m-%d %H"
            hoy = datetime.today()
            hoy = hoy.strftime(formato1)  


            path=str(path)+diagonal+"DATOS_COMPUTRABAJO"
            if os.path.exists(path):
                pass
            else:     
                os.mkdir(path)
                
            path=str(path)+diagonal+hoy
            #print(path)
            if os.path.exists(path):
                #print("CARPETA YA EXISTIA Y NO LA CREA")
                pass
            else:
                
                os.mkdir(path)
                #print("CARPETA CREADA")

            archivo_ruta=path+diagonal+pais+"_"+buscar+"_"+hoy+".csv"
            if os.path.exists(archivo_ruta):
                
                f= open(archivo_ruta,"a+")
            else:
                f= open(archivo_ruta,"a+")
                f.write("\"URL\","+"\"NOMBRE\","+"\"DESCRIPCION\"\n")
            
            

            cuerpo(URL,ext_dominio,buscar,f)

            f.close() 

            get_info(archivo_ruta,buscar,pais)
if __name__ == "__main__":
    computrabajo()

