from server.models.Properties import Property


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