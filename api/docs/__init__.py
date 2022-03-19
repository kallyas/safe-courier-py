from .resources import *

def docs_route(api):
    api.add_resource(DocsResource, '/docs')