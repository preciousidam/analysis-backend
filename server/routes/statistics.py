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
    print(a.year)
    return a.amount


@statRoute.route('/all-average/<int:bed>', methods=['GET'])
def avarage_rent(bed):
    properties = Property.query.filter_by(bedrooms=bed).all()
    stats = {'lekki': [0,0,0,0,0], 'vi': [0,0,0,0,0], 'ikoyi': [0,0,0,0,0], 'oniru': [0,0,0,0,0]}

    for prop in properties:
        price = list(map(prices,prop.rents))
        price = numpy.pad(price, pad_width=(5-len(price),0))
        stats[prop.area] = list(map(add,stats[prop.area],price))

    countLekki = Property.query.filter_by(area='lekki').count()
    countVi = Property.query.filter_by(area='vi').count()
    countIkoyi = Property.query.filter_by(area='ikoyi').count()
    countOniru = Property.query.filter_by(area='oniru').count()

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
    area = request.args.get('area')
    typeOf = request.args.get('type')
    comarea = request.args.get('comarea')
    props = Property.query.filter_by(area=area, bedrooms=bed, type=typeOf).all()
    propCom = Property.query.filter_by(area=comarea, bedrooms=bed, type=typeOf).all()
    stats = {area: [0,0,0,0,0], comarea: [0,0,0,0,0]}
    
    for prop in props:
        price = list(map(prices,prop.rents))
        price = numpy.pad(price, pad_width=(5-len(price),0))
        stats[area] = list(map(add, stats[area],price))
    
    for prop in propCom:
        price = list(map(prices,prop.rents))
        price = numpy.pad(price, pad_width=(5-len(price),0))
        stats[comarea] = list(map(add,stats[comarea],price))

    count1 = Property.query.filter_by(area=area).count()
    count2 = Property.query.filter_by(area=comarea).count()


    if count1 > 0:
        stats[area] = list(numpy.array(stats[area])/count1)
    if count2 > 0:
        stats[comarea] = list(numpy.array(stats[comarea])/count2)
    
    return jsonify({'data': stats, 'msg': 'success'}), 200

    