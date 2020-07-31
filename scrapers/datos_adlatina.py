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
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from selenium import webdriver


#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary



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
     
        
        
        
    #print(str(Total_pages)+ " resultados")
 
        
    Total_pages=int(Total_pages)/25
    #print(Total_pages)
    Total_pages=my_round(Total_pages+0.5)

    if Total_pages:
        return(Total_pages)
    else:
        return "error" 





def cuerpo(trabajo,f,scraper):

   
        URL="http://www.adlatina.com.ar/empleos/?q="+str(trabajo)+"&fecha=30"
        #print(URL)
        # Get login csrf token
        #result = scraper.get(URL, allow_redirects=True)
        #driver = webdriver.Firefox()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        display = Display(visible=0, size=(800, 600))
        display.start()
        try:
            
            driver = webdriver.chrome()
        except:
            print ("error driver")
            return 1
        #binary = FirefoxBinary('/usr/bin/firefox')
        #browser = webdriver.Firefox(firefox_binary=binary)
        driver.get(URL)
        driver.implicitly_wait(100)
        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        """last_height = driver.execute_script("return document.body.scrollHeight")

        this dowsnt work due to floating web elements on youtube
        """

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
               #print("break")
               break
            last_height = new_height
        #guardo en soup todo el codigo fuente para extraer los valores de la sesion
        
        try:
            scroll = driver.find_element_by_id('load_scroll')
        except:
            return False
        articulos = scroll.find_elements_by_tag_name('article')
        for item in articulos:
            item.click()
            
            time.sleep(2)
            
            articulo=driver.find_element_by_class_name('fancybox-content')
            nombre=articulo.find_element_by_tag_name('h1')
            
            #print(nombre.text)
            descripcion=articulo.find_element_by_tag_name('p')
            #print(descripcion.text)
            #print(parafo)
            articulo.find_element_by_class_name('close').click()
            
            
            f.write("\""+URL+"\",")
            f.write("\""+quitar_signos(nombre.text)+"\",")
    
    
            f.write("\""+quitar_signos(descripcion.text)+"\"\n")
            #exit()
            time.sleep(2)
            
        
        #soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        
        #print (soup)
        #trabajos=soup.find('div',{"id": "load_scroll"})
        
        #try:
        #    articles=trabajos.find_all('article')
            
        #except:
        #    print("error home")
        #print (articles)
        #exit()



def adlatina():
    print("adlatina")
    conexion=Conexion()
                
    cur = conexion.conn.cursor()   
    cur.execute( "SELECT nombre FROM `categorias`")
    categorias=cur.fetchall()
    #print(categorias)

    conexion.conn.close()   
    paises=["argentina"]
    for pais in paises:
        for catego in categorias:
            #if "DISE" in catego[0]:continue
            #if "MARKE" in catego[0]:continue
            
            #print(catego[0].replace(" ","-"))
            trabajo=str(catego[0].replace(" ","-"))

            scraper = cloudscraper.create_scraper() 

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
            #print(path)
            if os.path.exists(path):
                #print("CARPETA YA EXISTIA Y NO LA CREA")
                pass
            else:
                
                os.mkdir(path)
                #print("CARPETA CREADA")
                
            archivo_ruta=path+diagonal+pais+"_"+trabajo+"_"+hoy+".csv"
            if os.path.exists(archivo_ruta):
                
                f= open(archivo_ruta,"a+")
            else:
                f= open(archivo_ruta,"a+")
                f.write("\"URL\","+"\"NOMBRE\","+"\"DESCRIPCION\"\n")

            cuerpo(trabajo,f,scraper)
            f.close()

            get_info(archivo_ruta,trabajo,pais)
    return 0
    
if __name__ == "__main__":
    adlatina()
