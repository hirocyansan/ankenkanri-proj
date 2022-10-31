from django.contrib import admin
from django.urls import path, include
# import ankenkanri.views   # add

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('ankenkanri.urls')),
]
