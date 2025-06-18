from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        print("✨ Ready called")
        from django.contrib.auth import get_user_model
        print("👀 User model:", get_user_model())
        import users.signals
