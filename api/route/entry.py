from flask_restful import Resource


class Entry(Resource):

    def get(self):
        return {
            'status': 'ok',
            'version': '1.0'
        }
