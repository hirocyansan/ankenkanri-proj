from asyncio.windows_events import NULL
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE','first_project.settings')
from django import setup
setup()

from first_app.models import AnkenKanjokamoku
# AnkenList.objects.create(
a = AnkenKanjokamoku(
    
    ankenKanjokamokuCode = 10000,
    ankenKanjokamoku = ''
    
)

a.save(force_insert=True)