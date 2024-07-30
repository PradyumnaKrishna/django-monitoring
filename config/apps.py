from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = "config"

    def ready(self):
        import config.signals  # Ensure signal handlers are connected
