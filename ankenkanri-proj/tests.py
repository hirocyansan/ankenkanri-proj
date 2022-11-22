## これは、サンプルプログラムです。

from django.test import TestCase
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','bookproject.settings')
from django import setup
from django.db.models import Q     # OR検索を使うためQクラスをインポートする
import time
from datetime import datetime, timedelta
from django.utils import timezone

def referLineNoGet(ankenList):  ## コピーする（挿入する手前のレコードNo.）を取得
    edabanTemp = 0
    referLineNo = 1
    for row in ankenList:
        if(row.edaban is None) or (row.edaban ==""):
            pass
        elif row.edaban == 0:
            edabanTemp = row.edaban
            baseAnkenMei = row.ankenMei
        elif row.edaban > edabanTemp:
            edabanTemp = row.edaban
        else:
            break
        referLineNo = referLineNo + 1
    print('referLineNo =', referLineNo)
    return referLineNo, baseAnkenMei

def insert1Line(lenAnkenList, insertRow, insertHyojijun, insertAnkenMei):
    ankn, created = AnkenList.objects.update_or_create(
        hyojijun = lenAnkenList + 1,         ## hyojijunがankenList長+1のレコードがあれば修正
                                           ## それはあるわけないので、新規に1レコード追加される
        defaults = {
            'keiriShonin': insertRow[0].keiriShonin,
            'statusCode' : 1,
            'status' : '案件入力済',  
            'edabanGroup': insertRow[0].edabanGroup,
            'shiharaiPattern': insertRow[0].shiharaiPattern,
            'kanriNo': insertRow[0].kanriNo,  
            'edaban': insertRow[0].edaban + 1,  
            'ankenMei': insertAnkenMei ,  ####     自動枝番タイトルの付け方？？
            'torihikisakiCode': insertRow[0].torihikisakiCode, 
            'torihikisakiMei': insertRow[0].torihikisakiMei,  
            'kanjokamoku': insertRow[0].kanjokamoku,  
            'keikakuTanka': insertRow[0].keikakuTanka, 
            'keikakuSuu': insertRow[0].keikakuSuu, 
            'keikakuGokei': insertRow[0].keikakuGokei, 
            'mitsumoriTanka': insertRow[0].mitsumoriTanka, 
            'mitsumoriSuu': insertRow[0].mitsumoriSuu, 
            'mitsumoriGokei': insertRow[0].mitsumoriGokei, 
            'mitsumoriLink': insertRow[0].mitsumoriLink,  
            'ringiTanka': insertRow[0].ringiTanka, 
            'ringiSuu': insertRow[0].ringiSuu, 
            'ringiGokei': insertRow[0].ringiGokei, 
            'ringishoNo': insertRow[0].ringishoNo,  
            'ringishoLink': insertRow[0].ringishoLink,  
            'wfNo': insertRow[0].wfNo,  
            'keiyakuKingaku': insertRow[0].keiyakuKingaku, 
            'keiyakushoNo': insertRow[0].keiyakushoNo,  
            'keiyakushoLink': insertRow[0].keiyakushoLink,  
            'onatsuRingiNo': insertRow[0].onatsuRingiNo,  
            'onatsuRingiLink': insertRow[0].onatsuRingiLink,  
            'chumonTanka': insertRow[0].chumonTanka, 
            'chumonSuu': insertRow[0].chumonSuu, 
            'chumonGokei': insertRow[0].chumonGokei, 
            'chumonLink': insertRow[0].chumonLink,  
            'nohinKigen': insertRow[0].nohinKigen,  
            'kenshuKigen': insertRow[0].kenshuKigen,  
            'shiharaiKigen': insertRow[0].shiharaiKigen + timedelta(days=MARGIN_DAYS),  
            'nohinTanka': insertRow[0].nohinTanka, 
            'nohinSuu': insertRow[0].nohinSuu, 
            'nohinGokei': insertRow[0].nohinGokei, 
            'nohinLink': insertRow[0].nohinLink,  
            'shiharaiTanka': insertRow[0].shiharaiTanka, 
            'konyuSuu': insertRow[0].konyuSuu, 
            'konyuGokei': insertRow[0].konyuGokei, 
            'seikyushoLink': insertRow[0].seikyushoLink,  
            'keikaku_Jisseki': insertRow[0].keikaku_Jisseki, 
            'kurikaeshiKigen': insertRow[0].kurikaeshiKigen,  
            'konyuKaisha': insertRow[0].konyuKaisha,  
            'dataKoshinbi': insertRow[0].dataKoshinbi,  
            'saishuKoshinsha': insertRow[0].saishuKoshinsha,  
            'shainNo': insertRow[0].shainNo, 
            'tantosha': insertRow[0].tantosha,  
            'comment': insertRow[0].comment,  
            'hyojijun': insertHyojijun, 
        }
    )

