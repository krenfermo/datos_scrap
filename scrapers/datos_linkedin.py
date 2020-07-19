# -*- coding: UTF-8 -*-
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
        print(soup) 
        exit()
        Total_pages = soup.find('span', class_='results-context-header__job-count').text.split(" ")[0] 
    #Total_pages =driver.find_element_by_xpath("display-flex t-12 t-black--light t-normal").text.split(" ")[0] 
    except Exception as ex:
        print(ex)
        #Total_pages =driver.find_element_by_xpath("/html/body/div[7]/div[3]/section[1]/div[2]/div/div/div[1]/div[1]/div[1]/small").text.split(" ")[0]
          
        print('error pagina') 
        return "error"       
        
        
        
    print(str(Total_pages)+ " resultados")
    Total_pages=int(Total_pages)/25
    #print(Total_pages)
    Total_pages=my_round(Total_pages+0.5)


    return(Total_pages) 




def cuerpo(Total_paginas,f,trabajo,location):
    for pages in range(0,Total_paginas) :
            pagina=int(pages)*25
            print("start"+str(pagina))
            URL=  "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?f_TPR=r86400&keywords="+str(trabajo)+"&location="+str(location)+"&f_TP=1&redirect=true&position=1&pageNum=0&start="+str(pagina)
            print("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?f_TPR=r86400&keywords="+str(trabajo)+"&location="+str(location)+"&f_TP=1&redirect=true&position=1&pageNum=0&start="+str(pagina))
            # Get login csrf token
            result = session_requests.get(URL, allow_redirects=True)


            #guardo en soup todo el codigo fuente para extraer los valores de la sesion
            soup = BeautifulSoup(result.content, 'html.parser')
            trabajos=soup.find_all('li')
            lista_trabajos=[]
            for item in trabajos:
                #print(item.find('a')["href"])
                lista_trabajos.append(item.find('a')["href"])
            
            
            for item in lista_trabajos:
                time.sleep(1)                
                navega_cada_pagina_2(item)
                 
                
                    
              
              

def navega_cada_pagina_2(pagina):    
    
    #print(pagina)  
    headers = {
"Upgrade-Insecure-Requests":"1",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",


"Sec-Fetch-Dest":"document",
 
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}

# Returns a requests.models.Response object
    scraper = cloudscraper.create_scraper()   
    
    result =  scraper.get(pagina, headers=headers)
    
    
     
    soup = BeautifulSoup(result.content, 'html.parser')
    #soup=soup.encode('iso-8859-1')
     
    
    try:
        nombre = soup.find('h1', class_='topcard__title')
        nombre=nombre.text
    except:
        nombre="S/D"
    
 
    try:    
        descripcion = soup.find('div', class_='description__text description__text--rich')
        descripcion=descripcion.text
    except:
        descripcion="S/D"
 
  
    #jobs-top-card__bullet 
    time.sleep(1)
    
    
    f.write("\""+pagina.lstrip().rstrip()+"\",")
    f.write("\""+quitar_signos(nombre)+"\",")
    f.write("\""+quitar_signos(descripcion)+"\"\n")
    
 
    
def linkedin():
    conexion=Conexion()
                
    cur = conexion.conn.cursor()   
    cur.execute( "SELECT nombre FROM `categorias`")
    categorias=cur.fetchall()
    print(categorias)

    conexion.conn.close()   
    paises=["colombia","argentina"]
    for pais in paises:
        for catego in categorias:
            #if "INGE" in catego[0]:continue
            #if "MARKE" in catego[0]:continue
            print(catego[0].replace(" ","-"))
            trabajo=str(catego[0].replace(" ","-"))

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
            ##
            
            location=pais

            LOGIN_URL="https://www.linkedin.com/jobs/search/?f_TPR=r86400&keywords="+str(trabajo)+"&location="+str(location)+"&f_TP=1&redirect=false&position=1&pageNum=0"
            #f_TPR=r86400&geoId=100446943
            print(LOGIN_URL)

            session_requests = requests.session()

            # Get login csrf token
            result = session_requests.get(LOGIN_URL, allow_redirects=True)


            #guardo en soup todo el codigo fuente para extraer los valores de la sesion
            soup = BeautifulSoup(result.content, 'html.parser')


            Total_paginas=paginas2(soup)
            if Total_paginas=="error":
                return 1
            print(str(Total_paginas)+" paginas")
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
            cuerpo(Total_paginas,f,trabajo,location)
            f.close()
            get_info(archivo_ruta,buscar,pais)
    return 0
if __name__ == "__main__":
    linkedin()
 