import json
import pytest
from app import app
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello World.' in response.data

def test_hello_world_unsuccessful(client):
    response = client.get('/invalid_path')
    assert response.status_code == 404
    assert b'Hello World.' not in response.data

def test_get_all_tweets(client):
    response = client.get('/tweets')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
def test_create_tweet_success(client):
    tweet_data = {'user_name': 'JohnDoe', 'text': 'Test tweet'}
    response = client.post('/tweets', json=tweet_data)
    assert response.status_code == 201
    assert response.json['user_name'] == 'JohnDoe'

def test_create_tweet_incomplete_data(client):
    incomplete_data = {'user_name': 'JohnDoe'}  # Missing 'text'
    response = client.post('/tweets', json=incomplete_data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_get_tweet_by_id_success(client):
    response = client.get('/tweet/1360000000000000000')
    assert response.status_code == 200
    assert 'id_str' in response.json

def test_get_tweet_by_id_not_found(client):
    # Assume tweet with ID 999 does not exist in your dataset
    response = client.get('/tweet/999')
    assert response.status_code == 404
    assert 'error' in response.json
