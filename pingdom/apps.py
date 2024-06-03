from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = "pingdom"

    def ready(self):
        import pingdom.signals  # Ensure signal handlers are connected
