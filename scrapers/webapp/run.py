# -*- encoding: utf-8 -*-
"""
License: Commercial
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from os import environ
from sys import exit

from config import config_dict
from app import create_app, db
from flask_cors import CORS
#from flask_wtf.csrf import CSRFProtect
   

get_config_mode = environ.get('APPSEED_CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
    
except KeyError:
    exit('Error: Invalid APPSEED_CONFIG_MODE environment variable entry.')

app = create_app(config_mode) 
Migrate(app, db)
CORS(app) 
#csrf = CSRFProtect(app) 
#csrf.init_app(app)

if __name__ == "__main__":
   app.run(debug=True,port=5000, host='0.0.0.0') 
