from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from operator import add
import numpy
from sqlalchemy import func
from flask_cors import CORS

from server.models.Properties import Property, Price
from server.util.instances import db

searchRoute = Blueprint('search', __name__, url_prefix="/api")


CORS(searchRoute)


@searchRoute.route('/search')
def compare():
    keyword = request.args.get('keyword')
    
    prop = Property.query.filter_by(
                                    area=keyword, 
                                    bedrooms=keyword, 
                                    type=keyword,
                                    name=keyword,
                                    facilities=keyword,
                                    address=keyword,
                                    serv_charge=keyword,
                                    sale_price=keyword
                                ).order_by(func.random()).first()
    
    return jsonify({'property': prop, 'msg': 'success'}), 200

    