def hyojijunInc(insertHyojijun, ankenList):    ## 挿入した行以下のhyojijunを1行ずつ繰り下げる
    for row in ankenList:
        if row.hyojijun >= insertHyojijun:
            AnkenList.objects.filter(hyojijun=row.hyojijun).update(
                hyojijun = row.hyojijun + 1
            )

setup()
from book.models import AnkenList

ankenList = AnkenList.objects.all()

## edaban=0のレコードを取り出す >> edaban0List
edaban0List = []
for row in ankenList:
    if int(row.edaban) != 0:
        continue
    else:
        edaban0List.append(row.id)

print('edaban0List =', edaban0List)

## edaban0Listの全idに対して、夫々、edaban値最大レコード >> edabanMaxIdList
edabanMaxIdList = list(edaban0List)  ## edabanMaxIdListを新規に作る

baseAnkenMeiList = []
i = 0
for row1 in edaban0List:
    print('■i =', i)
    edaban0Record = AnkenList.objects.filter(id=row1)  ## edaban=0のレコードを取り出す
    baseAnkenMeiList.append(edaban0Record[0].ankenMei) ## edaban=0の案件名を取り出す
    for row2 in ankenList:
        print('row1 =', row1)
        print('row2 =', row2.id)
        if AnkenList.objects.filter(id=row1)[0].kanriNo !=  AnkenList.objects.filter(id=row2.id)[0].kanriNo:
            print('L131 id not equal!')   ## ankenListのレコードから
            pass                          ## edaban0Listと同じkanriNoレコードを探す

        elif int(AnkenList.objects.filter(id=edabanMaxIdList[i])[0].edaban) >= int(row2.edaban): 
            print('row1 =',  row1)
            print('row2.edaban =', row2.edaban) 
            print('L137 current edaban greater!')
            pass
        else:
            edabanMaxIdList[i] = row2.edaban
            print('edabanMaxIdList =', edabanMaxIdList)
    i = i + 1
print('baseAnkenMeiList =', baseAnkenMeiList)
print('edabanMaxIdList =', edabanMaxIdList)
referIdList = edabanMaxIdList

## 全edabanMaxIdListに対して、支払期限を調べ自動生成すべきか確認する

MARGIN_DAYS = 90
i = 0
for row in referIdList:
    sPattern = AnkenList.objects.filter(id=row)[0].shiharaiPattern
    kigen = AnkenList.objects.filter(id=row)[0].kurikaeshiKigen
    print('kigen =', kigen)
    if (sPattern == 3 or sPattern == 5) or \
        ((sPattern == 2 or sPattern == 4) and (timezone.now() < kigen)):

        print('i =', i)
        insertRow = AnkenList.objects.filter(id=row)
        print('insertRow =', insertRow)
        if timezone.now() >= insertRow.shiharaiKigen - timedelta(days=MARGIN_DAYS):
            insertHyojijun = insertRow.hyojijun + 1  ## 挿入行の表示位置は、参照行の下
            print('insertHyojijun =', insertHyojijun)
            if int(insertRow.edaban) == 0:    ## 案件名の生成
                insertAnkenMei = baseAnkenMeiList[i]  + '(初期費用)'
            else:
                insertAnkenMei = baseAnkenMeiList[i] + '(支払期限= )' \
                        + insertRow[0].shiharaiKigen + timedelta(days=MARGIN_DAYS)
            lenAnkenList = len(ankenList)
            insert1Line(lenAnkenList, insertRow, insertHyojijun, insertAnkenMei) 
                                                   ## 枝番レコードを1レコード追加
            hyojijunInc(insertHyojijun, ankenList) ## 挿入レコード以下のhyojijunを+1 
        i = i + 1

