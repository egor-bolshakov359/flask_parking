import factory
from app.models import Client, Parking


class ClientFactory(factory.Factory):
    """This class defines a factory of a Client model"""
    class Meta:
        model = Client

    name = factory.Faker("first_name_female")
    surname = factory.Faker("last_name_female")
    credit_card = factory.Faker("credit_card_number")
    car_number = factory.Faker("pystr", max_chars=10)


class ParkingFactory(factory.Factory):
    """This class defines a factory of a Parking model"""
    class Meta:
        model = Parking

    address = factory.Faker("address")
    opened = factory.Faker("pybool")
    count_places = factory.Faker("pyint", max_value=1000)
    count_available_places = factory.LazyAttribute(lambda a: a.count_places - 1)
