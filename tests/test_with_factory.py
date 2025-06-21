"""This module tests an app with factory boy"""

import pytest
from .factories import ClientFactory, ParkingFactory
from ..app.models import Client, Parking


@pytest.mark.factory_boy
def test_create_client(db):
    """Tests if client info creates successfully"""
    assert len(db.session.query(Client).all()) == 1
    new_client = ClientFactory()
    db.session.add(new_client)
    db.session.commit()
    assert len(db.session.query(Client).all()) == 2


@pytest.mark.factory_boy
def test_create_parking(db):
    """Tests if parking lot info creates successfully"""
    new_parking = ParkingFactory()
    parking_address = new_parking.address
    db.session.add(new_parking)
    db.session.commit()
    assert db.session.query(Parking).filter_by(address=parking_address).one()
