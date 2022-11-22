from asyncio.windows_events import NULL
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE','first_project.settings')
from django import setup
setup()

from first_app.models import AnkenTorihikisaki
# AnkenList.objects.create(
a = AnkenTorihikisaki(
    
    ankenTorihikisakiCode = 100000,
    ankenTorihikisakiKaisha = '',
    ankenTorihikisakiTantosha ='' 
    
)

a.save(force_insert=True)