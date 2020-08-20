# flask packages
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# project resources
from models.products import Products
from api.errors import forbidden


class ProductsApi(Resource):
    """
    Flask-resftul resource for returning db.product collection.

    :Example:

    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config

    # Create flask app, config, and resftul api, then add ProductsApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(ProductsApi, '/product/')

    """
    @jwt_required
    def get(self) -> Response:
        """
        GET response method for all documents in product collection.
        JSON Web Token is required.

        :return: JSON object
        """
        output = Products.objects()
        return jsonify({'result': output})

    @jwt_required
    def post(self) -> Response:
        """
        POST response method for creating product.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)

        :return: JSON object
        """
        authorized: bool = Products.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            data = request.get_json()
            post_user = Products(**data).save()
            output = {'id': str(post_user.id)}
            return jsonify({'result': output})
        else:
            return forbidden()


class ProductApi(Resource):
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
    #@jwt_required
    def get(self, product_id: str) -> Response:
        """
        GET response method for single documents in product collection.

        :return: JSON object
        """
        output = Products.objects.get(id=product_id)
        return jsonify({'result': output})

    #@jwt_required
    def put(self, product_id: str) -> Response:
        """
        PUT response method for updating a product.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)

        :return: JSON object
        """
        data = request.get_json()
        put_user = Products.objects(id=product_id).update(**data)
        return jsonify({'result': put_user})

    #@jwt_required
    def delete(self, user_id: str) -> Response:
        """
        DELETE response method for deleting single product.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)

        :return: JSON object
        """
        authorized: bool = Products.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            output = Products.objects(id=user_id).delete()
            return jsonify({'result': output})
        else:
            return forbidden()
