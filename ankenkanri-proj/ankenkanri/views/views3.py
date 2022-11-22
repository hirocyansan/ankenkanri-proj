# from curses.ascii import isspace
import re
from re import S
from django import forms
from tkinter.tix import Tree
from django.shortcuts import redirect, render
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

def checked(value, question):
    if (not question) or (value != question):   # questionがブランク、valueとquestionが違えば戻る
        return ""
    else:
        return "checked"

def initialParam(request):
    request.session['sessionSearchType'] = 'andSearch'
    request.session['sessionSorting'] = 'sortAccounting'
    request.session['sessionDpList'] = 'keiriShonin'
    request.session['orderRule'] = 'orderAsc'
    request.session['sessionKeiriYN'] = ['1','0']
    request.session['sessionStatusL'] = ['案件入力中','','','','','','','','','','']

    # request.session['sessionStatusL'] = ['案件入力中', '案件入力完', '見積書作成依頼済', '見積書入手済', \
    #                                      '稟議書承認完了', '契約書作成完了', '契約書締結完了', '注文完了', \
    #                                      '納品完了', '請求書入手済', '支払処理完了' ]
    request.session['sessionKanriNoE'] = ''
    request.session['sessionAnkenM'] = ''
    request.session['sessionTorihikisakiM'] = ''
    request.session['sessionKonyuG'] = ''
    request.session['sessionTantoshaM'] = ''
    request.session['sessionSaisyuH'] = ''
    return()

## プルダウンリスト表示中に選択された項目をc25にセット
def setC25(request):
    if request.session['sessionDpList'] == 'keiriShonin':
        c25 = '経理部承認'
    elif request.session['sessionDpList'] == 'status':
        c25 = '案件ステータス'
    elif request.session['sessionDpList'] == 'kanriNo':
        c25 = '管理No.'
    elif request.session['sessionDpList'] == 'ankenMei':
        c25 = '案件名'
    elif request.session['sessionDpList'] == 'torihikisakiMei':
        c25 = '取引先名'
    elif request.session['sessionDpList'] == 'konyuKaisha':
        c25 = '購入会社'
    elif request.session['sessionDpList'] == 'tantosha':
        c25 = '担当者名'
    elif request.session['sessionDpList'] == 'saishuKoshinsha':
        c25 = '最終編集者'
    return c25

## 検索画面表示のためのcontext情報をセットする
def searchContextSet(request, q):
    question = request.session['sessionSearchType']
    value = "andSearch"
    c1 = checked(value, question)

    value = "orSearch"
    c2 = checked(value, question)

    question = request.session['sessionOrderRule']
    value = "orderAsc"
    c3 = checked(value, question)

    value = "orderDesc"
    c4 = checked(value, question)

    question = request.session['sessionKeiriYN']
    print('L115 keiriYN =', request.session['sessionKeiriYN'] )
    value = "1"
    c5 = checked(value, question[0])
    #print('L77 c5 =', c5)

    value = "0"
    c6 = checked(value, question[1])
    #print('L81 c6 =', c6)

    question = request.session['sessionStatusL']
    value = "案件入力中"
    c7 = checked(value, question[0])

    value = "案件入力完"
    c8 = checked(value, question[1])

    value = "見積書作成依頼済"
    c9 = checked(value, question[2])

    value = "見積書入手済"
    c10 = checked(value, question[3])

    value = "稟議書承認完了"
    c11 = checked(value, question[4])

    value = "契約書作成完了"
    c12 = checked(value, question[5])

    value = "契約書締結完了"
    c13 = checked(value, question[6])

    value = "注文完了"
    c14 = checked(value, question[7])

    value = "納品完了"
    c15 = checked(value, question[8])

    value = "請求書入手済"
    c16 = checked(value, question[9])

    value = "支払処理完了"
    c17 = checked(value, question[10])

    c18 = request.session['sessionSorting']
    c19 = request.session['sessionKanriNoE']
    c20 = request.session['sessionAnkenM']
    c21 = request.session['sessionTorihikisakiM']
    c22 = request.session['sessionKonyuG']
    c23 = request.session['sessionTantoshaM']
    c24 = request.session['sessionSaisyuH']

    c25 = setC25(request)  ## dummy!! ドロップダウンリスト

    context = {
        'c1' : c1,  'c2' :  c2, 'c3' :  c3, 'c4' :  c4, 'c5' :  c5,  'c6':  c6,
        'c7' : c7,  'c8' :  c8, 'c9' :  c9, 'c10': c10, 'c11': c11, 'c12': c12,
        'c13': c13, 'c14': c14, 'c15': c15, 'c16': c16, 'c17': c17, 'c18': c18,
        'c19': c19, 'c20': c20, 'c21': c21, 'c22': c22, 'c23': c23, 'c24': c24,
        'c25': c25,  'q'  : q,
    }
    return(context) 

