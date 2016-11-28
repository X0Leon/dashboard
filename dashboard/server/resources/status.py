# -*- coding: utf-8 -*-

import json

from flask import render_template, make_response
from flask_restful import Resource

from dashboard import r_db, config
from ..utils import build_response


class Status(Resource):
    """
    Just for restful api test use
    """
    def get(self):
        return build_response(dict(data="hello, world", code=200))
