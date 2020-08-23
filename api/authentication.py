# flask packages
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine.errors import *
# project resources
from models.users import Users
from models.cart import Cart
from api.errors import unauthorized

# external packages
import datetime


class SignUpApi(Resource):
    """
    Flask-resftul resource for creating new user.

    :Example:

    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config

    # Create flask app, config, and resftul api, then add SignUpApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(SignUpApi, '/authentication/signup')

    """
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        data = request.get_json()
        
        usercart = Cart().save()
        output = {'id': str(usercart.id)}
        
        y = {"cartId": str(usercart.id)} 
        print('usercart')
        print(usercart.id)
        print(usercart.products)
        print('data')
        print(data)
        data.update(y)
        print('data')
        print(data)
        post_user = Users(**data)
        try:
            post_user.save()
        except NotUniqueError as exc:

            return {'message': "Email Id already exits!!"}, 400
        output = {'id': str(post_user.id)}
        return jsonify({'result': output})


class LoginApi(Resource):
    """
    Flask-resftul resource for retrieving user web token.

    :Example:

    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config

    # Create flask app, config, and resftul api, then add LoginApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(LoginApi, '/authentication/login')

    """
    @staticmethod
    def post() -> Response:
        """
        POST response method for retrieving user web token.

        :return: JSON object
        """
        data = request.get_json()
        try:
            user = Users.objects.get(email=data.get('email'))
        except :
            return {'message': "Email Id does not exits!!"}, 400
        auth_success = user.check_pw_hash(data.get('password'))
        if not auth_success:
            return {'message': "password wrong!!"}, 400
        else:
            expiry = datetime.timedelta(days=5)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({'jwt': access_token,
                                       'refresh_token': refresh_token,
                                       'cartId':user.cartId,
                                       'user': f"{user.username}"})
