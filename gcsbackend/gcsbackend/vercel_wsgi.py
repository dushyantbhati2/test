import sys
import os

# Add the current project directory to PYTHONPATH
sys.path.append(os.path.dirname(__file__))

# Set DJANGO_SETTINGS_MODULE to your settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gcsbackend.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
