import pytest
from app import app as flask_app
import json

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
    assert b"Sentiment Analysis with Transformers" in response.data

def test_predict_route_positive(client):
    """
    GIVEN a Flask application
    WHEN the '/predict' route is requested with positive text (POST)
    THEN check that the response is a valid positive prediction
    """
    test_text = "This is a fantastic library!"
    response = client.post('/predict',
                           data=json.dumps({'text': test_text}),
                           content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data
    assert 'confidence' in data
    assert 'inference_time_ms' in data
    assert data['prediction'] == 'POSITIVE'

def test_predict_route_negative(client):
    """
    GIVEN a Flask application
    WHEN the '/predict' route is requested with negative text (POST)
    THEN check that the response is a valid negative prediction
    """
    test_text = "I am very disappointed with this product."
    response = client.post('/predict',
                           data=json.dumps({'text': test_text}),
                           content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data
    assert 'confidence' in data
    assert 'inference_time_ms' in data
    assert data['prediction'] == 'NEGATIVE'

def test_predict_route_no_text(client):
    """
    GIVEN a Flask application
    WHEN the '/predict' route is requested with no text (POST)
    THEN check that a 400 error is returned
    """
    response = client.post('/predict',
                           data=json.dumps({'text': ''}),
                           content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No text provided'
