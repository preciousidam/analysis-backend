from sqlalchemy import func, or_
from functools import reduce
import numpy as np


from server.models.Properties import Property, Price
from server.util.instances import db


def no_of_Beds():
    properties = Property.query.all()
    dst = set()

    for prop in properties:
        dst.add(prop.bedrooms)

    return list(dst)


def get_areas():
    properties = Property.query.all()
    dst = set()

    for prop in properties:
        dst.add(prop.area)

    return list(dst)

def get_years():
    properties = Property.query.all()
    dst = set()

    for prop in properties:
        for rent in prop.rents:
            dst.add(rent.year)

    return list(dst)

def get_types():
    properties = Property.query.all()
    dst = set()

    for prop in properties:
        dst.add(prop.type)

    return list(dst)


def findAll(q,type, page):
    per_page=10
    prop = Property.query.filter_by(type=type)\
        .filter(or_(Property.area.ilike(f'%{q}%'),Property.name.ilike(f'%{q}%')))

    total = prop.count()     
    
    return prop.paginate(page,per_page,error_out=False).items, total


def get_average_type(year, area, bed, type):

    prices = np.array(Price.query.filter_by(year=year).join(Price.property).filter(Property.bedrooms==bed, Property.type == type, Property.area == area).all())
    
    sumTotal = reduce(lambda acc, a: acc + a.amount, prices, 0)
    
    if np.size(prices) > 0:
        return sumTotal/np.size(prices)
    return 0


def get_average(year, area, bed):

    prices = np.array(Price.query.filter_by(year=year).join(Price.property).filter(Property.bedrooms==bed, Property.area == area).all())
    
    sumTotal = reduce(lambda acc, a: acc + a.amount, prices, 0)
    

    return sumTotal/np.size(prices)

    
    