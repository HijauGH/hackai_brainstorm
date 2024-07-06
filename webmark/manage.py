#!/usr/bin/env python
import os
import sys
from webmark import settings

def prerun():
    """from dotenv import load_dotenv
    from os import getenv
    load_dotenv()
    settings.SECRET_KEY = getenv("SECRET_KEY")
    settings.ADMIN_PANEL = getenv("ADMIN_PANEL")"""
    print("Prerun complite !")

def main():
    """Run administrative tasks."""
    prerun()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webmark.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
