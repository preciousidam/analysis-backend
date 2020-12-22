from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from operator import add
import numpy
from sqlalchemy import func
from flask_cors import CORS

from server.models.Properties import Property, Price
from server.util.instances import db
from server.util.helpers import no_of_Beds, get_areas, get_years

statRoute = Blueprint('statistics', __name__, url_prefix="/api/stats")


CORS(statRoute)

def prices (a):
    return a.amount


@statRoute.route('/all-average/<int:bed>', methods=['GET'])
def avarage_rent(bed):
    areas = get_areas()
    allAverage = dict()
    years = get_years()
    
    for area in areas:
        properties = Property.query.filter_by(area=area,bedrooms=bed).all()
        total = len(properties)
        initial_prices = numpy.pad([], pad_width=(len(years)-len([]),0))
        allAverage.update({area:initial_prices})

        for prop in properties:
            price = list(map(prices,prop.rents))
            price = numpy.pad(price, pad_width=(len(years)-len(price),0))
            initial_prices = list(map(add,initial_prices,price))
        
        if total > 0:
            allAverage.update({area:list(numpy.floor_divide(initial_prices,total))})


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
    
    for bed in beds:
        properties = Property.query.filter_by(area=area,bedrooms=bed).all()
        total = len(properties)
        initial_prices = numpy.pad([], pad_width=(len(years)-len([]),0))
        allAverage.update({bed:initial_prices})

        for prop in properties:
            price = list(map(prices,prop.rents))
            price = numpy.pad(price, pad_width=(len(years)-len(price),0))
            initial_prices = list(map(add,initial_prices,price))

        if total > 0:
            allAverage.update({bed:list(numpy.floor_divide(initial_prices,total))})


    return jsonify({'data': allAverage, 'msg': 'success'}), 200
