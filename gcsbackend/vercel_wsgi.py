# gcsbackend/vercel_wsgi.py
# wrapper so Vercel finds `app` or `handler` variables.

# Import the Django WSGI application and expose it under the names Vercel expects.
# Your gcsbackend/gcsbackend/wsgi.py already exposes `application`.
from gcsbackend.gcsbackend.wsgi import application as app

# also provide `handler` as an alias (Vercel accepts either `app` or `handler`)
handler = app
