from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from operator import add
import numpy
from sqlalchemy import func
from flask_cors import CORS

from server.models.Properties import Property, Price
from server.util.instances import db

statRoute = Blueprint('statistics', __name__, url_prefix="/api/stats")


CORS(statRoute)

def prices (a):
    return a.amount


@statRoute.route('/all-average/<int:bed>', methods=['GET'])
def avarage_rent(bed):
    properties = Property.query.filter_by(bedrooms=bed).all()
    stats = {'lekki': [0,0,0,0,0], 'vi': [0,0,0,0,0], 'ikoyi': [0,0,0,0,0], 'oniru': [0,0,0,0,0]}

    for prop in properties:
        price = list(map(prices,prop.rents))
        stats[prop.area] = list(map(add,stats[prop.area],price))

    countLekki = properties = Property.query.filter_by(area='lekki').count()
    countVi = properties = Property.query.filter_by(area='vi').count()
    countIkoyi = properties = Property.query.filter_by(area='ikoyi').count()
    countOniru = properties = Property.query.filter_by(area='oniru').count()

    if countLekki > 0:
        stats['lekki'] = list(numpy.array(stats['lekki'])/countLekki)
    if countVi > 0:
        stats['vi'] = list(numpy.array(stats['vi'])/countVi)
    if countIkoyi > 0:
        stats['ikoyi'] = list(numpy.array(stats['ikoyi'])/countIkoyi)
    if countOniru > 0:
        stats['oniru'] = list(numpy.array(stats['oniru'])/countOniru)  
    
    return jsonify({'data': stats, 'msg': 'success'}), 200


@statRoute.route('/compare')
def compare():
    bed = request.args.get('bed')
    comarea = request.args.get('comarea')
    prop = Property.query.filter_by(area=comarea, bedrooms=bed).order_by(func.random()).first()
    
    return jsonify({'data': prop, 'msg': 'success'}), 200

    