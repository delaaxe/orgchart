import json

from flask import Flask, request
from flask_cors import CORS
from flask_restplus import Resource, Api

from orgchart import data

app = Flask(__name__)
CORS(app)
api = Api(app)
ns = api.namespace('orgchart', description='OrgChart operations', path='/orgchart/')

tree = data.load_mock_tree()


@ns.route('/entourage/<string:id>')
class OrgChartEntourage(Resource):
    def get(self, id):
        entourage = tree.get_entourage(id, 1)
        return json.dumps(tree.to_orgchart_dict(entourage))


@ns.route('/children/<string:id>')
class OrgChartChildren(Resource):
    def get(self, id):
        children = tree.get_children(id)
        return json.dumps({
            'children': [tree.to_orgchart_dict(child) for child in children]
        })


@ns.route('/parent/<string:id>')
class OrgChartParent(Resource):
    def get(self, id):
        parent = tree.get_parent(id)
        return json.dumps(tree.to_orgchart_dict(parent))


@ns.route('/siblings/<string:id>')
class OrgChartSiblings(Resource):
    def get(self, id):
        siblings = tree.get_siblings(id)
        return json.dumps({
            'siblings': [tree.to_orgchart_dict(sibling) for sibling in siblings]
        })


@ns.route('/family/<string:id>')
class OrgChartFamily(Resource):
    def get(self, id):
        family = tree.get_family(id)
        return json.dumps(tree.to_orgchart_dict(family))
