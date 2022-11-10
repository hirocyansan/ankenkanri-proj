# from curses.ascii import isspace
#import views
import sys
from re import S
from django import forms
from tkinter.tix import Tree
from django.shortcuts import redirect, render

#from symbol import pass_stmt
from django.contrib.auth import logout, authenticate, get_user_model
User = get_user_model()
#from django.http import HttpResponse
from .. import forms

#from ..models import User  #追加

#from ..forms import MySetPasswordForm   ##追加

#from ..forms import MySetPasswordForm

from django.urls import reverse

from django.views.generic import TemplateView
from ..models import AnkenList, AnkenStatus
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

from .views2 import get_last_date, edabanCreateCheck
from .views3 import searchContextSet
from .viewsa import dataexport, export2, dataimport, import2
from .viewsa import edit, edit2

def sysExit(request):

    sys.exit()

def terminate(request):
        return render(request, 'ankenkanri/terminate.html')

def top_menu(request):
    print('user_id =', str(request.user))   ### test code ###
    #request.session['sessionUserName'] = request.POST.get('username')
    #request.session['sessionPassword'] = request.POST.get('password')
    print('user_id =', request.POST.get('username'))
    print('password =', request.POST.get('password'))
    return redirect('/ankenkanri2/index')

# def logout_view(request):
#     logout(request)
#     return redirect('/ankenkanri/top_menu')

def number_treat(request):
    recallParam(request)       ## ログイン直後にパラメータを再読み込み
    request.session['sessionDisplayCode'] = 'dp02' 
    return render(request, 'ankenkanri/number_treat.html')

## 経理未承認のワーニングメッセージ画面中にキーが押された
def page_n0(request):
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    print("q =", q)
    ctx["object"] = q
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'] )
    if (q[0].keiriShonin) == 1:
        request.session['sessionDisplayCode'] = 'dp11'             
        return render(request, 'ankenkanri/page_n.html', context)
    elif  "pageN" in request.POST:
        request.session['sessionDisplayCode'] = 'dp11'    
        return render(request, 'ankenkanri/page_n.html', context)
    elif "pageTop" in request.POST: 
        return redirect('/ankenkanri2/index')
    else:
        request.session['sessionDisplayCode'] = 'dp01'    
        return render(request, 'ankenkanri/page_n0.html', context)     

## sessionに記憶しておいたユーザ設定値がない場合には、強制的にsessionデータを初期化する。
def recallParam(request):
    if (not 'sessionSearchType' in request.session) or (request.session['sessionSearchType'] == []):
        request.session['sessionSearchType'] = 'andSearch'
    if (not 'sessionDpList' in request.session) or (request.session['sessionDpList'] == []):
        request.session['sessionDpList'] = 'keiriShonin'
    if (not 'sessionSorting' in request.session) or (request.session['sessionSorting'] == []):
        request.session['sessionSorting'] = 'sortAccounting'
    if (not 'sessionOrderRule' in request.session) or (request.session['sessionOrderRule'] == []):
        request.session['sessionOrderRule'] = 'orderAsc'
    if (not 'sessionKeiriYN' in request.session) or (request.session['sessionKeiriYN'] == []): 
        request.session['sessionKeiriYN'] = ['1','0']
    print('(recallParam)sessionKeiriYN =', request.session['sessionKeiriYN'])
    if (not 'sessionStatusL' in request.session) or (request.session['sessionStatusL'] == []):
        request.session['sessionStatusL'] = ['案件入力中','','','','','','','','','','']

    # request.session['sessionStatusL'] = ['案件入力中', '案件入力完', '見積書作成依頼済', '見積書入手済', \
    #                                      '稟議書承認完了', '契約書作成完了', '契約書締結完了', '注文完了', \
    #                                      '納品完了', '請求書入手済', '支払処理完了' ]
    if (not 'sessionKanriNoE' in request.session) or (request.session['sessionKanriNoE'] == []):
        request.session['sessionKanriNoE'] = ''
    if (not 'sessionAnkenM' in request.session) or (request.session['sessionAnkenM'] == []):
        request.session['sessionAnkenM'] = ''
    if (not 'sessionTorihikisakiM' in request.session) or (request.session['sessionTorihikisakiM'] == []):
        request.session['sessionTorihikisakiM'] = ''
        print('L60 =', request.session['sessionTorihikisakiM'] )
    if (not 'sessionKonyuG' in request.session) or (request.session['sessionKonyuG'] == []):
        request.session['sessionKonyuG'] = ''
    if (not 'sessionTantoshaM' in request.session) or (request.session['sessionTantoshaM'] == []):
        request.session['sessionTantoshaM'] = ''
    if (not 'sessionSaisyuH' in request.session) or (request.session['sessionSaisyuH'] == []):
        request.session['sessionSaisyuH'] = ''
    return()

