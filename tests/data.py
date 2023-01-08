import random

from faker import Faker

fake = Faker(seed=random.seed)


def random_email():
    return fake.email()


def randon_name():
    return fake.name().replace(" ", "").lower()
