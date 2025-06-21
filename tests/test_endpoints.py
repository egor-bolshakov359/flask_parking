"""This module tests an app"""
import pytest
from ..app.models import ClientParking, Client, Parking

urls = ["/clients", "/clients/1", "check"]


@pytest.mark.parametrize("check_url", urls)
def test_all_endpoints(check_url, client):
    """Test if url exists"""
    resp = client.get(check_url)
    assert resp.status_code == 200


def test_client_1(client):
    """Test if page with client info exists"""
    resp = client.get("/clients/1")

    assert resp.status_code == 200


def test_create_client(client):
    """Test creating of a new client info"""
    new_client = {"data": {
        "client_name": "fdsfwefwef",
        "client_surname": "me",
        "client_card": "2405",
        "client_car": "deds3221"

    }}
    headers = {"contentType": 'application/json'}
    resp = client.post("/clients", json=new_client, headers=headers)
    assert resp.status_code == 200


def test_create_parking(client):
    """Test creating of a new parking log info"""
    new_parking = {"data": {
        "address": "101 Main st",
        "count_spaces": "20"
    }}
    headers = {"contentType": 'application/json'}
    resp = client.post("/parkings", json=new_parking, headers=headers)
    assert resp.status_code == 200


@pytest.mark.parking
def test_entering_parking(client, db):
    """Test if parking entrance log posts correctly"""
    free_spaces_before = db.session.query(Parking).filter_by(id="1").first().count_available_places
    new_log = {"data": {
        "client_id": "2",
        "parking_id": "1"
    }}
    headers = {"contentType": 'application/json'}
    resp = client.post("/client_parkings", json=new_log, headers=headers)
    free_spaces_after = db.session.query(Parking).filter_by(id="1").first().count_available_places
    assert db.session.query(Parking).filter_by(id="1").first().opened is True
    assert free_spaces_after < free_spaces_before
    assert resp.status_code == 200


@pytest.mark.parking
@pytest.mark.parametrize("client_id, status_code", [("1", 200)])
def test_leaving_parking(client_id, status_code, client, db):
    """Test if parking exiting log posts correctly"""
    new_log = {"data": {
        "client_id": client_id,
        "parking_id": "1"
    }}
    headers = {"contentType": 'application/json'}
    resp = client.delete("client_parkings", json=new_log, headers=headers)
    parking_log = db.session.query(ClientParking).filter_by(id=client_id).first()
    assert parking_log.time_in < parking_log.time_out
    assert db.session.query(Client).filter_by(id=client_id).first().credit_card is not None
    assert resp.status_code == status_code
