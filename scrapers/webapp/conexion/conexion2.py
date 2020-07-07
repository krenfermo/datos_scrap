'''
import mysql.connector

host='localhost'
user= 'joacho'
passwd='joacho12345*'
db='promall'

config = {'user': user,
'password': passwd,
'host': host,
'database': db,
'raise_on_warnings': True}

miConexion = mysql.connector.connect(**config)
miConexion.set_charset_collation('latin1')
'''


import sqlite3
from sqlite3 import Error

import platform
#print(platform.system())
from pathlib import Path
path=str(Path().absolute())
 
if platform.system()=='Windows':
   
    
    diagonal="\\"
else:    
    
    diagonal="/"


class Conexion (object):
    def __init__(self):
        try:
            self.conn = sqlite3.connect(path+"/conexion/base_productos.db")
        except :
            pass
            



 

 
