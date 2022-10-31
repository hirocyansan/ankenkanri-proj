from asyncio.windows_events import NULL
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ankenkanri-proj.settings')
from django import setup
setup()
from ankenkanri.models import AnkenList
# AnkenList.objects.create(
a = AnkenList(
    keiriShonin= True,
    statusCode= 10,
    status= '支払処理(完了）',

    shiharaiPattern= 1,
    kanriNo= 'S22-031',
    edaban= 1,
    ankenMei= 'GMOサイン初期費用',
    torihikisakiCode= 300005,
    torihikisakiMei= 'GMO',
    kanjokamokuCode= 10080,
    kanjokamoku= '研究費',
    keikakuTanka= 3598752,
    keikakuSuu= 1,
    keikakuGokei= 3598752,
    mitsumoriTanka= 3598752,
    mitsumoriSuu= 1,
    mitsumoriGokei= 3598752,
    mitsumoriLink= 'https://advantec-group.ent.box.com/file/925364524384、https://advantec-group.ent.box.com/file/925858622263',
    ringiTanka= 3598752,
    ringiSuu= 1,
    ringiGokei= 3598752,
    ringishoNo= '2022-0654',
    ringishoLink= 'https://advantec-group.ent.box.com/file/925364706508',
    wfNo= '稟議-2022-0654',
    keiyakuKingaku= 3260510,
    keiyakushoNo= '2270-059204',
    keiyakushoLink= 'https://advantec-group.ent.box.com/folder/157941386211',
    onatsuRingiNo= 'onatsu-020',
    onatsuRingiLink= 'https://advantec-group.ent.box.com/folder/157941386211',
    chumonTanka= 3598752,
    chumonSuu= 1,
    chumonGokei= 3598752,
    chumonLink= 'https://advantec-group.ent.box.com/folder/157941386211',
    nohinKigen= '2022-10-1 00:00',
    shiharaiKigen= '2022-12-28 00:00',
    nohinTanka= 3598752,
    nohinSuu= 1,
    nohinGokei= 3598752,
    nohinLink= 'https://advantec-group.ent.box.com/folder/157941386211',
    shiharaiTanka= 3598752,
    konyuSuu= 1,
    konyuGokei= 3598752,
    seikyushoLink= 'https://advantec-group.ent.box.com/folder/157941386211',
    keikaku_Jisseki= 99999999,

    konyuKaisha= 'KTS',
    dataKoshinbi= '2022-9-9 00:00',
    saishuKoshinsha= '荒木',
    shainNo= '12345',
    tantosha= '市ノ川',
    comment= 'Its a fine day,Today!',
    hyojijun= 8












































)
a.save(force_insert=True)