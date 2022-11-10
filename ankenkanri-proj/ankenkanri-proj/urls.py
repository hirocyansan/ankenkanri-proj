from django.contrib import admin
from django.urls import path, include
# import ankenkanri.views   # add
#from django.contrib.auth import views as auth_views    # 追加

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('ankenkanri.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  #追加
    # path('accounts/password_change_form/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change_form'),    # 追加
    # path('accounts/password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_finish.html'), name='password_change_done'), # 追加
]
