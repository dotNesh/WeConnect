from flask import Flask, jsonify,request,make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity
from app.models import User, Business, Reviews
from werkzeug.security import check_password_hash
from app import app

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


@app.route('/api/v1/auth/register',methods=['POST']) 
def register_user():
    user_data = request.get_json()
    email = user_data.get('email')
    username = user_data.get('username')
    password = user_data.get('password')

    person = User.users.items()
    existing_user = {k:v for k, v in person if user_data['email'] in v['email']}
    if existing_user:
        return jsonify({'message': 'Account is already existing.'}), 404
    
    new_person = User(email, username, password)
    new_person.create_user()
    return jsonify({'message':'User Succesfully Registered'}), 201

@app.route('/api/v1/auth/login', methods=['POST'])   
def login():
    
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
 
    login_data = request.get_json()
    username = login_data.get('username')
    password = login_data.get('password')

    person = User.users.items()
    existing_user = {k:v for k, v in person if login_data['username'] in v['username']}
    if existing_user:
       valid_user = [v for v in existing_user.values() if check_password_hash(v['password'],password)]
       if valid_user:
           access_token = create_access_token(identity=username)
           if access_token:
                    response = {
                        'message': 'You are logged in successfully',
                        'access_token': access_token
                    }
                    return make_response(jsonify(response)), 200
       else:
            return jsonify({'message': 'Wrong password'}), 400
    else:
        return jsonify({'message': 'Non-existent user. Try signing up'}), 404    