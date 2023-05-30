#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from precreate import main as precreate_main


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.contrib.auth import get_user_model
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if sys.argv[-1] == 'mymigration':
        os.remove('db.sqlite3')
        execute_from_command_line(sys.argv[:-1] + ['migrate'])
        User = get_user_model()
        User.objects.create_superuser('admin', '', '12345')
    if sys.argv[-1] == 'precreate':
        precreate_main()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
