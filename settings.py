import os

PINGPANTHER_ROOT = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(PINGPANTHER_ROOT, 'pingpanther.db')
CRON_FREQUENCY = 1
UPDATE_URL = "<uenter pdate url>"
COOKIES_SECRET_KEY = 'pingpanther123'
TWILIO_ACCOUNT = "<enter twilio account here>"
TWILIO_TOKEN = "<enter twilio token>"

try:
    from local_settings import *
except ImportError:
    pass
