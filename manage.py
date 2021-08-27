#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.runserver import Command as runserver

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if is_docker():
        runserver.default_addr = '0.0.0.0'

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
