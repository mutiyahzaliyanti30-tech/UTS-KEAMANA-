#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secure_auth_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Tidak bisa import Django. Pastikan sudah 'pip install -r requirements.txt' "
            "dan virtual environment aktif."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
