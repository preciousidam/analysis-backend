from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from operator import add
import numpy
from sqlalchemy import func, or_
from flask_cors import CORS

from server.models.Properties import Property, Price
from server.util.instances import db

searchRoute = Blueprint('search', __name__, url_prefix="/api")


CORS(searchRoute)


@searchRoute.route('/search')
def compare():
    keyword = request.args.get('keyword')
    
    prop = Property.query.filter(or_(Property.area.ilike(f'%{keyword}%'),
        Property.state.ilike(f'%{keyword}%'), Property.bedrooms.ilike(f'%{keyword}%'),
        Property.facilities.ilike(f'%{keyword}%'),Property.name.ilike(f'%{keyword}%'),
    )).order_by(func.random()).all()
    
    return jsonify({'property': prop, 'msg': 'success'}), 200

    