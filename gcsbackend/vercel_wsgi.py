import os
import sys
from pathlib import Path

# add project root (one level above current file)
sys.path.append(str(Path(__file__).resolve().parent))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gcsbackend.settings")

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
