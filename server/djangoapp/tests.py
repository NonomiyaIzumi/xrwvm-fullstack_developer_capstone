import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import CarMake, CarModel


class CarCatalogTests(TestCase):
    def setUp(self):
        make = CarMake.objects.create(name="Toyota", description="Test make")
        CarModel.objects.create(car_make=make, name="Corolla", type=CarModel.SEDAN, year=2023, dealer_id=1)

    def test_get_cars_returns_seeded_model(self):
        client = Client()
        response = client.get("/djangoapp/get_cars")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["CarModels"]), 1)
        self.assertEqual(data["CarModels"][0]["CarMake"], "Toyota")


class AuthFlowTests(TestCase):
    def test_register_then_login_then_logout(self):
        client = Client()

        register_response = client.post(
            "/djangoapp/register",
            data=json.dumps(
                {
                    "userName": "testuser",
                    "firstName": "Test",
                    "lastName": "User",
                    "email": "testuser@example.com",
                    "password": "S3curePass!",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(register_response.status_code, 200)
        self.assertEqual(register_response.json()["status"], "Authenticated")
        self.assertTrue(User.objects.filter(username="testuser").exists())

        client.logout()

        login_response = client.post(
            "/djangoapp/login",
            data=json.dumps({"userName": "testuser", "password": "S3curePass!"}),
            content_type="application/json",
        )
        self.assertEqual(login_response.json()["status"], "Authenticated")

        logout_response = client.get("/djangoapp/logout")
        self.assertEqual(logout_response.json()["userName"], "")
