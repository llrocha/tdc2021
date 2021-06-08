from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app

#app = ZipCodeApp()


# @app.get("/")
# async def read_main():
#     return {"msg": "Hello World"}


client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"app_name": "Zip Code App"}

def test_empty_zipcode():
    response = client.get("/zipcode")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_invalid_zipcode():
    response = client.get("/zipcode/12345")
    assert response.status_code == 404
    assert response.json() == {"detail": "Zip Code must contain 8 characters"}

def test_unexistent_zipcode():
    response = client.get("/zipcode/12345678")
    assert response.status_code == 404
    assert response.json() == {"detail":"Zip code 12345678 does not exist."}

def test_existent_zipcode():
    response = client.get("/zipcode/89035300")
    assert response.status_code == 200
    assert response.json() == ["{'id': 89035300, 'zipcode': '89035300', 'city': 'Blumenau', 'state': 'SC', 'neighborhood': 'Vila Nova', 'public_place': 'Rua Theodoro Holtrup', 'description': ''}"]
    
def test_healthy():
    response = client.get("/hc/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
