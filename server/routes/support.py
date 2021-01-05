from flask import Blueprint, jsonify, request, render_template, current_app
from flask_jwt_extended import jwt_required
from operator import add
import numpy
from sqlalchemy import func, or_
from flask_cors import CORS
from flask_mail import Message
from threading import Thread

from server.models.Properties import Property, Price
from server.util.instances import db, mail
from server.util.helpers import get_years, get_areas, no_of_Beds, get_types

supportRoute = Blueprint('support', __name__, url_prefix="/api")


CORS(supportRoute)


@supportRoute.route('/support/contact-us', methods=['POST'])
@jwt_required
def contact_us():
    email = request.json.get('email', None)
    name = request.json.get('name', None)
    subject = request.json.get('subject', None)
    message = request.json.get('message', None)

    if not name:
        return jsonify({'msg': 'Missing name', 'status': 'error'}), 400

    if not email:
        return jsonify({'msg': 'Missing email', 'status': 'error'}), 400

    if not subject:
        return jsonify({'msg': 'Missing subject', 'status': 'error'}), 400

    if not message:
        return jsonify({'msg': 'Missing message', 'status': 'error'}), 400

   
    sMail = SupportMail(email,name,subject,message)
    sMail.create_mail()
    
    
    return jsonify({'msg': 'Message Submitted', 'status': 'success'}), 201

@supportRoute.route('/areas')
def allArea():
    return jsonify({'data': get_areas(), 'status': 'success'}), 200

@supportRoute.route('/bedroom')
def allBeds():
    return jsonify({'data': no_of_Beds(), 'status': 'success'}), 200

@supportRoute.route('/years')
def allYears():
    return jsonify({'data': get_years(), 'status': 'success'}), 200

@supportRoute.route('/types')
def allTypes():
    return jsonify({'data': get_types(), 'status': 'success'}), 200



class SupportMail():

    def __init__(self, email, name, subject, message):
        self.name = name
        self.subject = subject
        self.message = message
        self.email = email

    def create_mail(self):
        app = current_app._get_current_object()
        
        msg = Message(
            sender=(self.name, self.email),
            subject=self.subject, 
            recipients=['napims.support@cortts.com'],
            body=f'{self.message}'
        )
        thr = Thread(target=self.send_mail, args=[app,msg])
        thr.start()

        
    def send_mail(self, app, msg):
        with app.app_context():
            mail.send(msg)