def search(request):
    q = AnkenList.objects.all()
    context = searchContextSet(request, q)  # 検索条件の読み出し、設定
    request.session['sessionDisplayCode'] = 'dp200'
    return render(request, 'ankenkanri/search.html', context)

## リストqの要素にnullが含まれていたら、リスト要素を詰める
def nullDelete(q):
    qo = []
    for row in q:
        if row is None:
            continue
        else:
            qo.append(row)
    return(qo)

## 検索実行ボタンが押された
def searchExec(request):
    print('(searchExecL205)sessionDpList =', request.session['sessionDpList'])    

    q = AnkenList.objects.all()   
    context = searchContextSet(request, q)  
    request.session['sessionDisplayCode'] = 'dp200' 

    if "dataClear" in request.POST:    ## データクリアボタン検出
        initialParam(request) 
        q = AnkenList.objects.all()   
        context = searchContextSet(request, q)     
        return render(request, 'ankenkanri/search.html', context)
    
    ## ドロップリスト（並べ替え）から選択された項目をsessionにメモリする
    elif "keiriShonin" in request.POST:
        request.session['sessionDpList'] = "keiriShonin"
        context = searchContextSet(request, q)  
        searchParamResume(request)
        return render(request, 'ankenkanri/search.html', context)
    elif "status" in request.POST:
        request.session['sessionDpList'] = "status"
        context = searchContextSet(request, q)  
        print('(searchExec)sessionStatusL =',request.session['sessionStatusL'])
        searchParamResume(request)
        return render(request, 'ankenkanri/search.html', context)
    elif "kanriNo" in request.POST:
        request.session['sessionDpList'] = "kanriNo"
        context = searchContextSet(request, q)  
        print('(searchExecL227)sessionDpList =', request.session['sessionDpList'])    
        searchParamResume(request)
        return render(request, 'ankenkanri/search.html', context)
    elif "ankenMei" in request.POST:
        request.session['sessionDpList'] = "ankenMei"
        context = searchContextSet(request, q)       
        searchParamResume(request)
        return render(request, 'ankenkanri/search.html', context)
    elif "torihikisakiMei" in request.POST:
        request.session['sessionDpList'] = "torihikisakiMei" 
        context = searchContextSet(request, q)       
        searchParamResume(request)
        return render(request, 'ankenkanri/search.html', context)
    elif "konyuKaisha" in request.POST:
        request.session['sessionDpList'] = "konyuKaisha"  
        context = searchContextSet(request, q)    
        searchParamResume(request)
        return render(request, 'ankenkanri/search.html', context)
    elif "tantosha" in request.POST:
        request.session['sessionDpList'] = "tantosha" 
        context = searchContextSet(request, q)      
        searchParamResume(request)
        return render(request, 'ankenkanri/search.html', context)
    elif "saishuKoshinsha" in request.POST:
        request.session['sessionDpList'] = "saishuKoshinsha" 
        context = searchContextSet(request, q)     
        searchParamResume(request)
        return render(request, 'ankenkanri/search.html', context)
    else:
        pass
                                  # 以下、スタートボタンが押されたときの処理
    searchParamResume(request)    # 検索パラメータをメモリしておく
    q = AnkenList.objects.all()
    q1, q2, q3, q4, q5, q6 = [], [], [], [], [], []
    if request.POST['searchType'] == 'andSearch':
        for row in q:                 # AND検索でブランクの検索条件欄を無視するため、列データをフルに入れておく
            q1.append(row.kanriNo)
            q2.append(row.ankenMei)
            q3.append(row.torihikisakiMei)
            q4.append(row.konyuKaisha)
            q5.append(row.tantosha)
            q6.append(row.saishuKoshinsha)

    if "searchStart" in request.POST:  ###  入力された検索条件をリストに入れ直す(レジューム表示のため)

        if (request.POST.get('kanriNoE') is None) or (request.POST.get('kanriNoE') == ""):
           pass
        else:
            q1 = request.POST.get('kanriNoE')
            q1 = q1.replace(' ',';').replace('　',';')    ## 半角、全角ブランク→;へ変換
            q1 = re.split('[,;、]', q1)     ## セパレート文字列(,;、)で分離してLISTへ
        if (request.POST.get('ankenM') is None) or (request.POST.get('ankenM') == ""):
            pass
        else:
            q2 = request.POST.get('ankenM')
            q2 = q2.replace(' ',';').replace('　',';')    ## 半角、全角ブランク→;へ変換
            q2 = re.split('[,;、]', q2)
