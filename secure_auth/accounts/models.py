from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Menyimpan role tiap user secara terpisah dari model User bawaan Django.
    Password TIDAK disimpan di sini — password tetap ditangani penuh oleh
    django.contrib.auth (hashing PBKDF2 otomatis, salt unik per user).
    """

    ROLE_ADMIN = "admin"
    ROLE_STAFF = "staff"
    ROLE_USER = "user"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_STAFF, "Staff"),
        (ROLE_USER, "User"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class LoginAttempt(models.Model):
    """
    Mencatat SETIAP percobaan login (berhasil maupun gagal).
    Dipakai untuk mendeteksi brute force dan mengunci akun sementara
    setelah beberapa kali gagal berturut-turut (lihat accounts/views.py).
    """

    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    berhasil = models.BooleanField(default=False)
    waktu = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-waktu"]
        verbose_name = "Percobaan Login"
        verbose_name_plural = "Percobaan Login"

    def __str__(self):
        status = "berhasil" if self.berhasil else "gagal"
        return f"{self.username} - {status} - {self.waktu:%Y-%m-%d %H:%M}"


class AuditLog(models.Model):
    """
    Jejak audit: siapa melakukan apa, kapan, dari IP mana.
    Sengaja dibuat READ-ONLY lewat admin (lihat accounts/admin.py) supaya
    log tidak bisa diubah/dihapus diam-diam, walau oleh admin sekalipun
    dari panel web — konsisten dengan prinsip "integritas log".
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    aksi = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    waktu = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-waktu"]
        verbose_name = "Log Aktivitas"
        verbose_name_plural = "Log Aktivitas"

    def __str__(self):
        pelaku = self.user.username if self.user else "anonim"
        return f"[{self.waktu:%Y-%m-%d %H:%M}] {pelaku} - {self.aksi}"
