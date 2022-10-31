from asyncio.windows_events import NULL
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE','first_project.settings')
from django import setup
setup()

from first_app.models import AnkenList
# AnkenList.objects.create(
AnkenList.objects.filter(
                    kanriNo= "S22-009",
                    edaban= 0
                ).delete()    
    
    
