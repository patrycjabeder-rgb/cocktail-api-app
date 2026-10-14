import re
from werkzeug.security import check_password_hash, generate_password_hash

from src.db import users_collection

def is_valid_password(password: str) -> bool:
    ''' Validate the password based on the following criteria:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit or special character from the set !@#$%^&*()-_=+[]{}|;:'",.<>?/`~'''
    
    if len(password) < 8:
        return 'Password must be at least 8 characters long'
    
    if not re.search(r'[A-Z]', password):
        return 'Password must contain at least one uppercase letter'
    
    if not re.search(r'[a-z]', password):
        return 'Password must contain at least one lowercase letter'
    
    if not re.search(r'[!@#$%^&*()\-\_=+\[\]{}|;:\'",.<>?/`~]', password) and not re.search(r'\d', password):
        return 'Password must contain at least one digit or special character'
    
    return True

def create_user(username: str, email: str, password: str) -> tuple:
    ''' Create a new user in the database.
    Takes:
        username: str, 
        email: str,
        and password: str 
    
    Returns a tuple (result, status_code).''' 

    if users_collection.find_one({'username': username}):
        return {'error': 'Username already taken'}, 400
    
    if users_collection.find_one({'email': email}):
        return {'error': 'Email already registered'}, 400
    
    # Check the validity of the password

    password_validation_result = is_valid_password(password)
    if password_validation_result is not True:
        return {'error': password_validation_result}, 400


    hashed_password = generate_password_hash(password)
    user = {
    'username': username,
    'email': email,
    'password_hash': hashed_password,
    'saved_cocktails': []
    }

    users_collection.insert_one(user)

    return {'message': 'User created successfully'}, 201

def login_user(username: str, password: str) -> tuple:
    ''' Authenticate a user.
    Takes:
        username: str,
        password: str
    Returns a tuple (result, status_code).'''

    user = users_collection.find_one({'username': username})
    if not user:
        return {'error': 'Invalid username or password'}, 401
    
    if not check_password_hash(user['password_hash'], password):
        return {'error': 'Invalid username or password'}, 401
    
    return {'message': 'Login successful', 'user_id': str(user['_id']), 'username': user['username']}, 200

def change_user_password(username, old_password, new_password):
    ''' Change the password for a user.
    Takes:
        username: str,
        old_password: str,
        new_password: str
    Returns a tuple (result, status_code).'''

    user = users_collection.find_one({'username': username})
    if not user:
        return {'error': 'User not found'}, 404 
   
    if not check_password_hash(user['password_hash'], old_password):
        return {'error': 'Old password is incorrect'}, 401
    # Check the validity of the new password
    if check_password_hash(user['password_hash'], new_password):
        return {'error': 'New password cannot be the same as the old password'}, 400
    
    password_validation_result = is_valid_password(new_password)
    if password_validation_result is not True:
        return {'error': password_validation_result}, 400
    
    # Update the user's password
    hashed_new_password = generate_password_hash(new_password)
    users_collection.update_one({'username': username}, {'$set': {'password_hash': hashed_new_password}})

    return {'message': 'Password changed successfully'}, 200

def delete_user(username: str, password: str) -> tuple:
    ''' Delete a user from the database.
    Takes:
        username: str
    Returns a tuple (result, status_code).'''
    user = users_collection.find_one({'username': username})
    if not user:
        return {'error': 'User not found'}, 404
    if not check_password_hash(user['password_hash'], password):
        return {'error': 'Incorrect password'}, 401

    result = users_collection.delete_one({'username': username})
    
    return {'message': 'User deleted successfully'}, 200