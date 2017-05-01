#!/usr/bin/env python
***REMOVED***

***REMOVED***
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cts.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
