from django.contrib import admin

from .models import AuditLog, LoginAttempt, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "dibuat_pada")
    list_filter = ("role",)
    search_fields = ("user__username",)


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ("username", "ip_address", "berhasil", "waktu")
    list_filter = ("berhasil",)
    search_fields = ("username", "ip_address")

    # Read-only: log percobaan login tidak boleh diedit/ditambah manual
    # lewat panel admin, supaya datanya tetap bisa dipercaya (integritas log).
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("waktu", "user", "aksi", "ip_address")
    list_filter = ("aksi",)
    search_fields = ("user__username", "aksi", "deskripsi")

    # Sama seperti LoginAttempt: audit log read-only lewat web/admin.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
