import sqlite3

from sqlite3 import Error

import platform
#print(platform.system())
from pathlib import Path
path=str(Path(__file__).parent.absolute())+"/webapp"

 
if platform.system()=='Windows':
   
    
    diagonal="\\"
else:    
    
    diagonal="/"


class Conexion (object):
    def __init__(self):
        try:
            print(path)
            self.conn = sqlite3.connect(path+"/database.db")
            
        except :
            pass
