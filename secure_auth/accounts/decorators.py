from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(*allowed_roles):
    """
    Decorator untuk membatasi akses view berdasarkan role user.
    Contoh pemakaian:

        @role_required("admin")
        def admin_dashboard(request): ...

        @role_required("admin", "staff")
        def staff_dashboard(request): ...

    Kalau user belum login -> diarahkan ke halaman login (via login_required).
    Kalau user login tapi role-nya tidak sesuai -> diarahkan ke access_denied,
    BUKAN dikasih pesan error yang membocorkan detail sistem.
    """

    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url="login")
        def wrapper(request, *args, **kwargs):
            profile = getattr(request.user, "profile", None)
            if profile is None or profile.role not in allowed_roles:
                return redirect("access_denied")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
