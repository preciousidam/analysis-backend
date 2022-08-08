from sqlalchemy import func, or_
from functools import reduce
import numpy as np


from server.models.Properties import Property, Price
from server.util.instances import db


class AreaSet:
    def __init__(self) -> None:
        self.items = list()

    def add(self, item):
        contained = any(item['area'] == node['area'] for node in self.items)

        if contained:
            return

        self.items.append(item)

    def all(self):
        return self.items


def no_of_Beds():
    properties = Property.query.all()
    dst = set()

    for prop in properties:
        dst.add(prop.bedrooms)

    return list(dst)


def get_areas():
    properties = Property.query.all()
    dst = AreaSet()

    for prop in properties:
        dst.add(dict(area=prop.area, state=prop.state))

    return dst.all()


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


def findAll(q, type, page):
    per_page = 10
    prop = Property.query.filter_by(type=type)\
        .filter(or_(Property.area.ilike(f'%{q}%'), Property.name.ilike(f'%{q}%')))

    total = prop.count()

    return prop.paginate(page, per_page, error_out=False).items, total


def get_average_type(year, area, bed, type, is_comm):
    prices = None
    priceQuery = Price.query.filter_by(year=year).join(Price.property)
    if is_comm == 'true':
        prices = np.array(priceQuery.filter(
            Property.bedrooms == bed, Property.type == type, Property.area == area, Property.is_commercial == True).all())
    elif is_comm == 'False':
        prices = np.array(priceQuery.filter(
            Property.bedrooms == bed, Property.type == type, Property.area == area, or_(Property.is_commercial == False, Property.is_commercial == None)).all())
    else:
        prices = np.array(priceQuery.filter(
            Property.bedrooms == bed, Property.type == type, Property.area == area).all())

    sumTotal = reduce(lambda acc, a: acc + a.amount, prices, 0)

    '''if np.size(prices) > 0:
        return sumTotal/np.size(prices)'''
    return sumTotal/(np.size(prices) if np.size(prices) else 1)


def get_average(year, area, bed, comm_type):
    values = Price.query.filter_by(year=year).join(Price.property)
    if comm_type == 'commercial':
        values = values.filter(Property.is_commercial == True)
    elif comm_type == 'non-commercial':
        values = values.filter(
            or_(Property.is_commercial == False, Property.is_commercial == None))
    prices = np.array(values.filter(Property.bedrooms ==
                      bed, Property.area == area).all())

    sumTotal = reduce(lambda acc, a: acc + a.amount, prices, 0)

    return sumTotal/(np.size(prices) if np.size(prices) else 1)
