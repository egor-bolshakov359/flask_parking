"""This module defines fixtures for testing"""

from datetime import datetime
import pytest
from app.main import create_app
from db import db as _db
from app.models import Parking, Client, ClientParking



@pytest.fixture
def app():
    """This function creates a fixture of an app"""
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'

    with _app.app_context():
        _db.drop_all()
        _db.create_all()

        _client = Client(
            name="newname",
            surname="newsurname",
            credit_card="999",
            car_number="0aaa000"
        )

        _parking = Parking(
            address="11 Main st",
            opened=True,
            count_places=10,
            count_available_places=10
        )
        _clientparking = ClientParking(
            client=1,
            parking_id=1,
            time_in=datetime.now()
        )
        _db.session.add(_client)
        _db.session.add(_parking)
        _db.session.add(_clientparking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    """This module creates a fixture of a client"""
    app_client = app.test_client()
    yield app_client


@pytest.fixture
def db(app):
    """This function creates a fixture of a database"""
    with app.app_context():
        yield _db
