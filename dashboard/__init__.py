# -*- coding: utf-8 -*-
from __future__ import absolute_import

import copy

import redis
from flask import Flask
from flask_restful import Api

from .conf import config


# app = Flask("__name__", static_folder="./static", template_folder="./templates")
# app = Flask("dashboard", static_folder="./static", template_folder="./templates")
# app = Flask("dashboard")
app = Flask(__name__)
api = Api(app)

r_kv = redis.Redis(host=config.redis_kv_host, port=config.redis_kv_port, db=config.redis_kv_db)
r_db = redis.Redis(host=config.redis_db_host, port=config.redis_db_port, db=config.redis_db_db)


log = config.logger


from . import client
from .server import views
