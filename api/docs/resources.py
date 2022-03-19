# API DOCS

from flask_restful import Resource
from flask import render_template, make_response



class DocsResource(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('docs.html'), 200, headers)
        