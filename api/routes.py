# flask packages
from flask_restful import Api

# project resources
from api.authentication import SignUpApi, LoginApi
from api.user import UsersApi, UserApi
from api.product import ProductsApi, ProductApi


def create_routes(api: Api):
    """Adds resources to the api.

    :param api: Flask-RESTful Api Object

    :Example:

        api.add_resource(HelloWorld, '/', '/hello')
        api.add_resource(Foo, '/foo', endpoint="foo")
        api.add_resource(FooSpecial, '/special/foo', endpoint="foo")

    """
    api.add_resource(SignUpApi, '/authentication/signup/')
    api.add_resource(LoginApi, '/authentication/login/')

    api.add_resource(UsersApi, '/user/')
    api.add_resource(UserApi, '/user/<user_id>')

    api.add_resource(ProductsApi, '/product/')
    api.add_resource(ProductApi, '/product/<product_id>')
