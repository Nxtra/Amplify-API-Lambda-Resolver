from urllib import request, error
from datetime import datetime
import simplejson
from pprint import pprint
import json


class GraphqlClient:

    def __init__(self, endpoint, headers):
        self.endpoint = endpoint
        self.headers = headers

    @staticmethod
    def serialization_helper(o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    def execute(self, query, operation_name, variables={}):
        data = simplejson.dumps({
            "query": query,
            "variables": variables,
            "operationName": operation_name
        },
            default=self.serialization_helper,
            ignore_nan=True
        )
        r = request.Request(
            headers=self.headers,
            url=self.endpoint,
            method='POST',
            data=data.encode('utf8')
        )
        response = None
        try:
            response = request.urlopen(r).read()
        except error.HTTPError as e:
            return e.read().decode()  # Read the body of the error response

        return json.loads(response.decode('utf8'))
