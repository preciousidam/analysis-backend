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

@authRoute.route('/adduser')
def adduser():
    user = User(
        name='ebube',
        email='ebube@cortts.com',
        phone="08162300796",
        username="ebube",
        role=1
    )

    user.hashPassword('lilian01')
    db.session.add(user)
    db.session.commit()
    return 'user added'

@authRoute.route('/addrole')
def addrole():
    roleAdmin = Role(
        title="admin",
        permissions='read,write'
    )

    roleUser = Role(
        title="user",
    )
    
    db.session.add(roleAdmin)
    db.session.add(roleUser)
    db.session.commit()
    return 'roles added'



@authRoute.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return {'status': 'error', 'msg': 'Email not provided'}, 400
    
    if not password:
        return {'status': 'error', 'msg': 'Password not provided'}, 400

    user = User.query.filter_by(email=email).first()

    if user is None:
        return {'status': 'error', 'msg': 'No user with this email, please check details and try again'}, 401

    if user.checkPassword(password) is False:
        return {'status': 'error', 'msg': 'Invalid Password, please check details and try again'}, 401

    expires = timedelta(days=7)
    access_token = create_access_token(identity=user.json(), expires_delta=expires)
    refresh_token = create_refresh_token(identity=user.json())
    return jsonify({'status': 'success', 'msg': 'Login Successful', 'token':access_token, 'refreshToken': refresh_token}), 200



@authRoute.route('/create', methods=['POST'])
def create():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    phone = request.json.get('phone', None)
    name = request.json.get('name', None)
    role = request.json.get('role', None)

    if not email:
        return {'status': 'error', 'msg': 'Email not provided'}, 400
    
    if not password:
        return {'status': 'error', 'msg': 'Password not provided'}, 400

    if not name:
        return {'status': 'error', 'msg': 'Name not provided'}, 400
    
    if not phone:
        return {'status': 'error', 'msg': 'Phone number not provided'}, 400

    if not role:
        return {'status': 'error', 'msg': 'User role not provided'}, 400

    user = User.query.filter_by(email=email).first()

    if user is not None:
        return {'status': 'error', 'msg': 'Email address already exist! try login'}, 401

    try:
        user = User(
            name=name,
            email=email,
            phone=phone,
            username=email.split('@')[0],
            role=role
        )

        user.hashPassword(password)

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    except:
        return jsonify({'status': 'error', 'msg': 'Something happend cannot add user to database'}), 500
    #expires = timedelta(days=7)
    #access_token = create_access_token(identity=user.json(), expires_delta=expires)
    #refresh_token = create_refresh_token(identity=user.json())
    return jsonify({'status': 'success', 'msg': 'User Created Successfully'}), 200


@authRoute.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    expires = timedelta(days=7)
    ret = {
        'token': create_access_token(identity=current_user, expires_delta=expires)
    }
    return jsonify(ret), 200