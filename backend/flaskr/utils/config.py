import os

class Config:
    ROUTE = os.environ.get('ROUTE')
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    SITE_URL = os.environ.get('SITE_URL')
    SITE_NAME = os.environ.get('SITE_NAME')