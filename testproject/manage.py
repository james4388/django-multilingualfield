#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    REPO_ROOT = os.path.dirname( __file__ )
    sys.path.append(REPO_ROOT)
    sys.path.append(os.path.join(REPO_ROOT,'testproject'))
    
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproject.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
