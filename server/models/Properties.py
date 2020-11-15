from server.util.instances import db
from datetime import datetime as dt
from flask_admin.contrib.sqla import ModelView


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    built = db.Column(db.Integer, nullable=False)
    units = db.Column(db.Integer, nullable=False)
    rents = db.relationship('Price', cascade='all, delete, delete-orphan', backref='properties', lazy=False, passive_deletes=True)
    serv_charge = db.Column(db.String(15))
    sale_price = db.Column(db.String(15))
    floors = db.Column(db.Integer)
    facilities = db.Column(db.String(1024))
    land_size = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=dt.now(), onupdate=dt.now())

    def __repr__(self):
        return '{} at {}'.format(self.name, self.address)

    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'area': self.area,
            'state': self.state,
            'bedrooms': self.bedrooms,
            'built': self.built,
            'units': self.units,
            'rents': self.rents,
            'serv_charge': self.serv_charge,
            'sale_price': self.sale_price,
            'floors': self.floors,
            'facilities': self.facilities,
            'land_size': self.land_size,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }



class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', ondelete='CASCADE'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=dt.now(), onupdate=dt.now())


    def __repr__(self):
        return 'Price list for  property with id {}'.format(self.property_id)

    
    def json(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'year': self.year,
            'amount': self.amount,
        }

class PropertyAdmin(ModelView):
    form_choices = {'area': [('ikoyi', 'Ikoyi'), ('vi', 'Victoria Island'), ('lekki', 'Lekki'), ('oniru', 'Oniru')],
                    'state': [('lagos', 'Lagos')],
                    'bedrooms': [(1,'1 Bedroom'), (2, '2 Bedroom'), (3, '3 Bedroom'), (4, '4 Bedroom')]
                    }