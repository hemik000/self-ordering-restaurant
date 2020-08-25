from django.apps import AppConfig


class CustomerConfig(AppConfig):
    name = "api.customer"

    def ready(self):
        import api.customer.signals
