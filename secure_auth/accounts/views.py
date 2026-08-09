from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils import timezone

from .decorators import role_required
from .models import AuditLog, LoginAttempt, Profile


def get_client_ip(request):
    """Ambil IP asli user, termasuk kalau di belakang proxy/load balancer."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def catat_audit(request, user, aksi, deskripsi=""):
    AuditLog.objects.create(
        user=user,
        aksi=aksi,
        deskripsi=deskripsi,
        ip_address=get_client_ip(request),
    )


def akun_sedang_terkunci(username):
    """
    Cek apakah username tertentu sedang dalam masa lockout, berdasarkan
    jumlah percobaan gagal berturut-turut dalam LOGIN_LOCKOUT_MINUTES
    terakhir. Ini mitigasi terhadap serangan Brute Force / Broken
    Authentication.
    """
    batas_waktu = timezone.now() - timedelta(minutes=settings.LOGIN_LOCKOUT_MINUTES)
    percobaan_terakhir = LoginAttempt.objects.filter(
        username=username, waktu__gte=batas_waktu
    ).order_by("-waktu")[: settings.LOGIN_MAX_ATTEMPTS]

    if percobaan_terakhir.count() < settings.LOGIN_MAX_ATTEMPTS:
        return False

    # Terkunci hanya jika SEMUA percobaan N-terakhir itu gagal
    return all(not p.berhasil for p in percobaan_terakhir)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        ip = get_client_ip(request)

        if akun_sedang_terkunci(username):
            messages.error(
                request,
                f"Akun ini sementara dikunci karena terlalu banyak percobaan "
                f"gagal. Coba lagi setelah {settings.LOGIN_LOCKOUT_MINUTES} menit.",
            )
            catat_audit(request, None, "login_blocked_lockout", f"username={username}")
            return render(request, "accounts/login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            LoginAttempt.objects.create(username=username, ip_address=ip, berhasil=True)
            login(request, user)  # Django otomatis regenerasi session key di sini
            catat_audit(request, user, "login_sukses")
            messages.success(request, f"Selamat datang, {user.username}!")
            return redirect("dashboard")
        else:
            LoginAttempt.objects.create(username=username, ip_address=ip, berhasil=False)
            catat_audit(request, None, "login_gagal", f"username={username}")
            messages.error(request, "Username atau password salah.")

    return render(request, "accounts/login.html")


def logout_view(request):
    if request.user.is_authenticated:
        catat_audit(request, request.user, "logout")
    logout(request)
    messages.info(request, "Kamu sudah logout.")
    return redirect("login")


def dashboard_redirect(request):
    """
    Satu pintu masuk setelah login, lalu diarahkan sesuai role masing-masing.
    """
    if not request.user.is_authenticated:
        return redirect("login")

    profile = getattr(request.user, "profile", None)
    role = profile.role if profile else Profile.ROLE_USER

    if role == Profile.ROLE_ADMIN:
        return redirect("dashboard_admin")
    elif role == Profile.ROLE_STAFF:
        return redirect("dashboard_staff")
    return redirect("dashboard_user")


@role_required(Profile.ROLE_ADMIN)
def dashboard_admin(request):
    log_terbaru = AuditLog.objects.all()[:20]
    percobaan_gagal = LoginAttempt.objects.filter(berhasil=False)[:20]
    return render(
        request,
        "accounts/dashboard_admin.html",
        {"log_terbaru": log_terbaru, "percobaan_gagal": percobaan_gagal},
    )


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_STAFF)
def dashboard_staff(request):
    return render(request, "accounts/dashboard_staff.html")


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_STAFF, Profile.ROLE_USER)
def dashboard_user(request):
    return render(request, "accounts/dashboard_user.html")


def access_denied(request):
    return render(request, "accounts/access_denied.html")
