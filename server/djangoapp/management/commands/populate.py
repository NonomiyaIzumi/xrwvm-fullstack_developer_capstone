from django.core.management.base import BaseCommand

from djangoapp.models import CarMake, CarModel

CAR_DATA = [
    ("Toyota", "Reliable Japanese manufacturer known for durability.", [
        ("Camry", CarModel.SEDAN, 2022, 1),
        ("Corolla", CarModel.SEDAN, 2023, 2),
        ("RAV4", CarModel.SUV, 2023, 3),
    ]),
    ("Honda", "Japanese manufacturer known for efficient engines.", [
        ("Civic", CarModel.SEDAN, 2022, 1),
        ("CR-V", CarModel.SUV, 2023, 4),
    ]),
    ("Ford", "American manufacturer known for trucks and SUVs.", [
        ("F-150", CarModel.TRUCK, 2023, 5),
        ("Mustang", CarModel.COUPE, 2022, 2),
        ("Explorer", CarModel.SUV, 2023, 6),
    ]),
    ("BMW", "German manufacturer known for performance vehicles.", [
        ("3 Series", CarModel.SEDAN, 2023, 7),
        ("X5", CarModel.SUV, 2022, 3),
    ]),
    ("Chevrolet", "American manufacturer with a broad lineup.", [
        ("Malibu", CarModel.SEDAN, 2022, 8),
        ("Silverado", CarModel.TRUCK, 2023, 5),
    ]),
]


class Command(BaseCommand):
    help = "Seed the database with CarMake and CarModel demo data for the capstone project."

    def handle(self, *args, **options):
        created_makes = 0
        created_models = 0
        for make_name, description, models_ in CAR_DATA:
            make, was_created = CarMake.objects.get_or_create(
                name=make_name, defaults={"description": description}
            )
            created_makes += int(was_created)
            for model_name, car_type, year, dealer_id in models_:
                _, model_created = CarModel.objects.get_or_create(
                    car_make=make,
                    name=model_name,
                    defaults={"type": car_type, "year": year, "dealer_id": dealer_id},
                )
                created_models += int(model_created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created_makes} new car makes and {created_models} new car models."
            )
        )
