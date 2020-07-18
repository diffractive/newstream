from django.apps import AppConfig


class NewstreamConfig(AppConfig):

    def ready(self):
        import newstream.signals  # noqa
