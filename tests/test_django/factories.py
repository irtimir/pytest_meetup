import factory.fuzzy
from django.contrib.auth import get_user_model

from core.models import Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.faker.Faker('bothify', text='generated-###???')
    email = factory.LazyAttribute(lambda x: f'{x.username}@example.com')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.fuzzy.FuzzyText(length=10)
    text = factory.fuzzy.FuzzyText(length=512)
    author = factory.SubFactory(UserFactory)
