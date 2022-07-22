from server.util.instances import db
from sqlalchemy.orm import backref
from datetime import datetime as dt
import enum
from .Auth import Auth


class CommercialTypes(enum.Enum):
    converted = 'Converted'
    purpose_built = 'Purpose Built'


class Property(db.Model, Auth):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    built = db.Column(db.Integer, nullable=True)
    units = db.Column(db.Integer, nullable=False)
    rents = db.relationship('Price', cascade='all, delete, delete-orphan',
                            backref='properties', lazy=False, passive_deletes=True, order_by='Price.year')
    serv_charge = db.Column(db.Float)
    sale_price = db.Column(db.Float)
    floors = db.Column(db.Integer)
    facilities = db.Column(db.Text(1024))
    land_size = db.Column(db.String(255))
    is_commercial = db.Column(db.Boolean)
    commercial_type = db.Column(db.Enum(CommercialTypes))
    size_in_sqm = db.Column(db.Integer)
    rent_per_sqm = db.Column(db.Float)
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=dt.now(), onupdate=dt.now())

    def __repr__(self):
        return f'{self.name} at {self.address}'

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'type': self.type,
            'area': self.area,
            'state': self.state,
            'bedrooms': self.bedrooms,
            'built': self.built,
            'units': self.units,
            'rents': self.rents,
            'serv_charge': self.serv_charge,
            'sale_price': self.sale_price,
            'floors': self.floors,
            'rent_per_sqm': self.rent_per_sqm,
            'is_commercial': self.is_commercial,
            'size_in_sqm': self.size_in_sqm,
            'commercial_type': self.commercial_type,
            'facilities': self.facilities,
            'land_size': self.land_size,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey(
        'properties.id', ondelete='CASCADE'), nullable=False)
    property = db.relationship(
        'Property', backref=backref('Price', uselist=False),)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=dt.now(), onupdate=dt.now())

    def __repr__(self):
        return f'{self.property} {self.year} rent({self.amount})\n'

    def __gt__(self, other):

        if(self.amount > other.amount):
            return True

        else:
            return False

    def __lt__(self, other):

        if(self.amount < other.amount):
            return True

        else:
            return False

    def __ge__(self, other):

        if(self.amount > other.amount or self.amount == other.amount):
            return True

        else:
            return False

    def __le__(self, other):

        if(self.amount < other.amount or self.amount == other.amount):
            return True

        else:
            return False

    def __add__(self, other):
        return self.amount + other.amount

    def json(self):
        return {
            'year': self.year,
            'amount': self.amount,
        }
