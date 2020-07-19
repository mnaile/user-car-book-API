from extensions.extensions import db
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__="User"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(),nullable=True)
    surname = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    password = db.Column(db.String(), nullable=True)

    def generate_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password_hash):
        return check_password_hash(self.password, password_hash)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_db(self, **kwargs):
        for key,val in kwargs.items():
            setattr(self, key, val)
        self.save_db()

    # def sereliazer(self):
    #     return {
    #         "name":self.name,
    #         "surname":self.surname
    #     }

class UserCar(db.Model):
    __tablename__="user_car"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id", ondelete='CASCADE'), nullable=False)
    car_id = db.Column(db.Integer, nullable=False)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_db(self, **kwargs):
        for key,val in kwargs.items():
            setattr(self, key, val)
        self.save_db()

class UserBook(db.Model):
    __tablename__="user_book"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id", ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_db(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save_db()






