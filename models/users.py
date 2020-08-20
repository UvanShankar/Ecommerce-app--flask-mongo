# mongo-engine packages
from mongoengine import (Document,
                         EmbeddedDocument,
                         EmbeddedDocumentField,
                         ListField,
                         StringField,
                         EmailField,
                         BooleanField,
                         ReferenceField)

# flask packages
from flask_bcrypt import generate_password_hash, check_password_hash

# project resources
from models.products import Products

# external packages
import re

class Users(Document):
    """
    Template for a mongoengine document, which represents a user.
    Password is automatically hashed before saving.

    :param email: unique required email-string value
    :param password: required string value, longer than 6 characters
    :param access: Access object
    :param fav_meals: List of Meal objects
    :param username: option unique string username
    :param phone: optional string phone-number, must be valid via regex

    :Example:

    >>> import mongoengine
    >>> from app import default_config

    >>> mongoengine.connect(**default_config['MONGODB_SETTINGS'])
    MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True, read_preference=Primary())

    # Create test user
    >>> new_user = Users(email="spam@ham-and-eggs.com", password="hunter2", access={"admin": True})
    >>> new_user.save()
    >>> new_user.username = "spammy"
    >>> new_user.save()

    # Remove test user
    >>> new_user.delete()
    """

    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=6, regex=None)
    username = StringField(unique=False)

    def generate_pw_hash(self):
        self.password = generate_password_hash(password=self.password).decode('utf-8')
    # Use documentation from BCrypt for password hashing
    generate_pw_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, password: str) -> bool:
        return check_password_hash(pw_hash=self.password, password=password)
    # Use documentation from BCrypt for password hashing
    check_pw_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        self.generate_pw_hash()
        super(Users, self).save(*args, **kwargs)
