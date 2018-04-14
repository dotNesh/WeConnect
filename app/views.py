'''views,py'''
from app import validate
from flask import jsonify, request, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
from app.models import User, Business, Reviews
from werkzeug.security import check_password_hash
from app import app

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECS'] = ['access']
jwt = JWTManager(app)
blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    '''Black listing'''
    jti = decrypted_token['jti']
    return jti in blacklist

@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    '''Route to register user'''
    data = request.get_json()
    for key in data:
        result = validate.empty(data[key])
        if result:
            return jsonify({'message': key + ' cannot be an empty string'}), 406
        else:
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')

    person = User.users.items()
    existing_email = {k:v for k, v in person if data['email'] in v['email']}
    existing_username = {k:v for k, v in person if data['username'] in v['username']}

    if existing_email:
        return jsonify({'message': 'Email already existing.'}), 409

    elif existing_username:
        return jsonify({'message': 'Username already existing.'}), 409
    else:
        new_person = User(email, username, password)
        new_person.create_user()
        return jsonify({'message':'User Succesfully Registered'}), 201

@app.route('/api/v1/auth/login', methods=['POST'])   
def login():
    '''Route to login'''
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    for key in data:
        result = validate.empty(data[key])
        if result:
            return jsonify({'message': key + ' cannot be an empty string'}), 406
        else:
            username = data.get('username')
            password = data.get('password')
    
    person = User.users.items()
    existing_user = {k:v for k, v in person if data['username'] in v['username']}
    if existing_user:
        valid_user = [v for v in existing_user.values() if check_password_hash(v['password'], password)]
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

@app.route('/api/v1/businesses', methods=['POST'])
@jwt_required
def register_business():
    '''Businesss registration route'''
    current_user = get_jwt_identity()
    data = request.get_json()
    for key in data:
        result = validate.empty(data[key])
        if result:
            return jsonify({'message': key + ' cannot be an empty string'}), 406
        else:
            business_name = data.get('business_name')
            category = data.get('category')
            location = data.get('location')
            description = data.get('description')

    biz = Business.business.items()
    existing_business = {k:v for k, v in biz if data['business_name'] in v['business_name']}

    if existing_business:
        return jsonify({"message":"Business name already exists"})
    else:
        new_biz = Business(business_name, category, location, description, current_user)
        new_biz.register_business()
        response = {'message': 'Business Successfully Registered',
                    'Registered by': current_user}
        return make_response(jsonify(response)), 201

@app.route('/api/v1/businesses',methods=['GET'])
def get_businesses():
    '''route to get all businesses'''
    #If GET method
    businesses = Business.get_all_businesses()
    return make_response(jsonify(businesses)), 200

@app.route('/api/v1/businesses/<int:business_id>', methods=['PUT', 'DELETE'])
@jwt_required
def one_business(business_id):
    '''Route for update and delete'''
    current_user = get_jwt_identity() #Current_user is username
    targetbusiness = Business.get_business(business_id)

    if request.method == 'DELETE':
        if targetbusiness:
            if current_user == targetbusiness['owner']:
                deletebusiness = Business.delete_business(business_id)
                return make_response(jsonify(deletebusiness)), 200
            else:
                return jsonify({'message':'You cannot delete a business that is not yours'}), 401
        else:
            return jsonify({'message':'Cannot Delete. Resourse Not Found'}), 404
    elif request.method == 'PUT':
        if targetbusiness:
            if current_user == targetbusiness['owner']:
                data = request.get_json()
                Business.update_business(business_id, data)
                return jsonify({'message':'Successfully Updated'}), 201
            else:
                return jsonify({'message':'You cannot update a business that is not yours'}), 401
        else:
            return jsonify({'message':'Cannot Update. Resource Not Found'}), 404

@app.route('/api/v1/businesses/<int:business_id>', methods=['GET'])
def get_a_business(business_id):
    '''route to get a business info'''
    targetbusiness = Business.get_business(business_id)
    if targetbusiness:
        return make_response(jsonify(targetbusiness)), 200
    else:
        return jsonify({'message':'Resource Not Found'}), 404

@app.route('/api/v1/businesses/<int:business_id>/reviews',methods=['POST'])   
@jwt_required
def reviews(business_id):
    '''Route to post reviews'''
    current_user = get_jwt_identity()
    if request.method == 'POST':
        review_data = request.get_json()
        title = review_data.get('title')
        description = review_data.get('description')
        new_review = Reviews(title, description)
        new_review.add_reviews()
        response = {
            'message': 'Review Posted',
            'Review by': current_user
            }
        return make_response(jsonify(response)), 201

@app.route('/api/v1/businesses/<int:business_id>/reviews',methods=['GET'])  
def get_reviews(business_id):
    '''Route to add a review'''
    return make_response(jsonify(Reviews.get_all_reviews())), 200

@app.route('/api/v1/auth/logout', methods=['POST'])
@jwt_required
def logout():
    '''Route to logut'''
    dump = get_raw_jwt()['jti']
    blacklist.add(dump)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/v1/auth/reset-password', methods=['POST'])
@jwt_required
def reset_password():
    '''Route to reset password'''
    current_user = get_jwt_identity()
    data = request.get_json()
    for key in data:
        result = validate.empty(data[key])
        if result:
            return jsonify({'message': key + ' cannot be an empty string'}), 406
    person = User.users.items()
    existing_username = {k:v for k, v in person if current_user in v['username']}
    valid_user = [v for v in existing_username.values() if check_password_hash(v['password'], data['old_password'])]
    if valid_user:
        User.reset_password(current_user, data)
        return jsonify({'message': 'Reset successful'}), 200
    else:
        return jsonify({'message': 'Wrong Password. Cannot reset. Forgotten password?'}), 401
        