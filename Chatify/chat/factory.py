import factory
from faker import Faker
from factory.faker import Faker as FactoryFaker
from factory import LazyFunction, post_generation, SubFactory
from .models import User, Chat, ChatGroup
import datetime

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["email"]

    email = FactoryFaker("email")
    username = FactoryFaker("name")
    first_name = FactoryFaker("first_name")
    last_name = FactoryFaker("last_name")
    mobile_number = factory.Sequence(lambda n: fake.phone_number() + str(n))
    profile_photo = factory.django.ImageField(format="jpeg")
    is_online = FactoryFaker("pybool")

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = (
            extracted
            if extracted
            else FactoryFaker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)


class GroupNameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatGroup

    name = FactoryFaker("name")
    created = LazyFunction(datetime.datetime.utcnow)


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chat

    message = FactoryFaker("name")
    sent_at = LazyFunction(datetime.datetime.utcnow)
    client_timezone = FactoryFaker("timezone")
    group = SubFactory(GroupNameFactory)
    sender = SubFactory(UserFactory)
    is_deleted = FactoryFaker("pybool")
