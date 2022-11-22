from asyncio.windows_events import NULL
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE','first_project.settings')
from django import setup
setup()

from first_app.models import AnkenStatus
# AnkenList.objects.create(
a = AnkenStatus(
    
    ankenStatusCode= 99,
    
    ankenStatus = '親案件用'
)

a.save(force_insert=True)