import sqlite3


conn = sqlite3.connect('base_productos.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

# Create table - CLIENTS
#c.execute('''CREATE TABLE enlaces_rotos
#             ([id] INTEGER PRIMARY KEY,[url] text, [fecha_encontrado] text, [bodega] text)''')
          
# Create table - COUNTRY
c.execute('''CREATE TABLE precios_cambiados
             ([id] INTEGER PRIMARY KEY,[precio_publico] text, [bodega] text,[codigo] text, [codigo_prov] text,[costo] text, [precio_prov] text, [fecha_actualizacion] text)''')
        
   
conn.commit()