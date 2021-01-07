from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from operator import add
import numpy
from sqlalchemy import func
from flask_cors import CORS
from functools import reduce
from json import dumps

from server.models.Properties import Property, Price
from server.util.instances import db
from server.util.helpers import (no_of_Beds, get_areas, 
    get_years, get_types, get_average, get_average_type)

statRoute = Blueprint('statistics', __name__, url_prefix="/api/stats")


CORS(statRoute)

def prices (a):
    return a.amount


@statRoute.route('/all-average/<int:bed>', methods=['GET'])
def avarage_rent(bed):
    areas = get_areas()
    allAverage = dict(ikoyi=[], vi=[])
    years = get_years()
    
    for area in areas:
        yearAve = []
        for year in years:
            yearAve.append(get_average(year, area, bed))
        
        allAverage.update({area: yearAve})


    return jsonify({'data': allAverage, 'msg': 'success'}), 200


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

    count1 = len(props)
    count2 = len(propCom)


    if count1 > 0:
        stats[area] = list(numpy.floor_divide(stats[area],count1))
    if count2 > 0:
        stats[comarea] = list(numpy.floor_divide(stats[comarea],count2))
    
    return jsonify({'data': stats, 'msg': 'success'}), 200


@statRoute.route('/<path:area>')
def area_stats(area):
    beds = no_of_Beds()
    allAverage = dict()
    years = get_years()
    aptType = request.args.get('type','flat')
    
    for bed in beds:
        yearAve = []
        for year in years:
            yearAve.append(get_average_type(year, area, bed, aptType))
        
        allAverage.update({bed: yearAve})


    return jsonify({'data': allAverage, 'msg': 'success'}), 200


@statRoute.route('/minmax/<path:area>')
def min_max(area):
    beds = no_of_Beds()
    year = get_years()[-1]
    type = request.args.get('type','flat')
    result = dict()

    for bed in beds:
        prices = Price.query.filter_by(year=year).join(Price.property).filter(Property.bedrooms==bed, Property.type == type, Property.area == area).all()
        if(len(prices) > 0):
            max = reduce(lambda acc, next: acc if acc >= next else next, prices)
            min = reduce(lambda acc, next: acc if acc <= next else next, prices)

            result[bed] = dict(max=max.property,min=min.property)

    

    return jsonify({'data': result, 'msg': 'success'}), 200

@statRoute.route('/types/<path:area>')
def type_stat(area):
    
    total = dict()
    properties = Property.query.filter_by(area=area.lower()).all()

    for prop in properties:
        if prop.type in total:
            total[prop.type] = total[prop.type] + 1
        else:
            total[prop.type] = 1

    return jsonify({'data': total, 'msg': 'success'}), 200