def time_test():
    # today
    today = date.today()
    print(today) # => 2016-04-19

    # 1ヶ月後
    #dt = today + relativedelta(months=1)
    dt = datetime(2022, 11, 30, 00, 00, 00, tzinfo=UTC)
    dt = get_last_date(dt + relativedelta(months=1))
    print(dt) 

    # 1年後
    dt = today + relativedelta(years=1)
    dt = datetime(2022, 11, 30, 00, 00, 00, tzinfo=UTC)
    dt = get_last_date(dt + relativedelta(years=1))    
    print(dt) # => 2017-04-19

    # 月末
    dt = today + relativedelta(months=1) - timedelta(days=today.day)
    print(dt) # => 2016-04-30

    print('timedelta(days=today.day) =', timedelta(days=today.day))

    # 月初（これはtimedeltaで普通にできるけど、一応書いてみる）
    dt = today - timedelta(days=today.day-1)
    print(dt) # => 2016-04-01

def initialStart(request):    
    request.session['sessionDisplayCode'] = 'dp02'    ## tempolary setting !!!
#    recallParam(request)        ## パラメータの読み出し（入っていなければ初期化）
    print('sessionDisplayCode =', request.session['sessionDisplayCode'])
    print('L37 in intialStart!!!!!!')
#    time_test()       #### for debug

    edabanCreateCheck(request) 
    request.session['sessionDisplayCode'] = 'dp001'    ## login画面表示 !!!
    return redirect('/accounts/login')

def setFilterCEdaban(request):
    print('sessionKanriNo =', request.session['sessionKanriNo'])
    edabanTemp = request.session['sessionEdaban']
    if (edabanTemp is None) or (edabanTemp == ""):
        q =  AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban__isnull=True)
    else: 
        q =  AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp)
    return(q)  

def setStatusCodeCEdaban(request, statusCodeTemp):
    ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=int(statusCodeTemp))
    edabanTemp = request.session['sessionEdaban']
    if (edabanTemp is None) or (edabanTemp == ""):
        AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
	    statusCode = statusCodeTemp,
        status = ankenTemp[0].ankenStatus)
    else:
        AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
	    statusCode = statusCodeTemp,
        status = ankenTemp[0].ankenStatus)
    return



## 入力された管理番号がDBに登録されているかチェック
def checkKanriNo(request):
    ankenList = AnkenList.objects.all()
    OK = True
    NG = False
    for row in ankenList:
        if request.session['sessionKanriNo'] == row.kanriNo and  \
                    request.session['sessionEdaban'] == row.edaban :
                    return(OK)
    return(NG)

DEBUG_MODE = 'ON'
def statusCodeCheck(request, selectedStatus):
    if DEBUG_MODE == 'ON':
        return 'OK'
    ankenTemp = AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=request.session['sessionEdaban'])
    if ankenTemp[0].statusCode < selectedStatus:
        return 'OK'
    else:
        return 'NG'


