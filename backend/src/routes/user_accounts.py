from flask import Response, Blueprint, jsonify, request

from src.services.user_accounts_service import (
    change_user_password,
    create_user,
    delete_user,
    login_user,
)

user_accounts_bp = Blueprint("user_accounts", __name__)

@user_accounts_bp.route("/register", methods=["POST"])
def register() -> Response:
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400
    
    if "username" not in data or "email" not in data or "password" not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    result, status = create_user(data['username'], data['email'], data['password'])
    return jsonify(result), status

@user_accounts_bp.route("/login", methods=["POST"])
def login() -> Response:
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400
    if "username" not in data:
        return jsonify({'error': 'Missing username'}), 400
    
    if "password" not in data:
        return jsonify({'error': 'Missing password'}), 400
    
    result, status = login_user(data['username'], data['password'])
    return jsonify(result), status

@user_accounts_bp.route("/change-password", methods=["POST"])
def change_password() -> Response:
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400
    if "username" not in data:
        return jsonify({'error': 'Missing username'}), 400
    if "password" not in data:
        return jsonify({'error': 'Missing password'}), 400
    if "new_password" not in data:
        return jsonify({'error': 'Missing new password'}), 400
    
    result, status = change_user_password(data['username'], data['password'], data['new_password'])
    return jsonify(result), status

@user_accounts_bp.route("/delete-user", methods=["POST"])
def delete_user_route() -> Response:
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400
    if "username" not in data:
        return jsonify({'error': 'Missing username'}), 400
    if "password" not in data:
        return jsonify({'error': 'Missing password'}), 400
    
    result, status = delete_user(data['username'], data['password'])
    return jsonify(result), status