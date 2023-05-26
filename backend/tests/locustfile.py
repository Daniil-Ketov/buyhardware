import time
from locust import HttpUser, FastHttpUser, task, between, events
from uuid import uuid4
from numpy.random import randint as rand
from random import sample


def rd():
    return str(rand(0, 10))


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    print("Тестирование начато")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    num_users = environment.runner
    print(f"Количество пользователей: {num_users}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Тестирование завершено")


class BuyhardwareUser(HttpUser):
    wait_time = between(10, 30)
    hardware_list: list
    user_token: str
    admin_token: str
    id: str = str(uuid4())

    @task(2)
    def create_order(self):
        self.client.get("/hardware")
        self.client.post("/orders", headers={"Authorization": f"Bearer {self.user_token}"}, json={
            "items": [
                {
                    "id": self.hardware_list[i],
                    "volume": rand(1, 100)
                }
                for i in sample(range(len(self.hardware_list)), rand(1, len(self.hardware_list)))
            ],
            "shipment_deadline": "2023-07-"+str(rand(0, 3))+rd()
        })
        self.client.get(
            "/orders", headers={"Authorization": f"Bearer {self.user_token}"})

    @task(3)
    def view_profile_and_orders(self):
        self.client.get(
            "/users/", headers={"Authorization": f"Bearer {self.user_token}"})
        self.client.get(
            "/orders", headers={"Authorization": f"Bearer {self.user_token}"})

    def on_start(self):
        response = self.client.get("/hardware?page=1&limit=2000")
        json = response.json()
        self.hardware_list = [hardware["id"]
                              for hardware in json["result"]["content"]]

        self.client.post("/auth/register_client", json={
            "username": "test"+self.id,
            "email": "test"+self.id,
            "name": "test"+self.id,
            "password": "123456",
            "phone_number": "+7-"+rd()+rd()+rd()+"-"+rd()+rd()+rd()+"-"+rd()+rd()+"-"+rd()+rd(),
            "address": "test"+self.id,
            "postal_address": "test"+self.id,
            "tin": self.id
        })
        try:
            response = self.client.post("/auth/login", json={
                "username": "test"+self.id,
                "password": "123456"
            })
            json = response.json()
            self.user_token = json["result"]["access_token"]
        except:
            print("something goes wrong")
