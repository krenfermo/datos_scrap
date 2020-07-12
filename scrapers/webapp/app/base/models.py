# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String,ForeignKey

from sqlalchemy.orm import relationship

from app import db, login_manager

from app.base.util import hash_pass

class Categorias(db.Model):

    __tablename__ = 'Categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    def __init__(self, nombre):
        self.nombre = nombre
        
    def __repr__(self):
        return str(self.nombre)
    
class Tecnologias(db.Model):

    __tablename__ = 'Tecnologias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    catego_id = Column(Integer)
    #categorias = relationship('Categorias', backref='Categoria')


    def __init__(self, nombre,catego_id):
        self.nombre = nombre 
        self.catego_id= catego_id 
    def __repr__(self):
        return '<Categoria %r>' % (self.nombre)
def getCategoria():
    p = Categorias.query
    return p   
    
class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

