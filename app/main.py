"""This module sets up the app and routes"""

from datetime import datetime
from flask import Flask, request, jsonify
from sqlalchemy.exc import NoResultFound
from db import db
from app.models import Client, Parking, ClientParking


def create_app():

    """
    Create an app and configure it
    """

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/check")
    def hello():

        """Create first test client profile"""

        db.session.add(Client(name="a", surname="b"))
        db.session.commit()
        return "Microphone Check, One-Two", 200

    @app.route("/clients")
    def clients():

        """Get all client profiles"""

        all_clients = db.session.query(Client).all()
        clients_list = [i.to_json() for i in all_clients]
        return jsonify(clients_list), 200

    @app.route("/clients/<int:client_id>")
    def client(client_id: int):

        """Get a specific client profile"""

        client_info = db.session.query(Client).filter_by(id=client_id).one()
        client_json = client_info.to_json()
        return jsonify(client_json), 200

    @app.route("/clients", methods=["POST"])
    def post_client():

        """Post a new client profile"""

        client_data: dict = request.get_json().get("data")
        client_name = client_data.get("client_name")
        client_surname = client_data.get("client_surname")
        client_card = client_data.get("client_card")
        client_car = client_data.get("client_car")
        client_info = Client(
            name=client_name,
            surname=client_surname,
            credit_card=client_card,
            car_number=client_car
        )
        db.session.add(client_info)
        db.session.commit()
        return "Client successfull", 200

    @app.route("/parkings", methods=["POST"])
    def post_parking():

        """Post a new parking lot profile"""

        parking_data: dict = request.get_json().get("data")
        parking_address = parking_data.get("address")
        parking_spaces = parking_data.get("count_spaces")
        parking_data = Parking(
            address=parking_address,
            opened=True,
            count_places=parking_spaces,
            count_available_places=parking_spaces
        )
        db.session.add(parking_data)
        db.session.commit()
        return "New Parking Lot Created Successfully", 200

    @app.route("/client_parkings", methods=["POST"])
    def client_parkings():
        """
        Post a new parking entrance log
        """
        parking_client_info: dict = request.get_json().get("data")
        client_id = parking_client_info.get("client_id")
        parking_id = parking_client_info.get("parking_id")
        parking_info = db.session.get(Parking, ident=parking_id)
        parking_info_json = parking_info.to_json()
        if (parking_info_json["opened"] is True
                and parking_info_json["count_available_places"] > 0):

            parking_info.count_available_places -= 1
            new_parking_log = ClientParking(
                client=client_id,
                parking_id=parking_id,
                time_in=datetime.now()
            )
            db.session.add(new_parking_log)
            db.session.commit()
            return "Car parked", 200

        return "Lot if closed or full", 200

    @app.route("/client_parkings", methods=["DELETE"])
    def client_parkings_delete():
        """
        Post a parking exit information into existing parking entrance log
        """
        parking_client_info: dict = request.get_json().get("data")
        client_id = parking_client_info.get("client_id")
        parking_id = parking_client_info.get("parking_id")
        parking_info = db.session.get(Parking, ident=parking_id)
        try:
            parking_log_info = (db.session.query(ClientParking)
                                .filter_by(client=client_id)
                                .filter_by(parking_id=parking_id)
                                .filter_by(time_out=None).one())

            parking_log_info.time_out = datetime.now()
            parking_info.count_available_places += 1
            db.session.commit()
            return "Car left the lot", 200
        except NoResultFound:
            return "Car already left the log or never entered it", 201

    return app