# referLineNo, baseAnkenMei = referLineNoGet(ankenList) 
# print('referLineNo =', referLineNo)
# print('baseAnkenMei =', baseAnkenMei)
# insertRow = AnkenList.objects.filter(id=referLineNo)
# print('isertRow =', insertRow)
# #for row in ankenListI:
# #    print('keiriShonin =', row.keiriShonin)


# print('timezone.now() =', timezone.now())

# for row in ankenList:     ### 自動挿入タイミングを過ぎていたら、1レコード挿入
#     print('row.shiharaiKigen =', row.shiharaiKigen)
#     print('shiharaiKigen - timedelta =', row.shiharaiKigen - timedelta(days=MARGIN_DAYS))
#     if timezone.now() >= row.shiharaiKigen - timedelta(days=MARGIN_DAYS):
#         print('create the new record !')
#         insertPosition = len(ankenList) + 1  ## レコード追加位置設定（最終行の下）
#         if row.edaban == 1:    ## 案件名の生成
#             row.ankenMei = insertRow[0].ankenMei + '(初期費用)'
#         else:
#             row.ankenMei = baseAnkenMei + '(支払期限= )' + insertRow[0].shiharaiKigen + timedelta(days=MARGIN_DAYS)
#         insert1Line(insertRow, insertPosition)  ## 枝番レコードを1レコード追加する。 


# Create your tests here.


##### time　を使った場合

# t = time.time()  # UNIX時間（1970/01/01 00:00:00からの経過時刻）を取得
# dt_from_timestamp = datetime.datetime.fromtimestamp(t)
# print(dt_from_timestamp)  # 2021-10-29 16:59:04.741680


##### datetime　を使った場合

# インポート必須


# 比較対象のDateTime
#print(post.created_at)
# 結果：2018-07-06 19:36:52.949309+00:00

# 現在日時
print(timezone.now())
# 結果：2018-07-06 19:38:56.865944+00:00

# 現在日時 - 1日
print(timezone.now() - timedelta(days=1))
# 結果：2018-07-05 19:38:56.865964+00:00



# inStatusCodeL = [ 3, 2, 1, 4, 10, 20]
# inKeiriShoninL = [True]
# inKanriNoL = ['S22-001', 'S22-002', 'S22-003', 'S22-004']
# inEdabanGroupL = [0, 1, 2]
# inEdabanL = [0, 1, 2, 3]
# inAnkenMeiL = ['BPO定型業務委託', '本社～VPN費用', 'Microsoft365ライセンス追加', 'Intune導入']
# inTorihikisakiMeiL = ['コムテック', '富士通JAPAN株式会社', '(株)大塚商会']
# inkonyuKaishaL = ['TRK', '全社', 'KTS']

# # OR検索は、１つの項目内のみ
# k = 'statusCode'
# q = AnkenList.objects.filter(statusCode__in=inStatusCodeL).order_by(k)
# print ('q = ', q)

# # AND検索は、項目内がORで、項目間がAND
# k = 'kanriNo'
# r = AnkenList.objects.filter(statusCode__in=inStatusCodeL, \
#                              keiriShonin__in=inKeiriShoninL, \
#                              kanriNo__in=inKanriNoL, \
#                              edabanGroup__in=inEdabanGroupL, \
#                              edaban__in=inEdabanL, \
#                              ankenMei__in=inAnkenMeiL, \
#                              torihikisakiMei__in=inTorihikisakiMeiL, \
#                              konyuKaisha__in=inkonyuKaishaL ).order_by(k).reverse()
# print('r = ', r)

### filterテスト
    # print('qq1_ref = ', AnkenList.objects.filter(Q(kanriNo__icontains='S22-001')|  \
    #                                             Q(kanriNo__icontains='S22-002')|  \
    #                                             Q(kanriNo__icontains='S22-003')|  \
    #                                             Q(kanriNo__icontains='S22-004')|  \
    #                                             Q(kanriNo__icontains='S22-005')))
    # print('qq2_ref =', AnkenList.objects.filter(Q(kanriNo__icontains="S22-001")|Q(kanriNo__icontains="S22-002")|Q(kanriNo__icontains="S22-003")|Q(kanriNo__icontains="S22-004")|Q(kanriNo__icontains="S22-005")))
    # i = 1
    # r =""
    # for row in q1:
    #     if len(q1) > i:
    #         temp = 'Q(kanriNo__icontains=' + '"' + row + '"' + ')|'
    #         r = r + temp
    #     else:
    #         temp = 'Q(kanriNo__icontains=' + '"' + row + '"' + ')'
    #         r = r + temp
    #     i = i + 1
    # print('r =', r)
    # qq1 = AnkenList.objects.filter(r)
    # print('qq1 =',qq1)


# def checked(value, question):
#     if (not question) or (value != question):   # questionがブランク、valueとquestionが違えば戻る
#         return ""
#     else:
#         return "checked"

# question = "andSearch"

# print("サーチタイプは", checked("andSearch", question))

# list1 = set()  # statusCode検索結果のレコードリスト 
# for row in inStatusCodeL:
#     list1.add(AnkenList.objects.filter(statusCode=row))


# print("statusCode検索結果 =")
# print(list1)

# list2 = []  # keiriShonin検索結果のレコードリスト 
# for row in inKeiriShoninL:
#     list2 = AnkenList.objects.filter(keiriShonin=row)
# print("list2 =", list2)

# print("keiriShonin検索結果 =")
# listx = []
# j = 0
# for i in range(len(list2[0])):
#     listx.append(list2[0][j])
#     print("j =",j, " listx =",listx)
#     j = j + 1
# print("listx =",listx)

# # intersection sample
# # set1 = {'python', 'java', 'c#'}
# # set2 = {'java', 'python'}
# # set3 = {'php', 'python'}
# # q = set1.intersection(set2, set3)
# # print('q =', q)

# r= set(list2).intersection(set(list1))
# print('r =', r)

# listAnd = []  # AND検索結果のレコードリスト
# for list1Row in list1:
#     for list2Row in list2:
#         print('id1 =', list1Row[0].id, 'id2 =', list2Row[0].id)
#         if list1Row[0].id == list2Row[0].id:
#             listAnd.append(list1Row[0].id)
# for row in listAnd:
#     print("AND_list =", row)

# listOr = []  # OR検索結果のレコードリスト
# for list1Row in list1:
#     flag = 1
#     if listOr == []:
#         listOr.append(list1Row)
#     for row in listOr:
#         if row[0].id == list1Row[0].id:
#             flag = 0
#     if flag == 1:
#         listOr.append(list1Row)
# for row in listOr:
#     print("OR_list =", row)


# for j in q:
#     print('q =', j)
# q = []
# r = []
# q = AnkenList.objects.filter(statusCode=4)
# print("test =", q)
# r = AnkenList.objects.filter(pk=1)
# print("test =", r)
# s = AnkenList.objects.get(pk=3)
# print("test =", s.pk)


# j = 0
# query = "("
# for row in inStatusCodeL:
#     if j == len(inStatusCodeL) - 1:
#         query = query + "Q(statusCode=" + "str(" + str(row) + "))"
#     else:
#         query = query + "Q(statusCode=" + "str(" + str(row) + "))|"
#     j = j + 1
# j = 0
# query = query + ")"

# print('query =', query)
# print("filtered =", AnkenList.objects.filter(Q(statusCode=1)|Q(statusCode=2)|Q(statusCode=3)))
# print("filtered_f =", AnkenList.objects.filter(query))



###　以下サンプルコード

# 文字列をリストに分割する
# c = "one、two、three"

# l = c.split('、')
# print(l)
# print(l[0])
# print(l[1])
# print(l[2])

#　リストの長さを調べる
#j = len(inStatusCodeL) - 1

#リストに要素を追加するにはappendを使う
#        q.append("Q(statusCode=" + "str(" + str(row) + "))")