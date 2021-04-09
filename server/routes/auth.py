from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (create_access_token, 
    get_jwt_claims, jwt_refresh_token_required, 
    create_refresh_token, get_jwt_identity, jwt_required
)
from datetime import timedelta
from flask_cors import CORS
from flask_mail import Message
from threading import Thread

from server.util.instances import jwt
from server.models.User import User, Role, UserRole, ResetToken
from server.util.instances import db, mail


authRoute = Blueprint('auth', __name__, url_prefix='/api/auth')

CORS(authRoute)

@authRoute.before_request
def create_db():
    db.create_all()
    db.session.commit()

@jwt.user_claims_loader
def add_details_to_token(identity):
    userRole = UserRole.query.filter_by(user_id=identity.get('id')).first()
    role = Role.query.filter_by(id=userRole.role_id).first()
    return role.json()

@authRoute.route('/')
def create():
    return ''

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

    if user.is_active is False:
        return {'status': 'error', 'msg': 'This account is in-active, please contact support'}, 401

    expires = timedelta(days=7)
    access_token = create_access_token(identity=user.json(), expires_delta=expires)
    refresh_token = create_refresh_token(identity=user.json())
    return jsonify({'status': 'success', 'msg': 'Login Successful', 'token':access_token, 'refreshToken': refresh_token, 'user': user}), 200


@authRoute.route('/register', methods=['POST'])
def register():
    
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    phone = request.json.get('phone', None)
    username = request.json.get('username', None)
    name = request.json.get('name', None)

    if not email:
        return {'status': 'error', 'msg': 'Email not provided'}, 400
    
    if not password:
        return {'status': 'error', 'msg': 'Password not provided'}, 400

    if not phone:
        return {'status': 'error', 'msg': 'Email not provided'}, 400
    
    if not name:
        return {'status': 'error', 'msg': 'Password not provided'}, 400

    user = User.query.filter_by(email=email.lower()).first()

    if user:
        return {'status': 'error', 'msg': 'User with this email already exist. Please login'}, 400


    user = User(phone=phone, name=name, email=email, username=username)
    user.hashPassword(password=password)
    db.session.add(user)
    db.session.commit()

    mail = NewUserMail(user.name, user.email)
    mail.create_mail()
    mail = SupportNewUserMail(user.name, user.email)
    mail.create_mail()
    
    return jsonify({'status': 'success', 'msg': 'Account created successful'}), 200


@authRoute.route('/request-password-reset', methods=['POST'])
@jwt_required
def passwordReset():
    
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    password_new = request.json.get('password_new', None)

    if not email:
        return {'status': 'error', 'msg': 'Email not provided'}, 400


    user = User.query.filter_by(email=email.lower()).first()

    if user is None:
        return {'status': 'error', 'msg': 'No user with this email, please check details and try again'}, 401
    
    if user.checkPassword(password) is False:
        return {'status': 'error', 'msg': 'Invalid Current Password, please check details and try again'}, 401
    
    user.hashPassword(password_new)
    db.session.commit()

    return jsonify({'status': 'success', 'msg': 'Password change successful'}), 200

@authRoute.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    
    if not email:
        return {'status': 'error', 'msg': 'Email not provided'}, 400

    reset = ResetToken.query.filter_by(email=email).first()
    
    if not reset:

        reset = ResetToken(email=email)
        db.session.add(reset)
        db.session.commit()
    else:
        reset.updateToken()
        db.session.commit()

    mail = ResetMail(email, reset.get_token())
    mail.create_mail()

    return jsonify({'status': 'success', 'msg': 'Please check your mail for how to reset password'}), 200


@authRoute.route('/forgot-password/<path:token>', methods=['POST'])
def forgot_password_token(token):
    password = request.json.get('password')
    reset = ResetToken.query.filter_by(token=token).first()

    if not reset:
        return jsonify({'status': 'error', 'msg': 'reset link expired. please request new link'}), 400
    

    user = User.query.filter_by(email=reset.email).first()
    user.hashPassword(password)
    db.session.commit()

    mail = ResetSuccessfulMail(user.email)
    mail.create_mail()

    return jsonify({'status': 'success', 'msg': 'password reset successful, please login with new password'}), 200


@authRoute.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    expires = timedelta(days=7)
    ret = {
        'token': create_access_token(identity=current_user, expires_delta=expires)
    }
    return jsonify(ret), 200



class ResetMail():

    def __init__(self, email, token):
        self.subject = "Password Reset"
        self.email = email
        self.token = token
        self.body = f'Hi,\n You requested a password reset, please use the link below to reset your password\n https://napims.cortts.com/reset-password/{self.token} \n\n please ignore if you are not the one that initiated this.'

    def create_mail(self):
        app = current_app._get_current_object()
        
        msg = Message(
            subject=self.subject, 
            recipients=[self.email],
            body=self.body
        )
        thr = Thread(target=self.send_mail, args=[app,msg])
        thr.start()

        
    def send_mail(self, app, msg):
        with app.app_context():
            mail.send(msg)

class ResetSuccessfulMail():
    def __init__(self, email):
        self.subject = "Password Reset"
        self.email = email
        self.body = f'Hi,\n Your password has been reset, click this link to login to your account.\n https://napims.cortts.com \n\n Thank you.'

    def create_mail(self):
        app = current_app._get_current_object()
        
        msg = Message(
            subject=self.subject, 
            recipients=[self.email],
            body=self.body
        )
        thr = Thread(target=self.send_mail, args=[app,msg])
        thr.start()

        
    def send_mail(self, app, msg):
        with app.app_context():
            mail.send(msg)


class SupportNewUserMail():
    def __init__(self, name, email):
        self.subject = "New user account"
        self.email = 'napims.support@cortts.com'
        self.body = f'Hi Support,\n A new account was created with details.\n\tEmail: {email}\n\tName: {name}\n\n\r Please confirm user identity in order to enable us authorize access.\n\n Thank you.'

    def create_mail(self):
        app = current_app._get_current_object()
        
        msg = Message(
            subject=self.subject, 
            recipients=[self.email],
            body=self.body
        )
        thr = Thread(target=self.send_mail, args=[app,msg])
        thr.start()

        
    def send_mail(self, app, msg):
        with app.app_context():
            mail.send(msg)
    

class NewUserMail():
    def __init__(self, name, email):
        self.subject = "New user account"
        self.email = email
        self.body = f'Hi {name},\n\n Thank you for creating an account. Your account will remain inactive while we verify your identity.\n\n You will get an email confirming your account activation once your identity has been confirmed.\n\n To contact us for further support, please send us an email via support.napims@cortts.com\n\n Best regards.\nNAPIMS Team'

    def create_mail(self):
        app = current_app._get_current_object()
        
        msg = Message(
            subject=self.subject, 
            recipients=[self.email],
            body=self.body
        )
        thr = Thread(target=self.send_mail, args=[app,msg])
        thr.start()

        
    def send_mail(self, app, msg):
        with app.app_context():
            mail.send(msg)