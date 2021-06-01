#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from scriptsConsultas import *
from hmgru.AutocallController import AutocallController

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmgru.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.runserver import Command as settings

        settings.default_addr = "148.204.142.162"
        settings.default_port = "3032"
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
