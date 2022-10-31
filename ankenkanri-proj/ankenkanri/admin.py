from django.contrib import admin
from .models import AnkenList
from .models import AnkenStatus
from .models import AnkenShiharaiPattern
from .models import AnkenTorihikisaki
from .models import AnkenTantosha
from .models import AnkenKanjokamoku
# Register your models here.

admin.site.register(AnkenList)
admin.site.register(AnkenStatus)
admin.site.register(AnkenShiharaiPattern)
admin.site.register(AnkenTorihikisaki)
admin.site.register(AnkenTantosha)
admin.site.register(AnkenKanjokamoku)














