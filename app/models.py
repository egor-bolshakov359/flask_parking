"""This module defines models"""

from typing import Dict, Any
from db import db


class Client(db.Model):
    """A class used to represent a client"""

    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    """A class used to represent a parking lot"""

    __tablename__ = "parking"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):
    """A class used to represent a parking log"""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    client = db.Column(db.Integer, db.ForeignKey("clients.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
    __table_args__ = (
        db.UniqueConstraint("client", "parking_id", name="unique_client_parking"),
    )
