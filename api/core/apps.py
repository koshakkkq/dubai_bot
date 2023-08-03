from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'shop'

    def ready(self):

        from . import recivers
        post_migrate.connect(recivers.run_post_migrate, sender=self)