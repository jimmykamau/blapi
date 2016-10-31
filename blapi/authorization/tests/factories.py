import factory
from ..models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.LazyAttribute(
        lambda a: '{0}@domain.com'.format(
            a.full_name.replace(' ', '')).lower())
    password = factory.LazyAttribute(
        lambda a: '{0}'.format(
            a.full_name.replace(' ', '')))
    full_name = factory.Faker('name')
    active = True
