from fastapi.testclient import TestClient


from app.main import app


client = TestClient(app)


def test_create_order():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImF2ZG9sIiwiZXhwIjoxNjg0MzIxODYwfQ.dzoSZZv5m64M2hWuEPTGn2alyp-wS_hQU5gmvfJhHf0"
    order = {
        "items": [
            {
                "id": "e1d23c8b-93ad-4b29-aa45-aad5ee65c5cd",
                "volume": "3"
            },
            {
                "id": "ff06833c-f705-4079-b575-c71f409ced27",
                "volume": "4"
            }
        ],
        "shipment_deadline": "2023-07-23"
    }
    response = client.post(
        "/orders", headers={'Content-Type': 'application/json',
                            'Accept': 'application/json', "Authorization": f"Bearer {token}"}, json=order)
    assert response.status_code == 200
    assert response.json()["detail"] == "Заказ успешно создан"
