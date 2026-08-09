# Secure Auth System — Login & Role-Based Access Control

Project Django untuk tugas Keamanan Komputer, bertema **autentikasi dan
kontrol akses berbasis role (RBAC)**. Lebih menekankan pada praktik
keamanan aplikasi web dibanding sekadar CRUD biasa.

## Fitur Keamanan yang Diimplementasikan

| Fitur | Penjelasan |
|---|---|
| **Password Hashing** | Password user disimpan ter-hash pakai PBKDF2 + salt unik (bawaan Django `django.contrib.auth`), bukan plaintext. |
| **Role-Based Access Control (RBAC)** | 3 role: `admin`, `staff`, `user`. Tiap halaman dashboard dibatasi decorator `@role_required(...)` di `accounts/decorators.py`. |
| **Account Lockout** | Setelah `LOGIN_MAX_ATTEMPTS` (5) kali gagal login berturut-turut dalam `LOGIN_LOCKOUT_MINUTES` (15 menit), akun dikunci sementara — mitigasi brute force. |
| **Audit Log** | Semua aksi penting (login sukses, login gagal, logout, blokir lockout) tercatat di tabel `AuditLog` dengan waktu, user, dan IP. Read-only lewat admin panel. |
| **Login Attempt Log** | Setiap percobaan login (berhasil/gagal) tercatat di `LoginAttempt`, jadi bisa dianalisis pola serangannya. |
| **CSRF Protection** | Form login pakai `{% csrf_token %}` (bawaan Django, aktif otomatis lewat middleware). |
| **Session Security** | `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE`, `SESSION_EXPIRE_AT_BROWSER_CLOSE`, dan session timeout 30 menit — mitigasi session hijacking. Django juga otomatis regenerasi session key tiap kali login (mitigasi session fixation). |
| **Clickjacking Protection** | `X_FRAME_OPTIONS = "DENY"` supaya halaman tidak bisa ditaruh dalam `<iframe>` situs lain. |
| **Password Validators** | Django `AUTH_PASSWORD_VALIDATORS` aktif: menolak password terlalu pendek, terlalu umum, mirip data user, atau full angka. |

## Struktur Project

```
secure_auth/
├── manage.py
├── requirements.txt
├── secure_auth_project/      # folder settings Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── accounts/                 # app utama
    ├── models.py             # Profile, LoginAttempt, AuditLog
    ├── views.py              # login, logout, dashboard per role
    ├── decorators.py         # role_required()
    ├── signals.py            # auto-create Profile untuk user baru
    ├── admin.py               # log dibuat read-only di admin panel
    ├── migrations/
    │   ├── 0001_initial.py
    │   └── 0002_seed_demo_users.py   # buat 3 akun demo otomatis
    └── templates/accounts/
```

## Cara Menjalankan

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` untuk halaman login.

### Akun Demo (dibuat otomatis lewat migration)

| Username | Password | Role |
|---|---|---|
| `admin_demo` | `AdminAman123!` | Admin (akses semua dashboard + panel admin Django di `/admin/`) |
| `staff_demo` | `StaffAman123!` | Staff (akses dashboard staff & user) |
| `user_demo` | `UserAman123!` | User (akses dashboard user saja) |

> Catatan: password demo ini sengaja dibuat "kuat" (huruf besar, kecil,
> angka, simbol, 8+ karakter) supaya lolos `AUTH_PASSWORD_VALIDATORS`.
> Password tetap disimpan ter-hash di database, bukan plaintext.

### Mau bikin superuser sendiri?

```bash
python manage.py createsuperuser
```

User yang dibuat lewat cara ini otomatis dapat `Profile` dengan role
default `user` (lewat signal di `accounts/signals.py`) — kalau mau jadi
admin, ubah role-nya lewat Django admin panel di `/admin/`.

## Kenapa Log & Percobaan Login Read-Only di Admin?

Supaya konsisten dengan prinsip **integritas audit trail**: kalau siapa
pun (termasuk admin) bisa mengedit/menghapus log lewat panel web, log itu
jadi tidak bisa dipercaya lagi sebagai bukti forensik. Makanya di
`accounts/admin.py`, `LoginAttempt` dan `AuditLog` di-set
`has_add_permission`, `has_change_permission` (dan `has_delete_permission`
untuk AuditLog) jadi `False`.

## Untuk Deployment Sungguhan (Bukan Tugas Lokal)

Beberapa hal di `settings.py` sengaja dimatikan/disederhanakan karena
project ini jalan di `runserver` lokal (HTTP, bukan HTTPS):

- `SECRET_KEY` harus diambil dari environment variable, jangan hardcode.
- `DEBUG = False` di production.
- Aktifkan `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`,
  `SECURE_SSL_REDIRECT` (sudah dikomentari di `settings.py`, tinggal
  di-uncomment kalau sudah pakai HTTPS).
