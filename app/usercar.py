from flask import Flask,jsonify,request
from app.model import User, UserCar, UserBook
from app.serializer import UserSchema, UpdateUserSchema
from app_init.app_factory import create_app
from http import HTTPStatus
from marshmallow import ValidationError
import requests, os

settings_name = os.getenv("settings")
app = create_app(settings_name)

#CREATE USER

@app.route('/user', methods=["POST"])
def create_user():
    user_info = request.get_json()
    user = User.query.filter_by(email=user_info.get("email")).first()
    if user:
        return jsonify(msg="exists"),HTTPStatus.BAD_REQUEST
    try:
        user = UserSchema().load(user_info)
        response = requests.get(f"http://127.0.0.1:5002/car/{user_info.get('car_id')}")
        response_book = requests.get(f"http://127.0.0.1:5003/books/{user_info.get('book_id')}")
        if user:
            user.generate_password()
            user.save_db()
            if response.status_code == 200:
                user_car = UserCar()
                user_car.user_id = user.id
                user_car.car_id = response.json().get('id')
                user_car.save_db()
                user_book = UserBook()
                user_book.user_id = user.id
                user_book.book_id = response_book.json().get('id')
                user_book.save_db()
        else:
            return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND

    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    return UserSchema(exclude=["password"]).jsonify(user),HTTPStatus.OK

# CREATE CAR

@app.route('/user/<int:id>/car', methods=["POST"])
def create_car(id):
    user = User.query.get(id)
    if user:
        car_id = request.json.get('car_id')
        if car_id:
            response = requests.get(f"http://127.0.0.1:5002/car/{car_id}")
            if response.status_code == 200:
                car = UserCar()
                car.user_id = user.id
                car.car_id = car_id
                car.save_db()                
                return jsonify(msg="OK"),HTTPStatus.OK
        return jsonify(msg="Car not found")
    return jsonify(msg="User not found"),HTTPStatus.NOT_FOUND     


#CREATE BOOK

@app.route('/user/<int:id>/books', methods=["POST"])
def create_book(id):
    user = User.query.get(id)
    if user:
        user_book = request.json.get("book_id")
        if user_book:
            response = requests.get(f"http://127.0.0.1:5003/books/{user_book}")
            if response.status_code == 200:
                book_info = UserBook()
                book_info.user_id = user.id
                book_info.book_id = user_book
                book_info.save_db()
                return jsonify(msg="OK"),HTTPStatus.OK
        return jsonify(msg="Book not found"),HTTPStatus.NOT_FOUND
    return jsonify(msg="User not found"),HTTPStatus.NOT_FOUND




#READ ALL USER

@app.route('/user', methods=["GET"])
def get_all_user():
    user_info = User.query.all()
    temp=[]
    for user in user_info:
        user_car = UserCar.query.filter_by(user_id=user.id).all()
        user_book = UserBook.query.filter_by(user_id=user.id).all()
        data_schema = UserSchema().dump(user)
        data_schema.pop("password")
        data_schema["car_info"]=[]
        data_schema["book_info"]=[]       
        if user_car:
            for car in user_car:
                response = requests.get(f"http://127.0.0.1:5002/car/{car.car_id}")
                if response.status_code == 200:
                    data_schema["car_info"].append(response.json())   
        if user_book:
            for book in user_book:
                response = requests.get(f"http://127.0.0.1:5003/books/{book.book_id}")
                if response.status_code == 200:
                    data_schema["book_info"].append(response.json())                
        temp.append(data_schema)        
    return jsonify(temp),HTTPStatus.OK


    # return UserSchema(exclude=["password"]).jsonify(user_info,many=True),HTTPStatus.OK

#READ USER 

@app.route('/user/<int:id>',methods=["GET"])
def get_user(id):
    user_info = User.query.get(id)
    temp_book=[]
    temp_car=[]
    if user_info:
        user_car = UserCar.query.filter_by(user_id=user_info.id).all()
        user_book = UserBook.query.filter_by(user_id=user_info.id).all()
        if user_car:                      
            for car in user_car:              
                response = requests.get(f"http://127.0.0.1:5002/car/{car.car_id}")
                if response.status_code == 200:
                    temp_car.append(response.json())     
        if user_book:          
            for book in user_book:
                response = requests.get(f"http://127.0.0.1:5003/books/{book.book_id}")
                if response.status_code == 200:
                    temp_book.append(response.json())
        data = UserSchema().dump(user_info)
        data["car_info"]=temp_car
        data["book_info"]=temp_book
        data.pop("password") 
        return jsonify(data),HTTPStatus.OK
        # return UserSchema(exclude=["password"]).jsonify(user_info),HTTPStatus.OK
    return jsonify(msg="user not found"),HTTPStatus.NOT_FOUND


#DELETE USER

@app.route('/user/<int:id>',methods=["DELETE"])
def delete_user(id):
    user_info = User.query.get(id)
    if user_info:
        user_info.delete_from_db()
        return jsonify(msg="User deleted"),HTTPStatus.OK
    return jsonify(msg="User not found"),HTTPStatus.NOT_FOUND

# DELETE CAR

@app.route('/user/<int:id>/car/<int:car_id>', methods=["DELETE"])
def delete_users_car(id,car_id):
    user_car = UserCar.query.filter_by(user_id=id, car_id=car_id).first()
    if user_car:
        user_car.delete_from_db()
        return jsonify(msg="OK"),HTTPStatus.OK
    return jsonify(msg="user or car not found"),HTTPStatus.NOT_FOUND

#UPDATE USER INFO

@app.route('/user/<int:id>', methods=["PUT"])
def update_user_info(id):
    user = User.query.get(id)
    if user:
        new_user = request.get_json()
        new_user = UpdateUserSchema().load(new_user)
        user.update_db(**new_user)
        return UserSchema().jsonify(user),HTTPStatus.OK
    return jsonify(msg="User not found"),HTTPStatus.NOT_FOUND


#UPDATE CAR

@app.route('/users/<int:id>/cars/<int:car_id>', methods=["PUT"])
def updete_car_info(id, car_id):
    user_car = UserCar.query.filter_by(user_id=id, car_id=car_id).first()
    if user_car:
        new_car = request.get_json()
        if new_car.get("new_car_id"):
            response = requests.get(f"http://127.0.0.1:5002/car/{new_car.get('new_car_id')}")
            if response.status_code == 200:
                car_dict={
                    "car_id":new_car.get("new_car_id")
                }
                user_car.update_db(**car_dict)
                return jsonify(msg="OK"),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND

#UPDATE BOOK

@app.route('/users/<int:id>/books/<int:book_id>', methods=["PUT"])
def update_book(id, book_id):
    book = UserBook.query.filter_by(user_id=id, book_id=book_id).first()
    if book:
        new_book = request.get_json()
        if new_book.get("new_book_id"):
            response = requests.get(f"http://127.0.0.1:5003/books/{new_book.get('new_book_id')}")
            if response.status_code == 200:
                book_dict = {
                    "book_id":new_book.get("new_book_id")
                }
                book.update_db(**book_dict)
                return jsonify(msg="OK"),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND

