from django.contrib import admin
from django.urls import path

from .views import views1
from .views import views2
from .views import views3
from .views import views4
from .views import viewsa
                             
urlpatterns = [
#    path('logout/', views1.logout_view, name='logout'),  
#    path('ankenkanri/logIn/', views1.logIn, name='logIn'), 

    path('ankenkanri/number_treat/', views1.number_treat, name='number_treat'),    
    path('ankenkanri/page_n/', views1.page_n, name='page_n'), 
    path('ankenkanri/page_n0/', views1.page_n0, name='page_n0'),
    path('ankenkanri/top_menu/', views1.top_menu, name='top_menu'),  
    
    path('ankenkanri/search/', views3.search, name='search'),
    path('ankenkanri/searchExec', views3.searchExec, name='searchExec'),

    path('ankenkanri/variousSettings/', views1.variousSettings, name='variousSettings'),  
#    path('ankenkanri/changePasswordPost/', views1.changePasswordPost, name='changePasswordPost'),  

    path('ankenkanri/views1/', views1.initialStart, name='initialStart'),
    path('ankenkanri/page_n', views1.page_n, name='page_n'),
    path('ankenkanri/ankenNyuuryokuKan1', views1.ankenNyuuryokuKan1, name='ankenNyuuryokuKan1'),
    path('ankenkanri/mitsumorisyoIraiKan2', views1.mitsumorisyoIraiKan2, name='mitsumorisyoIraiKan2'),
    path('ankenkanri/mitumorisyoNyuusyuKan3', views1.mitumorisyoNyuusyuKan3, name='mitumorisyoNyuusyuKan3'),
    path('ankenkanri/ringiShoninKan4', views1.ringiShoninKan4, name='ringiShoninKan4'),
    path('ankenkanri/keiyakusyoSakuseiKan5', views1.keiyakusyoSakuseiKan5, name='keiyakusyoSakuseiKan5'),
    path('ankenkanri/keiyakusyoTeiketsuKan6', views1.keiyakusyoTeiketsuKan6, name='keiyakusyoTeiketsuKan6'),
    path('ankenkanri/cyuumonKan7', views1.cyuumonKan7, name='cyuumonKan7'),
    path('ankenkanri/nouhinKan8', views1.nouhinKan8, name='nouhinKan8'),
    path('ankenkanri/seikyuusyoNyuusyu9', views1.seikyuusyoNyuusyu9, name='seikyuusyoNyuusyu9'),
    path('ankenkanri/shiharaiKan10', views1.shiharaiKan10, name='shiharaiKan10'),

    path('ankenkanri/mitsumoriSave', views4.mitsumoriSave, name='mitsumoriSave'),
    path('ankenkanri/ringiShoninSave', views4.ringiShoninSave, name='ringiShoninSave'),
    path('ankenkanri/keiyakusyoSakuseiSave', views4.keiyakusyoSakuseiSave, name='keiyakusyoSakuseiSave'),
    path('ankenkanri/keiyakusyoTeiketsuSave', views4.keiyakusyoTeiketsuSave, name='keiyakusyoTeiketsuSave'),
    path('ankenkanri/cyuumonSave', views4.cyuumonSave, name='cyuumonSave'),
    path('ankenkanri/nouhinSave', views4.nouhinSave, name='nouhinSave'),
    path('ankenkanri/seikyuusyoSave', views4.seikyuusyoSave, name='seikyuusyoSave'),
    path('ankenkanri/shiharaiSave', views4.shiharaiSave, name='shiharaiSave'),
    path('ankenkanri/kingakuW', views4.kingakuW, name='kingakuW'),
    path('ankenkanri/kingakuW2', views4.kingakuW2, name='kingakuW2'),

    path('ankenkanri/kingakuInputAgain', views4.kingakuInputAgain, name='kingakuInputAgain'),
    path('ankenkanri/kingakuInputAgain2', views4.kingakuInputAgain2, name='kingakuInputAgain2'),

    path('ankenkanri/service_start', views1.service_start, name='service_start'),
    path('ankenkanri/terminate', views1.terminate, name='terminate'),
    path('ankenkanri2/editOperation', viewsa.editOperation, name='editOperation'),    

    # path('ankenkanri2/hello', viewsa.index, name='index'),
    path('ankenkanri2/index', viewsa.index, name='index'),
    path('ankenkanri2/home', viewsa.home, name='home'),
    path('ankenkanri2/sample', viewsa.sample, name='sample'),
    path('ankenkanri2/sample3', viewsa.sample3, name='sample3'),
    path('ankenkanri2/import', viewsa.dataimport, name='import'),
    path('ankenkanri2/export', viewsa.dataexport, name='export'),
    path('ankenkanri2/export2', viewsa.export2, name='export2'),
    path('ankenkanri2/import2', viewsa.import2, name='import2'),
    path('ankenkanri2/edit', viewsa.edit, name='edit'),
    path('ankenkanri2/edit2', viewsa.edit2, name='edit2'),
    path('ankenkanri2/edit3', viewsa.edit3, name='edit3'),
    
    # path('ankenkanri2/import3', viewsa.import3, name='import3'),
]
print("currently, 'urls.py' last line!!")