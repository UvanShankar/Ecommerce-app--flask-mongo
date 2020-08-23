# flask packages
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# project resources
from models.cart import Cart
from api.errors import forbidden


class CartApi(Resource):
    """
    Flask-resftul resource for returning db.product collection.

    :Example:

    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config

    # Create flask app, config, and resftul api, then add productApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(productApi, '/product/<product_id>')

    """
    
    def get(self, cart_id: str) -> Response:
        """
        GET response method for single documents in product collection.

        :return: JSON object
        """
        output = Cart.objects.get(id=cart_id)
        return jsonify({'result': output})
    

    def put(self, cart_id: str) -> Response:
        """
        PUT response method for updating a product.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)

        :return: JSON object
        """
        data = request.get_json()
        put_user = Cart.objects(id=cart_id).update(**data)
        return jsonify({'result': put_user})
