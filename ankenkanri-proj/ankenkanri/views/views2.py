# from curses.ascii import isspace
#import views

from re import S
from django import forms
from tkinter.tix import Tree
from django.shortcuts import redirect, render

#from symbol import pass_stmt
#from django.http import HttpResponse
from .. import forms
from django.views.generic import TemplateView
from ..models import AnkenList
from django.db.models import Q
from functools import reduce
from operator import and_ # 論理演算子をインポート
from operator import or_ 
import time
from datetime import datetime, timedelta, date
import calendar
from dateutil.relativedelta import relativedelta
from dateutil import tz
from django.utils import timezone
JST = tz.gettz('Asia/Tokyo')
UTC = tz.gettz("UTC")

## 　ある月の月末の日を割り出す
def get_last_date(dt):
    return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])

## 参照行(insertRow)のデータなどをコピーし、自動登録する行にデータを設定する
def insert1Line(lenAnkenList, insertRow, newEdaban, insertHyojijun, insertAnkenMei, newKigen):
                                             ## hyojijunがankenList長+1のレコードがあれば修正
                                             ## それはあるわけないので、新規に1レコード追加される

    ankn, created = AnkenList.objects.update_or_create(
        hyojijun = 10000,        
        defaults = {
            'keiriShonin': insertRow[0].keiriShonin,
            'statusCode' : 1,
            'status' : '案件入力完',  
            'edabanGroup': insertRow[0].edabanGroup,
            'shiharaiPattern': insertRow[0].shiharaiPattern,
            'kanriNo': insertRow[0].kanriNo,  
            'edaban': newEdaban,  
            'ankenMei': insertAnkenMei ,  
            'torihikisakiCode': insertRow[0].torihikisakiCode, 
            'torihikisakiMei': insertRow[0].torihikisakiMei,  
            'kanjokamoku': insertRow[0].kanjokamoku,  
            'keikakuTanka': insertRow[0].keikakuTanka, 
            'keikakuSuu': insertRow[0].keikakuSuu, 
            'keikakuGokei': insertRow[0].keikakuGokei, 
            'mitsumoriTanka': insertRow[0].mitsumoriTanka, 
            'mitsumoriSuu': insertRow[0].mitsumoriSuu, 
            'mitsumoriGokei': insertRow[0].mitsumoriGokei, 
            'mitsumoriLink': "",  
            'ringiTanka': insertRow[0].ringiTanka, 
            'ringiSuu': insertRow[0].ringiSuu, 
            'ringiGokei': insertRow[0].ringiGokei, 
            'ringishoNo': insertRow[0].ringishoNo,  
            'ringishoLink': insertRow[0].ringishoLink,  
            'wfNo': "",  
            'keiyakuKingaku': insertRow[0].keiyakuKingaku, 
            'keiyakushoNo': insertRow[0].keiyakushoNo,  
            'keiyakushoLink': insertRow[0].keiyakushoLink,  
            'onatsuRingiNo': insertRow[0].onatsuRingiNo,  
            'onatsuRingiLink': insertRow[0].onatsuRingiLink,  
            'chumonTanka': insertRow[0].chumonTanka, 
            'chumonSuu': insertRow[0].chumonSuu, 
            'chumonGokei': insertRow[0].chumonGokei, 
            'chumonLink': insertRow[0].chumonLink,  
            #'nohinKigen': ,  
            #'kenshuKigen': ,  
            'shiharaiKigen': newKigen,  
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
            'dataKoshinbi': timezone.now(),  
            'saishuKoshinsha': "system",  
            'shainNo': insertRow[0].shainNo, 
            'tantosha': insertRow[0].tantosha,  
            'comment': "",  
            'hyojijun': insertHyojijun, 
        }
    )

    return

## 挿入したレコード以下の行(hyojijun)を+1行ずつインクリメントする。
def hyojijunInc(insertHyojijun):    ## 挿入した行以下のhyojijunを1行ずつ繰り下げる
    ankenList = AnkenList.objects.order_by('hyojijun')
    for row in ankenList:
        if row.hyojijun >= insertHyojijun:
            row.hyojijun = row.hyojijun + 1
            row.save()
    return

## レコードの支払期限まで一定期間内(WARNING_MSG_DAYS)のものをリストアップする
def warningCheck(request, ankenList):
    # ankenList = AnkenList.objects.all()
    WARNING_MSG_DAYS = 14
    ON = True
    OFF = False
    messageFlag = []
    # today = date.today()
    today = timezone.now()

    for row in ankenList:
        #a = row.shiharaiKigen
        #b = timedelta(days=WARNING_MSG_DAYS)
        #c = row.shiharaiKigen - timedelta(days=WARNING_MSG_DAYS)   ## !! for debug
        if row.shiharaiKigen == None:
            messageFlag.append(OFF)
        elif today >= (row.shiharaiKigen - timedelta(days=WARNING_MSG_DAYS)):
            messageFlag.append(ON)
        else:
            messageFlag.append(OFF)
    request.session['sessionMessageFlag'] = 'messageFlag'

## これから自動登録するレコードが既にDBに存在しないことを確認
def sameRecordCheck(insertRow, ankenList):
    for row in ankenList:
        nextEdaban = int(insertRow[0].edaban) + 1
        nextEdaban = str(nextEdaban)
        if (insertRow[0].kanriNo == row.kanriNo) and (nextEdaban == row.edaban):
            return "Exist"
    return "None"

