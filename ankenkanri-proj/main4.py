from asyncio.windows_events import NULL
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE','ankenkanri-proj.settings')
from django import setup
setup()

from ankenkanri.models import AnkenTantosha
# AnkenList.objects.create(
a = AnkenTantosha(
    
    ankenTantoshaCode = 00000,
    ankenTantoshaMei = ''
    
)

a.save(force_insert=True)