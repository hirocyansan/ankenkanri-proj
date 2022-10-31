from asyncio.windows_events import NULL
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE','first_project.settings')
from django import setup
setup()

from first_app.models import AnkenTantosha
# AnkenList.objects.create(
a = AnkenTantosha(
    
    ankenTantoshaCode = 00000,
    ankenTantoshaMei = ''
    
)

a.save(force_insert=True)