## 全レコードに対して枝番自動生成の条件をチェックして、枝番を生成する。
def edabanCreateCheck(request):
    ankenList = AnkenList.objects.all()

    ## edaban=0のレコード(のid)を取り出す >> edaban0List
    edaban0List = []
    for row in ankenList:
        #if int(row.edaban) != 0 or (row.edaban is None) or row.edaban =="":
        if row.edaban is None or int(row.edaban) != 0:
            continue
        else:
            edaban0List.append(row.id)

    print('edaban0List =', edaban0List)

    ## edaban0Listの全idに対して、夫々、edaban値最大レコード >> edabanMaxIdList
    edabanMaxIdList = list(edaban0List)  ## edabanMaxIdListを新規に作る

    baseAnkenMeiList = []
    i = 0
    for row1 in edaban0List:
        #print('■i =', i)
        edaban0Record = AnkenList.objects.filter(id=row1)  ## edaban=0のレコードを取り出す
        baseAnkenMeiList.append(edaban0Record[0].ankenMei) ## edaban=0の案件名を取り出す
        for row2 in ankenList:
            if row2.edaban is None:
                continue
            #print('edaban0Record =', AnkenList.objects.filter(id=row1)[0].kanriNo)
            #print('ankenList(all) =', row2.kanriNo)
            if AnkenList.objects.filter(id=row1)[0].kanriNo !=  row2.kanriNo:  ## edaban0レコードとankenList（から1レコードずつ取り出した）kanriNoを比較
                #print('L131 id not equal!')   ## ankenListのレコードから
                pass                          ## edaban0Listと同じkanriNoレコードを探す

            elif int(AnkenList.objects.filter(id=edabanMaxIdList[i])[0].edaban) >= int(row2.edaban): ## edabanMaxIdListとankenListのedabanを比較
                #print('(edaban0Record)id =',  row1)        
                #print('ankenList(all)id =', row2.edaban) 
                #print('L137 current edaban greater!')
                pass
            else:
                edabanMaxIdList[i] = row2.id
                #print('edabanMaxIdList =', edabanMaxIdList)
        i = i + 1
    print('baseAnkenMeiList =', baseAnkenMeiList)
    print('edabanMaxIdList =', edabanMaxIdList)
    referIdList = edabanMaxIdList

    ## 支払期限前ワーニングメッセージ表示

    warningCheck(request, ankenList)

    ## 全referIdListに対して、支払期限のMARGIN_DAYSを超えている場合1行自動生成

    MARGIN_MONTHS = 3
    i = 0
    today = timezone.now() 
    dt = today + relativedelta(months=1) - timedelta(days=today.day)
    for referId in referIdList:
        insertRow = AnkenList.objects.filter(id=referId)
        print('insertRow =', insertRow)
        sPattern = AnkenList.objects.filter(id=referId)[0].shiharaiPattern
        if sPattern == 2 or sPattern ==3:
            a = insertRow[0].shiharaiKigen
            b = relativedelta(months=1)   
            newKigen = get_last_date(insertRow[0].shiharaiKigen + relativedelta(months=1))
        else:
            a = insertRow[0].shiharaiKigen
            b = relativedelta(years=1)
            c = a + b 
            d = timedelta(days=today.day)         
            newKigen = get_last_date(insertRow[0].shiharaiKigen + relativedelta(years=1)) 
        print('newKigen =', newKigen)
        if (sPattern == 3 or sPattern == 5) or \
            ((sPattern == 2 or sPattern == 4) and (today < newKigen)):

            print('i =', i)

            ## 自動生成のタイムリミットを過ぎているか、既に自動生成されているか　のチェック
            c = relativedelta(months=MARGIN_MONTHS)
            d = newKigen - relativedelta(months=MARGIN_MONTHS)
            e = sameRecordCheck(insertRow, ankenList)

            if (today >= newKigen - relativedelta(months=MARGIN_MONTHS)) and \
                                      sameRecordCheck(insertRow, ankenList) == "None":
                insertHyojijun = insertRow[0].hyojijun + 1  ## 挿入行の表示位置は、参照行の下
                print('insertHyojijun =', insertHyojijun)

                ## 案件名の生成
                if int(insertRow[0].edaban) == 0:    
                    insertAnkenMei = baseAnkenMeiList[i]  + '(初期費用)'

                ## 支払期限は参照する行の支払期限＋1か月（又は＋1年）
                elif sPattern == 2 or sPattern ==3:
                    newKigen = get_last_date(insertRow[0].shiharaiKigen + relativedelta(months=1))    
                    #newKigen = insertRow[0].shiharaiKigen + relativedelta(months=1) 
                    newKigenJST = newKigen.astimezone(JST)
                    #insertAnkenMei = baseAnkenMeiList[i]
                    insertAnkenMei = baseAnkenMeiList[i] + '(支払期限： ' \
                            + str(newKigenJST) + ')'
                else:
                    newKigen = get_last_date(insertRow[0].shiharaiKigen + relativedelta(years=1))       
                    #newKigen = insertRow[0].shiharaiKigen + relativedelta(years=1)
                    #newKigenJST = newKigen.astimezone(JST)
                    #insertAnkenMei = baseAnkenMeiList[i]      
                    insertAnkenMei = baseAnkenMeiList[i] + '(支払期限： ' \
                            + str(newKigenJST) + ')'

                ## 1行自動挿入                    
                lenAnkenList = len(ankenList)
                newEdaban = str(int(insertRow[0].edaban) + 1)
                hyojijunInc(insertHyojijun) ## 挿入レコード以下のhyojijunを+1 
                insert1Line(lenAnkenList, insertRow, newEdaban, insertHyojijun, insertAnkenMei, newKigen) 
                                                    ## 枝番レコードを1レコード追加

        i = i + 1
    return()