#        print('L204 =', request.session['sessionTorihikisakiM'] )
        if (request.POST.get('torihikisakiM') is None) or (request.POST.get('torihikisakiM') == ""):
            pass
        else:
            q3 = request.POST.get('torihikisakiM')
            q3 = q3.replace(' ',';').replace('　',';')    ## 半角、全角ブランク→;へ変換
            q3 = re.split('[,;、]', q3)
        if (request.POST.get('konyuG') is None) or (request.POST.get('konyuG') == ""):
            pass
        else:
            q4 = request.POST.get('konyuG')
            q4 = q4.replace(' ',';').replace('　',';')    ## 半角、全角ブランク→;へ変換
            q4 = re.split('[,;、]', q4)
        if (request.POST.get('tantoshaM') is None) or (request.POST.get('tantoshaM') == ""):
            pass
        else:
            q5 = request.POST.get('tantoshaM')
            q5 = q5.replace(' ',';').replace('　',';')    ## 半角、全角ブランク→;へ変換
            q5 = re.split('[,;、]', q5)
        if (request.POST.get('saisyuH') is None) or (request.POST.get('saisyuH') == ""):
            pass
        else:
            q6 = request.POST.get('saisyuH')
            q6 = q6.replace(' ',';').replace('　',';')    ## 半角、全角ブランク→;へ変換
            q6 = re.split('[,;、]', q6)

   ## リストの要素にNullがあれば削除する。
    q1 = nullDelete(q1) 
    q2 = nullDelete(q2)
    q3 = nullDelete(q3)
    q4 = nullDelete(q4)
    q5 = nullDelete(q5)
    q6 = nullDelete(q6)  

    print('q1 =', q1)
    print('q2 =', q2)
    print('q3 =', q3)
    print('q4 =', q4)
    print('q5 =', q5)
    print('q6 =', q6)

    checksKeiriCondition = request.POST.getlist('keiriYN') # 経理承認条件を配列に設定
    print('checksKeiriCondition =', checksKeiriCondition)
    checksAnkenStatus = request.POST.getlist('statusL') # 案件ステータス条件を配列に設定
    print('checksAnkenStatus =', checksAnkenStatus)
    orderItem = request.session['sessionDpList']

    print('L578 checksKeiriCondition =', checksKeiriCondition)
    aaa = reduce(or_, [Q(keiriShonin__icontains=q) for q in checksKeiriCondition])
    ya =  reduce(or_, [Q(status__icontains=q) for q in checksAnkenStatus])
    if q1 == []:
        q1 = [" "]
        y1 = reduce(or_, [Q(kanriNo__icontains=q) for q in q1])
    else:
        y1 = reduce(or_, [Q(kanriNo__icontains=q) for q in q1])
    if q2 == []:
        q2 = [" "]
        y2 = reduce(or_, [Q(ankenMei__icontains=q) for q in q2])
    else:
        y2 = reduce(or_, [Q(ankenMei__icontains=q) for q in q2])
    if q3 == []:
        q3 = [" "]
        y3 = reduce(or_, [Q(torihikisakiMei__icontains=q) for q in q3])
        print('searchExecL324 y3 =', y3)
    else:
        y3 = reduce(or_, [Q(torihikisakiMei__icontains=q) for q in q3])
    if q4 == []:
        q4 = [" "]
        y4 = reduce(or_, [Q(konyuKaisha__icontains=q) for q in q4])
    else:
        y4 = reduce(or_, [Q(konyuKaisha__icontains=q) for q in q4])
    if q5 == []:
        q5 = [" "]
        y5 = reduce(or_, [Q(tantosha__icontains=q) for q in q5])
    else:
        y5 = reduce(or_, [Q(tantosha__icontains=q) for q in q5])
    if q6 == []:
        q6 = [" "]
        y6 = reduce(or_, [Q(saishuKoshinsha__icontains=q) for q in q6])
    else:
        y6 = reduce(or_, [Q(saishuKoshinsha__icontains=q) for q in q6])

    print('L613 checksKeiriCondition =', checksKeiriCondition)
    print('経理承認 aaa =', aaa)
    print('案件ステータス ya =', ya)
    print('y1 =', y1)
    print('y2 =', y2)
    print('y3 =', y3)
    print('y4 =', y4)
    print('y5 =', y5)
    print('y6 =', y6)
    print('L622 経理承認　aaa(query) =', aaa)
    print('経理承認 aaa =', AnkenList.objects.filter(aaa))
    print('案件ステータス ya(query) =', ya)
    print('案件ステータス ya =', AnkenList.objects.filter(ya))
    print('y1 =', AnkenList.objects.filter(y1))
    print('y2 =', AnkenList.objects.filter(y2))
    print('y3 =', AnkenList.objects.filter(y3))
    print('y4 =', AnkenList.objects.filter(y4))
    print('y5 =', AnkenList.objects.filter(y5))
    print('y6 =', AnkenList.objects.filter(y6))

    form = forms.formAnkenList()
    kazu = AnkenList.objects.all().count()   
    if request.POST['searchType'] == 'andSearch':
        ##　AND　検索
        if request.POST['orderRule'] == 'orderAsc':
            q = AnkenList.objects.filter(aaa).filter(ya)   \
                                .filter(y1).filter(y2).filter(y3) \
                                .filter(y4).filter(y5).filter(y6).order_by(orderItem)
            print('AND_RESULT =', q) 
        else:
            q = AnkenList.objects.filter(aaa).filter(ya)   \
                                .filter(y1).filter(y2).filter(y3) \
                                .filter(y4).filter(y5).filter(y6).order_by(orderItem).reverse()
            print('AND_RESULT =', q)                                       
    else:
        ##  OR 検索
        if request.POST['orderRule'] == 'orderAsc':
            q = AnkenList.objects.filter(aaa).filter(ya)   \
                                 .filter(Q(y1)|Q(y2)|Q(y3)|Q(y4)|Q(y5)|Q(y6)).order_by(orderItem)
            print('OR_RESULT = ', q)
        else:
            q = AnkenList.objects.filter(aaa).filter(ya)   \
                                 .filter(Q(y1)|Q(y2)|Q(y3)|Q(y4)|Q(y5)|Q(y6)).order_by(orderItem).reverse()
            print('OR_RESULT = ', q)

    request.session['sessionDisplayCode'] = 'dp201'     
    # context = searchContextSet(request, q)           
    # return render(request, 'ankenkanri/searchResult.html', context)
    return render(
        request,'ankenkanri2/edit.html',context={'form':form,'ankenList' : q,'kazu':kazu}

        
    )    

