import time
from locust import HttpUser, task, between

class ZipCode(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def get_app_name(self):
        self.client.get("/")

    @task(3)
    def view_items(self):
        zipcodes = [
            '01551010',
            '12010000',
            '23017100',
            '34018432',
            '45003335',
            '56304570',
            '67020651',
            '78025085',
            '89021901',
            '90110360'
        ]
        for zipcode in zipcodes:
            self.client.get(f"/zipcode/{zipcode}", name="/zipcode")
            time.sleep(1)

    def on_start(self):
        self.client.get("/hc")

