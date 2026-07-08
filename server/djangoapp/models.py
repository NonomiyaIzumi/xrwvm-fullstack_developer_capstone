from django.db import models


class CarMake(models.Model):
    """A car manufacturer, e.g. Toyota, Ford, BMW."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class CarModel(models.Model):
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    COUPE = "Coupe"
    TRUCK = "Truck"
    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (COUPE, "Coupe"),
        (TRUCK, "Truck"),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=SEDAN)
    year = models.IntegerField(default=2023)
    dealer_id = models.IntegerField(help_text="Dealer id from the MongoDB dealer service")

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
