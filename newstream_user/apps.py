from django.apps import AppConfig


class NewstreamUserConfig(AppConfig):
    name = 'newstream_user'

    def ready(self):
        import newstream_user.signals
