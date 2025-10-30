import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_route(client):
    """
    GIVEN a Flask application
    WHEN the '/' route is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200

def test_predict_route(client):
    """
    GIVEN a Flask application
    WHEN the '/predict' route is requested (POST)
    THEN check that the response is a valid prediction
    """
    response = client.post('/predict')
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data
    assert 'confidence' in data
    assert 'inference_time' in data
    assert 'model_info' in data
