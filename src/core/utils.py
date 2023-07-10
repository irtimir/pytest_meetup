from django.contrib.auth import get_user_model


def get_user_names_posts():
    users = get_user_model().objects.prefetch_related('posts').all()
    return {user.username: list(user.posts.all()) for user in users}
