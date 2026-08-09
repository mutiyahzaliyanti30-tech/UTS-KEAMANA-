from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Akun & Kontrol Akses"

    def ready(self):
        import accounts.signals  # noqa: F401  (mendaftarkan signal saat app siap)
