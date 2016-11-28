# -*- coding: utf-8 -*-

import json

from flask_restful import Resource

from dashboard import r_kv
from ..utils import build_response


class KeyList(Resource):
    """
    Get the keys in database.

    Return all the keys exist in database which are used to
    store data for build table and visualization. i.e, those
    data shared by users in ipython.

    Attributes:
    """
    def get(self):
        """
        Get key list in storage.
        """
        keys = r_kv.keys()
        keys.sort()
        return build_response(dict(data=keys, code=200))


class Key(Resource):
    """
    Get the data of a key.

    Get all the data of a key. Both Key and KeyList API has much to
    implement in future to make it more usable. Namely, auto-complete
    for KeyList, and fetch part of data via a key for this API.

    Attributes:
    """
    def get(self, key):
        """Get a key-value from storage according to the key name.
        """
        data = r_kv.get(key)
        # data = json.dumps(data) if isinstance(data, str) else data
        # data = json.loads(data) if data else {}

        return build_response(dict(data=data, code=200))
