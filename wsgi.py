import sys
import os
import os.path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            'tennis_mockup')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_mockup.settings')
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
