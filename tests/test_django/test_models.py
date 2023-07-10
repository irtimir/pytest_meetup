import pytest

from core.models import Post
from core.utils import get_user_names_posts
from tests.test_django.factories import UserFactory, PostFactory


@pytest.mark.django_db
def test_my_user(django_user_model):
    me = django_user_model.objects.create(username='me')
    assert not me.is_superuser


@pytest.mark.django_db
def test_n_plus_1(django_user_model, django_assert_num_queries):
    for n in range(100):
        django_user_model.objects.create(username=str(n))

    with django_assert_num_queries(2):
        get_user_names_posts()


@pytest.mark.django_db
def test_user(django_user_model):
    user = UserFactory()
    assert not user.is_superuser
    assert len(django_user_model.objects.all()) == 1


@pytest.mark.django_db
def test_superuser(django_user_model, superuser):
    assert superuser.is_superuser
    assert len(django_user_model.objects.filter(pk=superuser.pk, is_superuser=True)) == 1


@pytest.mark.django_db
def test_post():
    PostFactory()

    assert len(Post.objects.all()) == 1


@pytest.mark.django_db
def test_post_with_user(user):
    PostFactory(author=user)

    assert len(Post.objects.filter(author=user)) == 1
