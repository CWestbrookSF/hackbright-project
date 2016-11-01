"""Utility file to seed airfare database from iatacodes.org and
faredectective.com stored in seed_data/"""

import json
from model import Airport, Airfare, connect_to_db, db
from server import app
from sqlalchemy import func


def load_airports():
    """Load airports -- code, name, country code -- from seed_data/airports.json
     into database."""

    print "Airports"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate airports.
    Airport.query.delete()

    # Open airports.json file and parse data into airport table
    jf = open("seed_data/airports.json")
    dictionary = json.load(jf)
    for item in dictionary['response']:
        airport = Airport(code=item['code'],
                          country_code=item['country_code'],
                          name=item['name'].encode('ascii', 'ignore'),)
    
        db.session.add(airport)

    db.session.commit()

def load_airfares():
    """Load historical airfare info from seed_data/airfare.json file."""

    print "Airfare"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate airports.
    Airfare.query.delete()

    # Open airports.json file and parse data into airport table
    jf = open("seed_data/airfare.json")
    dictionary = json.load(jf)
    for i, item in enumerate(dictionary):
        airfare = Airfare(depart=item['depart'],
                          arrive=item['arrive'],
                          lowest_price=float(item['lowest_price'].encode('ascii', 'ignore')),
                          average_price=float(item['average_price'].encode('ascii', 'ignore')),
                          cheapest_month=item['cheapest_month'],)
    
        db.session.add(airfare)

        if i % 100 == 0:
            db.session.commit()

    db.session.commit()
    

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()
    
    # load_airports()
    # load_airfares()
    load_ports()
    print "All's well that ends in the database well."
