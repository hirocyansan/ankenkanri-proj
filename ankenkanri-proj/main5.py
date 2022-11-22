from asyncio.windows_events import NULL
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE','ankenkanri-proj.settings')
from django import setup
setup()

from ankenkanri.models import AnkenKanjokamoku
# AnkenList.objects.create(
a = AnkenKanjokamoku(
    
    ankenKanjokamokuCode = 10000,
    ankenKanjokamoku = ''
    
)

a.save(force_insert=True)