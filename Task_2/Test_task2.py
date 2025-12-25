import pytest
import requests

BASE_URL = "https://qa-internship.avito.com"
SELLER_ID = 888888 

@pytest.fixture(scope="session")
def created_item_id():
    payload = {
        "sellerId": SELLER_ID,
        "name": f"Test Item {uuid.uuid4()}",
        "price": 1500,
        "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 200, f"Create failed: {response.text}"
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], str)  
    assert data["sellerId"] == SELLER_ID
    yield data["id"]

def test_create_item_valid():
    payload = {
        "sellerId": SELLER_ID,
        "name": "Valid Test Item",
        "price": 999, 
        "statistics":{"likes": 0, "viewCount": 0, "contacts": 0}
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], str)
    assert "createdAt" in data  
    assert data["sellerId"] == SELLER_ID
    assert data["price"] == 999

def test_create_item_missing_field():
    payload = {
        "name": "No sellerId",
        "price": 100
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400 

def test_get_item_by_id(created_item_id):
    response = requests.get(f"{BASE_URL}/api/1/item/{created_item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["sellerId"] == SELLER_ID
    assert "createdAt" in data

def test_get_item_not_found():
    response = requests.get(f"{BASE_URL}/api/1/item/999999")
    assert response.status_code == 400 

def test_get_items_by_seller(created_item_id):
    response = requests.get(f"{BASE_URL}/api/1/{SELLER_ID}/item")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)  
    ids = [item["id"] for item in items]
    assert created_item_id in ids

def test_get_items_empty_seller():
    empty_seller = 999999
    response = requests.get(f"{BASE_URL}/api/1/{empty_seller}/item")
    assert response.status_code == 200
    data = response.json()
    
    if isinstance(data, list):
        assert len(data) == 0
    else:
        assert "items" in data or len(data) == 0

def test_get_statistic(created_item_id):
    response = requests.get(f"{BASE_URL}/api/1/statistic/{created_item_id}")
    assert response.status_code == 200
    stats = response.json()
    assert isinstance(stats, list)  
    if stats:
        first = stats[0]
        assert "views" in first or "likes" in first or "contacts" in first

def test_get_statistic_not_found():
    response = requests.get(f"{BASE_URL}/api/1/statistic/999999")
    assert response.status_code == 400 


