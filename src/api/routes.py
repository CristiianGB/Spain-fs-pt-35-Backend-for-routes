
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import datetime
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Event, Group, Image, Post, Group_participation, Event_participation, Form_friendship, Event_comments, Post_comments
from api.utils import generate_sitemap, APIException
from sqlalchemy.sql import text
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, get_jwt
from slugify import slugify

api = Blueprint('api', __name__)
##CREA LAS SIGUIENTES RUTAS ==> /signup --- /login --- un CRUD para los POSTS ( Create, Read, Update, Delete )


################################################################################
#                                   signup                                     #
################################################################################




################################################################################
#                                   Login                                      #
################################################################################



################################################################################
#                               CRUD Posts                                     #
################################################################################
