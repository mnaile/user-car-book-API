from flask import Flask
from app.model import User
from extensions.extensions import ma
from marshmallow import fields,validate

class UserSchema(ma.SQLAlchemyAutoSchema):

    name = fields.String(required=True, validate=[validate.Length(min=2, max=30)])
    surname = fields.String(required=True, validate=[validate.Length(min=2, max=30)])
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[validate.Length(min=8, max=60)])
    car_id = fields.Integer()
    book_id = fields.Integer()

    class Meta:
        model = User
        load_instance = True

class UpdateUserSchema(ma.SQLAlchemySchema):

    name = fields.String(validate=[validate.Length(min=2, max=30)])
    surname = fields.String(validate=[validate.Length(min=2, max=30)])
    email = fields.Email()
    password = fields.String(validate=[validate.Length(min=8, max=60)])
    car_id = fields.Integer()
    book_id = fields.Integer()


