from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func, or_
from flask_cors import CORS

from server.models.Properties import Property, Price
from server.util.instances import db
from server.util.helpers import findAll


propertyRoute = Blueprint('properties', __name__, url_prefix='/api/properties')

CORS(propertyRoute)


@propertyRoute.before_request
def create_db():
    db.create_all()
    db.session.commit()


@propertyRoute.route('/', methods=['GET'])
def get_properties():
    properties = Property.query.order_by(Property.updated_at.desc()).all()
    return jsonify({'data': properties, 'msg': 'success'}), 200


@propertyRoute.route('/search', methods=['GET'])
def search_properties():
    q = request.args.get('q', '')
    type = request.args.get('type', '')
    page = int(request.args.get('page', 1), base=10)
    properties, total = findAll(q, type, page)
    return jsonify({'data': {'properties': properties, 'total': total}, 'msg': 'success'}), 200


@propertyRoute.route('/<path:area>', methods=['GET'])
def get_property_in_area(area):
    page = int(request.args.get('page', 1))

    q = request.args.get('q').lower()
    bed = request.args.get('bed')
    prop_type = request.args.get('prop_type')
    per_page = 10

    properties = Property.query.filter(
        or_(Property.name.ilike(f'%{q}%'))).filter_by(area=area.lower())

    if bed != '':
        properties = properties.filter_by(bedrooms=bed)

    if prop_type == 'commercial':
        properties = properties.filter_by(is_commercial=True)
    elif prop_type == 'non-commercial':
        properties = properties.filter(
            or_(Property.is_commercial == None, Property.is_commercial == False))

    propertyCount = properties.count()
    properties = properties.order_by(Property.updated_at.desc()).paginate(
        page, per_page, error_out=False).items

    return jsonify({'data': {'properties': properties, 'total': propertyCount}, 'msg': 'success'}), 200


@propertyRoute.route('/<path:area>/<int:propertyId>', methods=['GET'])
def get_property_by_id(area, propertyId):

    property = Property.query.filter_by(area=area, id=propertyId).first()

    return jsonify({'data': property, 'msg': 'success'}), 200


@propertyRoute.route('/delete', methods=['POST'])
@jwt_required
def delete_property():
    if request.method == 'POST':
        id = request.json.get('id', None)

    if not id:
        return jsonify({'msg': 'Missing Property ID', 'status': 'failed'}), 400

    Property.query.filter_by(id=id).delete()
    db.session.commit()
    properties = Property.query.all()
    return jsonify({'data': properties, 'msg': 'success'}), 201


@propertyRoute.route('/create', methods=['POST'])
@jwt_required
def get_create_property():

    name = request.json.get('name', None)
    address = request.json.get('address', None)
    area = request.json.get('area', None)
    state = request.json.get('state', None)
    bedrooms = request.json.get('bedrooms', None)
    built = request.json.get('built', None)
    units = request.json.get('units', None)
    rents = request.json.get('rents', None)
    serv_charge = request.json.get('serv_charge', None)
    sale_price = request.json.get('sale_price', None)
    floors = request.json.get('floors', None)
    facilities = request.json.get('facilties', None)
    land_size = request.json.get('land_size', None)

    if not name:
        return jsonify({'msg': 'Missing name', 'status': 'failed'}), 400

    if not address:
        return jsonify({'msg': 'Missing address', 'status': 'failed'}), 400

    if not area:
        return jsonify({'msg': 'Missing area', 'status': 'failed'}), 400

    if not state:
        return jsonify({'msg': 'Missing state', 'status': 'failed'}), 400

    if not bedrooms:
        return jsonify({'msg': 'Missing bedrooms', 'status': 'failed'}), 400

    if not built:
        return jsonify({'msg': 'Missing built', 'status': 'failed'}), 400

    if not units:
        return jsonify({'msg': 'Missing units', 'status': 'failed'}), 400

    if not rents:
        return jsonify({'msg': 'Missing rents', 'status': 'failed'}), 400

    if not serv_charge:
        return jsonify({'msg': 'Missing serv charge', 'status': 'failed'}), 400

    if not floors:
        return jsonify({'msg': 'Missing floors', 'status': 'failed'}), 400

    property = Property(
        name=name,
        address=address,
        area=area,
        state=state,
        bedrooms=bedrooms,
        built=built,
        units=units,
        serv_charge=serv_charge,
        sale_price=sale_price,
        floors=floors,
        facilities=facilities,
        land_size=land_size
    )
    db.session.add(property)
    db.session.commit()
    for key, value in rents.items():
        price = Price(
            property_id=property.id,
            amount=value,
            year=key,
        )
        db.session.add(price)

    db.session.commit()

    db.session.refresh(property)

    return jsonify({'msg': 'Property saved', 'status': 'success', 'data': property}), 201


@propertyRoute.route('/edit', methods=['POST'])
@jwt_required
def get_edit_property():

    id = request.json.get('id', None)
    name = request.json.get('name', None)
    address = request.json.get('address', None)
    area = request.json.get('area', None)
    state = request.json.get('state', None)
    bedrooms = request.json.get('bedrooms', None)
    built = request.json.get('built', None)
    units = request.json.get('units', None)
    rents = request.json.get('rents', None)
    serv_charge = request.json.get('serv_charge', None)
    sale_price = request.json.get('sale_price', None)
    floors = request.json.get('floors', None)
    facilities = request.json.get('facilties', None)
    land_size = request.json.get('land_size', None)

    if not id:
        return jsonify({'msg': 'Missing id', 'status': 'failed'}), 400

    if not name:
        return jsonify({'msg': 'Missing name', 'status': 'failed'}), 400

    if not address:
        return jsonify({'msg': 'Missing address', 'status': 'failed'}), 400

    if not area:
        return jsonify({'msg': 'Missing area', 'status': 'failed'}), 400

    if not state:
        return jsonify({'msg': 'Missing state', 'status': 'failed'}), 400

    if not bedrooms:
        return jsonify({'msg': 'Missing bedrooms', 'status': 'failed'}), 400

    if not built:
        return jsonify({'msg': 'Missing built', 'status': 'failed'}), 400

    if not units:
        return jsonify({'msg': 'Missing units', 'status': 'failed'}), 400

    if not rents:
        return jsonify({'msg': 'Missing rents', 'status': 'failed'}), 400

    if not serv_charge:
        return jsonify({'msg': 'Missing serv charge', 'status': 'failed'}), 400

    if not sale_price:
        return jsonify({'msg': 'Missing sale price', 'status': 'failed'}), 400

    if not floors:
        return jsonify({'msg': 'Missing floors', 'status': 'failed'}), 400

    if not facilities:
        return jsonify({'msg': 'Missing facilities', 'status': 'failed'}), 400

    if not land_size:
        return jsonify({'msg': 'Missing land size', 'status': 'failed'}), 400

    property = Property(
        name=name,
        addresss=address,
        area=area,
        state=state,
        bedrooms=bedrooms,
        built=built,
        units=units,
        serv_charge=serv_charge,
        sale_price=sale_price,
        floors=floors,
        facilities=facilities,
        land_size=land_size
    )
    db.session.add(property)
    db.session.commit()
    for item in rents:
        price = Price(
            property_id=property,
            amount=item['amount'],
            year=item['year'],
        )
        db.session.add(price)

    db.session.commit()

    db.session.refresh(property)

    return jsonify({'msg': 'Property saved', 'status': 'success', 'data': property}), 201