## TOPメニュー表示中にボタンが押されたとき
def service_start(request):
    if "searchButton" in request.POST:
        q = AnkenList.objects.all()
        recallParam(request)  ## 検索パラメータが未設定の場合、初期化する
        context = searchContextSet(request, q)    # 検索条件読み出し、設定
        #searchParamResume(request)
        request.session['sessionDisplayCode'] = 'dp200' 
        return render(request, 'ankenkanri/search.html', context) 
    elif "kanriNoButton" in request.POST:
        request.session['sessionDisplayCode'] = 'dp02' 
        return render(request, 'ankenkanri/number_treat.html')
    elif "dataEditButton" in request.POST:
        form = forms.formAnkenList()
        kazu = AnkenList.objects.all().count()  
        request.session['sessionDisplayCode'] = 'dp230'   
        return render(
            request,'ankenkanri2/edit.html',context={'form':form,'ankenList' \
                                                : AnkenList.objects.order_by('hyojijun'),'kazu':kazu}
        )
    elif "dataExportButton" in request.POST:
        request.session['sessionDisplayCode'] = 'dp210' 
        return render(request, 'ankenkanri2/export.html')
    elif "dataImportButton" in request.POST:
        request.session['sessionDisplayCode'] = 'dp220' 
        return render(request, 'ankenkanri2/import.html')
    elif "variousSettingsButton" in request.POST:
        request.session['sessionDisplayCode'] = 'dp240' 
        return render(request, 'ankenkanri/variousSettings.html')
    elif "usageButton" in request.POST:
        return redirect('/ankenkanri2/index')

    else:  ## "terminateButton" in request.POST:
        logout(request)
        return redirect('/accounts/login/')
        #return redirect('/ankenkanri/terminate')

## 各種設定画面表示中にボタンが押された
def variousSettings(request):
    if "changeSettings" in request.POST:
        request.session['sessionDisplayCode'] = 'dp240' 
        return redirect('/ankenkanri2/index')   ###  暫定的にTOP画面に戻す
    elif "changePassword" in request.POST:
        request.session['sessionDisplayCode'] = 'dp250' 
        return redirect('/accounts/password_change')
        #return render(request, 'ankenkanri/changePassword.html')   
    else:  ## "pageTop" in request.POST:
        return redirect('/ankenkanri2/index')   

# # パスワード変更フォームを表示する処理
# def changePassword(request):
#     template_name = 'changePassword.html'
#     form = MySetPasswordForm(user=request.user)
#     context = {
#         'form': form,
#     }
#     return render(request, template_name, context)


# # パスワードの変更を保存する処理
# def changePasswordPost(request):
#     if request.method == 'POST':
#         form = MySetPasswordForm(request.POST)
#         if form.is_valid():
#             form.save()
#     request.session['sessionDisplayCode'] = 'dp00' 
#     return redirect('/ankenkanri2/index')
#     #return render(request, '/ankenkanri2/index.html', context)


