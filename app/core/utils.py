from django.contrib.auth import get_user_model


def get_customer_orders():
    users = get_user_model().objects.prefetch_related('orders__products').all()
    return {user.username: list(user.orders.all()) for user in users}
