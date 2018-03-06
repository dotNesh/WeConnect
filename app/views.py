from flask import Flask, jsonify,request,make_response
from app.models import User, Business, Reviews
from werkzeug.security import check_password_hash
from app import app


@app.route('/api/v1/auth/register',methods=['POST']) 
def register_user():
    user_data = request.get_json()
    email = user_data.get('email')
    username = user_data.get('username')
    password = user_data.get('password')

    person = User.users.items()
    existing_user = {k:v for k, v in person if user_data['email'] in v['email']}
    if existing_user:
        return jsonify({'message': 'Account is already registered'})
    
    new_person = User(email, username, password)
    new_person.create_user()
    return jsonify({'message':'User Succesfully Registered'}), 201