## 管理番号入力処理画面でボタンが押された
def page_n(request):
    print('user_id =', str(request.user))   ### test code ###
    #print('request.session[sessionDisplayCode] =', request.session['sessionDisplayCode'] )
    if 'sessionDisplayCode' in request.session:
        pass
    else:
        request.session['sessionDisplayCode'] = 'dp000'    #### for dummy ###
    #model = AnkenList
    print("(page_n)Current point is L164 !!")

    ## 管理番号入力画面表示中チェック
    if request.session['sessionDisplayCode'] == 'dp02' and request.method == "POST":

        if "pageTop" in request.POST:    ## 「TOPメニュー」検出
                request.session['sessionDisplayCode'] = 'dp00' 
                return redirect('/ankenkanri2/index')

        # inData = request.POST.get('inputNo')
        # request.session['sessionKanriNo'] = inData
        # request.session['sessionEdaban'] = request.POST.get('edaban')

        # if "pageSearch" in request.POST:  ## 暫定ボタン「検索へ飛ぶ」検出
        #         q = AnkenList.objects.all()
        #         context = searchContextSet(request, q)    # 検索条件読み出し、設定
        #         print('L338 =', request.session['sessionTorihikisakiM'] )                
        #         print('c1 =', context['c1'])
        #         print('c2 =', context['c2'])
        #         print('c3 =', context['c3'])
        #         print('c4 =', context['c4'])
        #         print('c5 =', context['c5'])
        #         print('c6 =', context['c6'])
        #         print('c7 =', context['c7'])
        #         print('c8 =', context['c8'])
        #         print('c9 =', context['c9'])
        #         print('c10 =', context['c10'])
        #         print('c11 =', context['c11'])
        #         print('c12 =', context['c12'])
        #         print('c13 =', context['c13'])
        #         print('c14 =', context['c14'])
        #         print('c15 =', context['c15'])
        #         print('c16 =', context['c16'])
        #         print('c17 =', context['c17'])
        #         print('c18 =', context['c18'])
        #         print('c19 =', context['c19'])
        #         print('c20 =', context['c20'])
        #         print('c21 =', context['c21'])
        #         print('c22 =', context['c22'])
        #         print('c23 =', context['c23'])
        #         print('c24 =', context['c24'])

        #         #searchParamResume(request)
        #         print('L847 =', request.session['sessionTorihikisakiM'] )
        #         request.session['sessionDisplayCode'] = 'dp200' 
        #         return render(request, 'ankenkanri/search.html', context) 

        request.session['sessionKanriNo'] = request.POST.get('kanriNo')   ## dummy ##
        request.session['sessionEdaban'] = request.POST.get('edaban')    ## dummy ##
        form = forms.kanriNoForm(request.POST)

        is_valid = form.is_valid()
        print(is_valid)
        if form.is_valid() == False:
            print(form.errors)
        # if form.is_valid() == False:
        #     for ele in form :
        #         print(ele)


        if form.is_valid():
            request.session['sessionKanriNo'] = form.cleaned_data.get('kanriNo')
            if form.cleaned_data.get('edaban') == '':
                request.session['sessionEdaban'] = None
            else:
                request.session['sessionEdaban'] = form.cleaned_data.get('edaban')
                if form.cleaned_data.get('edaban') == '0':
                    message = '枝番0(親枝番)は対象外です。他の番号を入力願います。'
                    context = { 'message' : message }
                    request.session['sessionDisplayCode'] = 'dp02'             
                    return render(request, 'ankenkanri/number_treat.html', context)                     
        else:
            #print(form.errors)
            message = '入力にエラーが検出されました！再入力願います。'
            context = { 'message' : message }
            request.session['sessionDisplayCode'] = 'dp02'             
            return render(request, 'ankenkanri/number_treat.html', context)  

        ##　入力された管理番号チェック
        inData = request.session['sessionKanriNo']           
        if len(inData) == 0 or inData == "" or inData == " ":          ### 空文字検出　いまいち！
            print("NULL Detected !!!")
        elif checkKanriNo(request) == False:   ## 管理番号がDBに入っているものかチェック
            request.session['sessionDisplayCode'] = 'dp02'  
            message = '登録済み管理番号を入力願います。'
            context = { 'message' : message }
            return render(request, 'ankenkanri/number_treat.html', context)   

        else:  ## 管理番号入力検出
            print("L53 Here! indata !=0 ")
            inData = request.session['sessionKanriNo']
            edaban = request.session['sessionEdaban']
            q = setFilterCEdaban(request)
            print('(page_n)q =', q)
            context = contextSet(inData, edaban)
            print(" arrived at L864 !!You are right!!!")

            if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
                request.session['sessionDisplayCode'] = 'dp11'     
                return render(request, 'ankenkanri/page_n.html', context)
            else:
                request.session['sessionDisplayCode'] = 'dp01'     
                return render(request, 'ankenkanri/page_n0.html', context) 

    if request.session['sessionDisplayCode'] == 'dp02':
        request.session['sessionDisplayCode'] = 'dp02'  
        message = ''
        context = { 'message' : message } 
        return render(request, 'ankenkanri/number_treat.html')
    
    ## 案件入力完了の確認画面表示チェック

    elif request.session['sessionDisplayCode'] ==  'dp10':  ## 案件入力完了画面表示中にキー入力
        if  "pageN" in request.POST:
            ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=1)
            edabanTemp = request.session['sessionEdaban']
            if (edabanTemp is None) or (edabanTemp == ""):  ## statusCode,statusをDBへ記録
                AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
                    statusCode = 1,
                    status = ankenTemp[0].ankenStatus,
                    saishuKoshinsha = str(request.user),
                    dataKoshinbi = timezone.now()
                )
            else:            
                AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
                    statusCode = 1,
                    status = ankenTemp[0].ankenStatus,
                    saishuKoshinsha = str(request.user),
                    dataKoshinbi = timezone.now()
                )
                request.session['sessionDisplayCode'] = 'dp11' 
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
        elif "pageTop" in request.POST:
                request.session['sessionDisplayCode'] = 'dp00' 
                return redirect('/ankenkanri2/index')
        else:
            return render(request, 'ankenkanri/ankenNyuuryokuKan1.html')

    ## 見積書依頼確認画面表示チェック

    elif request.session['sessionDisplayCode'] ==  'dp20':  ## 見積書依頼確認画面表示中にキー入力
        ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=2)
        edabanTemp = request.session['sessionEdaban']
        if  "pageN" in request.POST:
            if (edabanTemp is None) or (edabanTemp == ""):  ## statusCode,statusをDBへ記録
                AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
                    statusCode = 2,
                    status = ankenTemp[0].ankenStatus,
                    saishuKoshinsha = str(request.user),
                    dataKoshinbi = timezone.now()
                )
            else:            
                AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
                    statusCode = 2,
                    status = ankenTemp[0].ankenStatus,
                    saishuKoshinsha = str(request.user),
                    dataKoshinbi = timezone.now()
                )
                request.session['sessionDisplayCode'] = 'dp11' 
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
        elif "pageTop" in request.POST:
                request.session['sessionDisplayCode'] = 'dp00' 
                return redirect('/ankenkanri2/index')
        else:
            return render(request, 'ankenkanri/mitsumorisyoIraiKan2.html')
    
    ## 見積書入手確認画面表示チェック　（多分、このコードは使われていない）

    # elif request.session['sessionDisplayCode'] ==  'dp30':
    #     if  "pageN" in request.POST:
    #             request.session['sessionDisplayCode'] = 'dp11' 
    #             context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    #             return render(request, 'ankenkanri/page_n.html', context)
    #     elif "pageTop" in request.POST:
    #             request.session['sessionDisplayCode'] = 'dp00' 
    #             return redirect('/ankenkanri2/index')
    #     else:
    #         return render(request, 'ankenkanri/mitumorisyoNyuusyuKan3.html')
    
    ## 検索画面表示チェック
    
    elif request.session['sessionDisplayCode'] ==  'dp200':  ## 検索画面表示中
        print('L919 dpList =', request.POST.get('dpList') )
    else:
        print( "arrived L921 !!")
        if "pageTop" in request.POST:
                request.session['sessionDisplayCode'] = 'dp00' 
                return redirect('/ankenkanri2/index')

        ## 案件入力完了画面
        if  "ankenNyuuryokuKan1"  in request.POST:  # (クリックしたボタンに応じたHTMLへ分岐させる)
            if statusCodeCheck(request, 1) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 1)  ## statusCode = 1
            print("Detected the button1")
            request.session['sessionDisplayCode'] = 'dp10'   
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/ankenNyuuryokuKan1.html', context)

        ## 見積書作成依頼の終了ボタンが押された（page_n表示中）
        elif "mitsumorisyoIraiKan2" in request.POST:
            if statusCodeCheck(request, 2) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 2)  ## statusCode = 2
            print("Detected the button2")
            request.session['sessionDisplayCode'] = 'dp20'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/mitsumorisyoIraiKan2.html', context)

        ## 見積書の入手ボタンが押された（page_n表示中）
        elif "mitumorisyoNyuusyuKan3" in request.POST:
            if statusCodeCheck(request, 3) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 3)  ## statusCode = 3
            print("Detected the button3")
            request.session['sessionDisplayCode'] = 'dp30'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            print(" L145 is here !!")
            return render(request, 'ankenkanri/mitumorisyoNyuusyuKan3.html', context)

        ## スキップボタンが押された（稟議決裁完了画面表示中）        
        elif "skipPage3to4" in request.POST:
            setStatusCodeCEdaban(request, 4)  ## statusCode = 4
            print("Detected the skip-button(in dp40)")
            request.session['sessionDisplayCode'] = 'dp40'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/page_n.html', context)

        ## 稟議決裁終了ボタンが押された（page_n表示中）
        elif "ringiShoninKan4" in request.POST:
            if statusCodeCheck(request, 4) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 4)  ## statusCode = 4
            print("Detected the button4")
            request.session['sessionDisplayCode'] = 'dp40'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/ringiShoninKan4.html', context)

        ## スキップボタンが押された（契約書作成終了画面表示中）
        elif "skipPage4to5" in request.POST:
            setStatusCodeCEdaban(request, 5)  ## statusCode = 5
            print("Detected the skip-button(in dp50)")
            request.session['sessionDisplayCode'] = 'dp50'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/page_n.html', context)

        ## 契約書の作成終了ボタンが押された（page_n表示中）
        elif "keiyakusyoSakuseiKan5" in request.POST:
            if statusCodeCheck(request, 5) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 5)  ## statusCode = 5
            print("DisplayCode =", request.session['sessionDisplayCode'] )
            print("Detected the button5")
            request.session['sessionDisplayCode'] = 'dp50'
            print("DisplayCode =", request.session['sessionDisplayCode'] )
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/keiyakusyoSakuseiKan5.html', context)

        ## スキップボタンが押された（契約書締結終了画面表示中）
        elif "skipPage5to6" in request.POST:
            setStatusCodeCEdaban(request, 6)  ## statusCode = 6
            print("Detected the skip-button(in dp60)")
            request.session['sessionDisplayCode'] = 'dp60'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/page_n.html', context)

        ## 契約書締結終了ボタンが押された（page_n表示中）
        elif "keiyakusyoTeiketsuKan6" in request.POST:
            if statusCodeCheck(request, 6) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 6)  ## statusCode = 6
            print("Detected the button6")
            request.session['sessionDisplayCode'] = 'dp60'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/keiyakusyoTeiketsuKan6.html', context)

        ## スキップボタンが押された（注文処理終了画面表示中）
        elif "skipPage6to7" in request.POST:
            setStatusCodeCEdaban(request, 7)  ## statusCode = 7
            print("Detected the skip-button(in dp70)")
            request.session['sessionDisplayCode'] = 'dp70'
            context = contextSet( request.session['sessionKanriNo'],request.session['sessionEdaban'])
            return render(request, 'ankenkanri/page_n.html', context)

        ## 契約書締結終了ボタンが押された（page_n表示中）
        elif "cyuumonKan7" in request.POST:
            if statusCodeCheck(request, 7) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 7)  ## statusCode = 7
            print("Detected the button7")
            request.session['sessionDisplayCode'] = 'dp70'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/cyuumonKan7.html', context)

        ## スキップボタンが押された（納品処理終了画面表示中）
        elif "skipPage7to8" in request.POST:
            setStatusCodeCEdaban(request, 8)  ## statusCode = 8
            print("Detected the skip-button(in dp80)")
            request.session['sessionDisplayCode'] = 'dp70'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/page_n.html', context)

        ## 納品処理終了ボタンが押された（page_n表示中）
        elif "nouhinKan8" in request.POST:
            if statusCodeCheck(request, 8) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 8)  ## statusCode = 8
            print("Detected the button8")
            request.session['sessionDisplayCode'] = 'dp80'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/nouhinKan8.html', context)

        ## スキップボタンが押された（請求書処理終了画面表示中）
        elif "skipPage8to9" in request.POST:
            setStatusCodeCEdaban(request, 9)  ## statusCode = 9
            print("Detected the skip-button(in dp90)")
            request.session['sessionDisplayCode'] = 'dp70'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/page_n.html', context)

        ## 請求書処理終了ボタンが押された（page_n表示中）
        elif "seikyuusyoNyuusyu9" in request.POST:
            if statusCodeCheck(request, 9) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 9)  ## statusCode = 9
            print("Detected the button9")
            request.session['sessionDisplayCode'] = 'dp90'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/seikyuusyoNyuusyu9.html', context)

        ## スキップボタンが押された（支払処理終了画面表示中）
        elif "skipPage9to10" in request.POST:
            setStatusCodeCEdaban(request, 10)  ## statusCode = 10
            print("Detected the skip-button(in dp100)")
            request.session['sessionDisplayCode'] = 'dp100'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/page_n.html', context)

        ## 支払処理終了ボタンが押された（page_n表示中）
        elif "shiharaiKan10" in request.POST:
            if statusCodeCheck(request, 10) == "NG":  ## 既に終了した処理のキーが押されたら、入力無視
                request.session['sessionDisplayCode'] = 'dp11'
                context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
                return render(request, 'ankenkanri/page_n.html', context)
            setStatusCodeCEdaban(request, 10)  ## statusCode = 10
            print("Detected the button10")
            request.session['sessionDisplayCode'] = 'dp100'
            context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
            return render(request, 'ankenkanri/shiharaiKan10.html', context)
        else:
            request.session['sessionDisplayCode'] = 'dp02'
            message = ''
            context = { 'message' : message }   
            return render(request, 'ankenkanri/number_treat.html')

