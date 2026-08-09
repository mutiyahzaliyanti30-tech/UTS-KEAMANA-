from django.contrib.auth.hashers import make_password
from django.db import migrations


# --------------------------------------------------------------------------
# Data akun demo. Password di sini HANYA untuk keperluan demo tugas kuliah,
# dan tetap disimpan ter-hash (PBKDF2 + salt unik) lewat make_password(),
# BUKAN plaintext, walaupun didefinisikan di source code.
#
# Untuk pemakaian sungguhan: jangan pernah hardcode password demo di
# migration seperti ini di project produksi.
# --------------------------------------------------------------------------
AKUN_DEMO = [
    {"username": "admin_demo", "password": "AdminAman123!", "role": "admin", "is_staff": True, "is_superuser": True},
    {"username": "staff_demo", "password": "StaffAman123!", "role": "staff", "is_staff": False, "is_superuser": False},
    {"username": "user_demo", "password": "UserAman123!", "role": "user", "is_staff": False, "is_superuser": False},
]


def buat_akun_demo(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("accounts", "Profile")
    AuditLog = apps.get_model("accounts", "AuditLog")

    for data in AKUN_DEMO:
        if User.objects.filter(username=data["username"]).exists():
            continue

        user = User.objects.create(
            username=data["username"],
            password=make_password(data["password"]),
            is_staff=data["is_staff"],
            is_superuser=data["is_superuser"],
            is_active=True,
        )
        # Profile mungkin sudah otomatis dibuat oleh signal saat testing,
        # tapi signal TIDAK berjalan di dalam data migration seperti ini,
        # jadi kita buat manual dan pastikan tidak dobel dengan get_or_create.
        Profile.objects.get_or_create(user=user, defaults={"role": data["role"]})

    AuditLog.objects.create(
        user=None,
        aksi="seed_demo_users",
        deskripsi="3 akun demo (admin_demo, staff_demo, user_demo) dibuat via migration.",
    )


def hapus_akun_demo(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username__in=[d["username"] for d in AKUN_DEMO]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(buat_akun_demo, hapus_akun_demo),
    ]