def searchParamResume(request):
    request.session['sessionSearchType'] = request.POST.get('searchType')
#    request.session['sessionDpList'] = request.POST.get('dpList')
    request.session['sessionOrderRule'] = request.POST.get('orderRule')
    r = request.POST.getlist('keiriYN')
    print('r =', r)
    s = ['1', '0']
    t = listExpand(r, s) ## リストtに要素2設定
    request.session['sessionKeiriYN'] = t
    print('(searchParamResume)sessionKeiriYN =', request.session['sessionKeiriYN'])

    # request.session['sessionKeiriYN'] = request.POST.getlist('keiriYN')
    # keiriShoninList = request.POST.getlist('keiriYN')
    # s = ['True', 'False']
    # keiriShoninList = listExpand(keiriShoninList, s)
    # print('keiriShoninList =', keiriShoninList)       ## !!!! dummy !!!!

     ### リストt要素数を11にする。（そのために空白(ヌル)を挿入）
    r = request.POST.getlist('statusL')
    s = ['案件入力中', '案件入力完', '見積書作成依頼済', '見積書入手済', \
         '稟議書承認完了', '契約書作成完了', '契約書締結完了', '注文完了', \
         '納品完了', '請求書入手済', '支払処理完了' ]
    t = listExpand(r, s)  ## リストtに要素11設定
    request.session['sessionStatusL'] = t 
    # print('r =', r)
    # print('t =', t)
    
    request.session['sessionKanriNoE'] = request.POST.get('kanriNoE')
    request.session['sessionAnkenM'] = request.POST.get('ankenM')
    request.session['sessionTorihikisakiM'] = request.POST.get('torihikisakiM')
    request.session['sessionKonyuG'] = request.POST.get('konyuG')
    request.session['sessionTantoshaM'] = request.POST.get('tantoshaM')
    request.session['sessionSaisyuH'] = request.POST.get('saisyuH')

    print('(searchParamResume)searchType =', request.POST.get('searchType'))
    print('(searchParamResume)dpList =', request.session['sessionDpList'])
    print('(searchParamResume)orderRule =', request.POST.get('orderRule'))
    print('(searchParamResume)keiriYN =', request.POST.getlist('keiriYN'))

    print('(searchParamResume)kanriNoE =', request.POST.get('kanriNoE'))
    print('(searchParamResume)ankenM =', request.POST.get('ankenM'))
    print('(searchParamResume)torihikisakiM =', request.POST.get('torihikisakiM'))
    print('(searchParamResume)konyuG =', request.POST.get('konyuG'))
    print('(searchParamResume)tantoshaM =', request.POST.get('tantoshaM'))
    print('(searchParamResume)saisyuH =', request.POST.get('saisyuH'))
    return()

##### 圧縮されて入っているリストrをtに展開する　r:現状リスト、s:フルリスト→t（結果）

def listExpand(r, s):
    t = [] 
    i = 0   
    for row1 in s:
        j = 0
        for row2 in r:
            if row1 == row2:
                t.append(row1)
                break
            if j >= len(r) - 1:
                t.append("")
            j = j + 1
    #        print('j =',j)
        i = i + 1
    #    print('i =', i)
    return(t)