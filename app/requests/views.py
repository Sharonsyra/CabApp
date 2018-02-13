from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app

    @app.route('/orders/', methods=['POST', 'GET'])
    def orders():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                order = Order(name=name)
                order.save()
                response = jsonify({
                    'id': order.id,
                    'name': order.name,
                    'justification': order.justification,
                    'date_created': order.date_created,
                    'date_modified': order.date_modified
                })
                response.status_code = 201
                return response
        else:
            orders = Order.get_all()
            results = []

            for order in orders:
                obj = {
                    'id': order.id,
                    'name': order.name,
                    'justification': order.justification,
                    'date_created': order.date_created,
                    'date_modified': order.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    return app

    @app.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def order_manipulation(id, **kwargs):
        order = Order.query.filter_by(id=id).first()
        if not order:
            abort(404)

        if request.method == 'DELETE':
            order.delete()
            return {
            "message": "order {} deleted successfully".format(order.id) 
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            order.name = name
            order.save()
            response = jsonify({
                'id': order.id,
                'name': order.name,
                'justification': order.justification,
                'date_created': order.date_created,
                'date_modified': order.date_modified
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'id': order.id,
                'name': order.name,
                'justification': order.justification,
                'date_created': order.date_created,
                'date_modified': order.date_modified
            })
            response.status_code = 200
            return response

    return app