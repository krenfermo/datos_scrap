# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Email, DataRequired
from app.base.models import Categorias

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])
    
class CategoriaForm(FlaskForm):
    nombre = TextField    ('Nombre', id='nombre_categora'   , validators=[DataRequired()])


class TecnologiaForm(FlaskForm):
    nombre = TextField    ('Nombre', id='nombre_tecnologia'   , validators=[DataRequired()])
    categoria=QuerySelectField(query_factory=lambda: Categorias.query.all(),allow_blank=True, blank_text=u'-- selecciona categoria --')
