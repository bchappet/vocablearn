from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_static_files():
    response = client.get("/static/styles.css")  # Updated path to match actual static file structure
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]

def test_routes_exist():
    routes = [route.path for route in app.routes]
    print(routes)
    assert "/manage/" in routes  
    assert "/quiz/" in routes   
    assert "/settings" in routes 
    assert "/keyboard/" in routes 
    assert "/reset_database" in routes 

def test_startup_event():
    # This test will implicitly test create_db_and_tables()
    # since it's called on startup
    with TestClient(app) as test_client:
        response = test_client.get("/")
        assert response.status_code == 200