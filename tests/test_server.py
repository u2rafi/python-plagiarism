import json
from plagiarism.web.server import app


def test_route():
    with app.test_client() as client:
        rv = client.get('/')
        assert rv.status_code == 200


def test_request():
    with app.test_client() as client:
        rv = client.post('/', data=dict(text='the Big Bang singularity'))
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert data['success'] == True