from server.util.instances import db
from datetime import datetime as dt
from flask_admin.contrib.sqla import ModelView


class Property(db.Model):
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
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=dt.now(), onupdate=dt.now())

    def __repr__(self):
        return '{} at {}'.format(self.name, self.address)

    
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
            'year': self.year,
            'amount': self.amount,
        }



    


class PropertyAdmin(ModelView):
    form_choices = {'area': [('ikoyi', 'Ikoyi'), ('vi', 'Victoria Island'), ('lekki', 'Lekki'), ('oniru', 'Oniru')],
                    'state': [('lagos', 'Lagos')],
                    'bedrooms': [(1,'1 Bedroom'), (2, '2 Bedroom'), (3, '3 Bedroom'), (4, '4 Bedroom')],
                    'type': [('Flat','Flat'), ('pent house', 'Pent House'), ('terrace', 'Terrace'), ("duplex", 'Duplex'), ("maisonette", 'Maisonette')]
                    }
    
    column_auto_select_related = True
    inline_models = [(Price,dict(form_columns=['id', 'year', 'amount']))]
    column_labels = {'built': 'Year built', 'serv_charge': 'Service charge'}
    column_sortable_list = ('area', 'bedrooms', 'name', 'built',)
    column_searchable_list = ('name', 'area',)
    column_exclude_list=('created_at', 'updated_at')
    column_default_sort = ('name',False)
    can_export = True
    column_editable_list = ('name', 'bedrooms', 'address', 'area', 'serv_charge', 'type', 'sale_price')
    form_widget_args = {
        'facilities': {
            'rows': 6
        }
    }

