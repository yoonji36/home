# backend/login/apps.py

from django.apps import AppConfig

class LoginConfig(AppConfig):
    name = 'login'

    def ready(self):
        import login.signals  # signals 연결