def badgeButtonSet():
    badgeName = ["案件入力済\n(STATUS = 1)", \
                "見積書依頼処理\n(STATUS = 2)", \
                "見積書入手処理\n(STATUS = 3)", \
                "稟議承認処理\n(STATUS = 4)", \
                "契約書_作成完了\n(STATUS = 5)",\
                "契約書_締結完了\n(STATUS = 6)", \
                "注文処理\n(STATUS = 7)", \
                "納品処理\n(STATUS = 8)", \
                "請求書処理\n(STATUS = 9)", \
                "支払処理済\n(STATUS = 10)"
                ]
    buttonName0 = {"ankenNyuuryokuKan1"     : "案件入力を終了しました", \
                   "mitsumorisyoIraiKan2"   : "見積書の作成依頼を終了しました", \
                   "mitumorisyoNyuusyuKan3" : "見積書を入手しました", \
                   "ringiShoninKan4"        : "稟議決裁を終了しました", \
                   "keiyakusyoSakuseiKan5"  : "契約書の作成が終了しました", \
                   "keiyakusyoTeiketsuKan6" : "契約書の締結が終了しました", \
                   "cyuumonKan7"            : "注文処理が終了しました", \
                   "nouhinKan8"             : "納品処理が終了しました", \
                   "seikyuusyoNyuusyu9"     : "請求書処理が終了しました", \
                   "shiharaiKan10"          : "支払処理が終了しました"
                   }

    buttonName = ["案件入力を終了しました", "見積書の作成依頼を終了しました", \
                "見積書を入手しました", "稟議決裁を終了しました", \
                "契約書の作成が終了しました", "契約書の締結が終了しました", \
                "注文処理が終了しました", "納品処理が終了しました", \
                "請求書処理が終了しました", "支払処理が終了しました"
                ]
    buttonName2 = ["ankenNyuuryokuKan1", "mitsumorisyoIraiKan2", \
                "mitumorisyoNyuusyuKan3", "ringiShoninKan4", \
                "keiyakusyoSakuseiKan5", "keiyakusyoTeiketsuKan6", \
                "cyuumonKan7", "nouhinKan8", \
                "seikyuusyoNyuusyu9", "shiharaiKan10" 
                ]
    return badgeName, buttonName0, buttonName, buttonName2 


