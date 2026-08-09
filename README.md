Sistem Login dengan Role-Based Access Control (RBAC) — tugas Keamanan Komputer.
Inti konsepnya: Bukan cuma login biasa, tapi nunjukin gimana caranya sistem web yang "aman" itu bekerja — siapa boleh akses apa, dan gimana serangan-serangan umum dicegah.
3 Role Pengguna:
Admin → bisa lihat semua dashboard + log aktivitas semua orang
Staff → bisa lihat dashboard staff & user
User → cuma bisa lihat dashboard user sendiri
Kalau user coba akses halaman yang bukan levelnya, otomatis ditolak (halaman "Akses Ditolak"), bukan malah error atau nyasar ke data yang bukan haknya.
Fitur keamanan yang diterapin (7 poin):
Password Hashing — password gak disimpan polos di database, tapi di-enkripsi (hash) pakai algoritma PBKDF2
Role-Based Access Control — pembagian akses per role kayak dijelasin di atas
Account Lockout — kalau salah password 5x berturut-turut, akun dikunci sementara 15 menit (mencegah brute force/tebak-tebak password)
Audit Log — setiap aktivitas (login berhasil, gagal, logout) tercatat waktu & IP-nya
CSRF Protection — mencegah form dipalsuin dari situs lain
Session Security — cookie session diatur aman, otomatis logout kalau browser ditutup
Clickjacking Protection — halaman gak bisa "disusupin" lewat iframe situs lain
Struktur teknis (Django):
App accounts isinya 3 model: Profile (role user), LoginAttempt (catatan tiap percobaan login), AuditLog (jejak aktivitas)
Decorator role_required() yang jadi "penjaga pintu" tiap halaman
3 akun demo otomatis kebuat pas migrate: admin_demo, staff_demo, user_demo
