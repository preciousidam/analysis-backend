from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, 
    get_jwt_claims, jwt_refresh_token_required, 
    create_refresh_token, get_jwt_identity
)
from datetime import timedelta

from server.util.instances import jwt
from server.models.User import User, Role
from server.util.instances import db


authRoute = Blueprint('auth', __name__, url_prefix='/api/auth')

@authRoute.before_request
def create_db():
    db.create_all()
    db.session.commit()

@jwt.user_claims_loader
def add_details_to_token(identity):
    role = Role.query.filter_by(id=identity.get('role')).first()
    return role.json()


@authRoute.route('/roles/<int:id>', methods=['GET'])
def get_roles(id):
    role = Role.query.filter_by(id=id).first()
    return jsonify({'data': role, 'msg': 'success'}), 200


@authRoute.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return {'status': 'error', 'msg': 'Email not provided'}, 400
    
    if not password:
        return {'status': 'error', 'msg': 'Password not provided'}, 400

    user = User.query.filter_by(email=email.lower()).first()

    if user is None:
        return {'status': 'error', 'msg': 'No user with this email, please check details and try again'}, 401

    if user.checkPassword(password) is False:
        return {'status': 'error', 'msg': 'Invalid Password, please check details and try again'}, 401

    expires = timedelta(days=7)
    access_token = create_access_token(identity=user.json(), expires_delta=expires)
    refresh_token = create_refresh_token(identity=user.json())
    return jsonify({'status': 'success', 'msg': 'Login Successful', 'token':access_token, 'refreshToken': refresh_token}), 200



@authRoute.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    expires = timedelta(days=7)
    ret = {
        'token': create_access_token(identity=current_user, expires_delta=expires)
    }
    return jsonify(ret), 200