def contextSet( inData, edaBan ):  #　 inData： 案件管理No.
    model = AnkenList
    ctx = {}
    if (edaBan is None) or (edaBan==""):
        q = AnkenList.objects.filter(kanriNo=inData).filter(edaban__isnull=True)
    else:
        q = AnkenList.objects.filter(kanriNo=inData).filter(edaban=edaBan)

    ctx["object"] = q
    badgeName, buttonName0, buttonName, buttonName2 = badgeButtonSet()
    print('(contextSet)q[0] =', q[0])
    badgeGray = q[0].statusCode
    buttonGray = q[0].statusCode
    context = {
        'badgeName': badgeName,
        'buttonName0': buttonName0,
        'buttonName': buttonName,
        'buttonName2': buttonName2,
        'badgeGray': badgeGray,
        'buttonGray': buttonGray,
        'q': q,
    }
    return(context)

def contextSetWMessage( inData, edaBan, message):  #　 inData： 案件管理No.
    model = AnkenList
    ctx = {}
    if (edaBan is None) or (edaBan==""):
        q = AnkenList.objects.filter(kanriNo=inData).filter(edaban__isnull=True)
    else:
        q = AnkenList.objects.filter(kanriNo=inData).filter(edaban=edaBan)

    ctx["object"] = q
    badgeName, buttonName0, buttonName, buttonName2 = badgeButtonSet()
    print('(contextSet)q[0] =', q[0])
    badgeGray = q[0].statusCode
    buttonGray = q[0].statusCode
    context = {
        'badgeName': badgeName,
        'buttonName0': buttonName0,
        'buttonName': buttonName,
        'buttonName2': buttonName2,
        'badgeGray': badgeGray,
        'buttonGray': buttonGray,
        'q': q,
        'message': message,
    }
    return(context)

