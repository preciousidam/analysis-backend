from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func, or_
from flask_cors import CORS

from server.models.Report import Report
from server.util.instances import db
from server.util.helpers import findAll


reportRoute = Blueprint('reports', __name__, url_prefix='/api/reports')

CORS(reportRoute)

@reportRoute.route('/')
def index():
    name = request.args.get('q')
    
    reports = Report.query.order_by(Report.updated_at.desc())
    reports = reports.filter(Report.title.ilike(f'%{name}%')).all()
   
    return jsonify({'data': reports, 'msg': 'success'}), 200