def ankennyuuryokucyuu0(request):  # 案件入力中の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-page0-1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 0)  ## statusCode = 0
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def ankenNyuuryokuKan1(request):   # 案件入力が完了したときの処理
    print("Arrived L630(ankenNyuuryokuKan1)")
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 1)  ## statusCode = 1
        print("Keiri shonin detected!!!")
        return render(request, 'ankenkanri/page_n.html', ctx)
    print("Keiri mi-shonin detected!!!")
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def mitsumorisyoIraiKan2(request):  # 見積書依頼が完了した時の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 2)  ## statusCode = 2
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def mitumorisyoNyuusyuKan3(request):  # 見積書入手が完了した時の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 3)  ## statusCode = 3
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def ringiShoninKan4(request):  # 稟議承認処理が完了した時の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 4)  ## statusCode = 4
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def keiyakusyoSakuseiKan5(request):  # 契約書の作成が終了した時の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 5)  ## statusCode = 5
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def keiyakusyoTeiketsuKan6(request):  # 契約書の締結が完了した時の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 6)  ## statusCode = 6
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def cyuumonKan7(request):  # 注文処理が完了した時の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 7)  ## statusCode = 7
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def nouhinKan8(request):  # 納品が完了した時の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 8)  ## statusCode = 8
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def seikyuusyoNyuusyu9(request):  #  請求書の入手が完了した時の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 9)  ## statusCode = 9
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx) 

def shiharaiKan10(request):  # 支払処理が完了した時の処理
    model = AnkenList
    ctx = {}
    q = setFilterCEdaban(request)
    ctx["object"] = q
    print("passed the views.py-def-ankenNyuuryokuKan1 ")
    print("statusCode =", q[0].statusCode)
    if (q[0].keiriShonin) == 1:             # !!!!! dummy code !!!!!!!
        setStatusCodeCEdaban(request, 10)  ## statusCode = 10
        return render(request, 'ankenkanri/page_n.html', ctx)
    return render(request, 'ankenkanri/page_n0.html', ctx)   






