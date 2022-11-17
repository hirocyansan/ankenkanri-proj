# from curses.ascii import isspace
#import views
from re import S
from django import forms
from tkinter.tix import Tree
from django.shortcuts import redirect, render
#from django.http import HttpResponse
from .. import forms
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


from .views1 import setStatusCodeCEdaban, contextSet, contextSetWMessage

## 金額が入力されているかチェック 

def dataCheck(tanka, kosu):

    if len(str(tanka)) == 0 or (not str(tanka)) :
        return 'NG'
    else:
        value = tanka*kosu
        return value

## 見積書入手済画面でボタンが押された
def mitsumoriSave(request):   # 入力した見積情報をＤＢに書き込んでpage_n.htmlへ遷移する
    print("Arrived L349 !!!")
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    if "pageTop" in request.POST:
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif  "confirm" in request.POST:
        if (request.POST.get('mitsumoriTanka') is None) or (request.POST.get('mitsumoriTanka') == "") :          ### 空文字検出　いまいち！
            print('Detect 空文字！')
            request.session['sessionDisplayCode'] = 'dp30' 
            message = '入力が空です。再入力願います。'
            context = contextSetWMessage( request.session['sessionKanriNo'], request.session['sessionEdaban'], message)
            return render(request, 'ankenkanri/mitumorisyoNyuusyuKan3.html', context)
        form = forms.mitsumorisyoForm(request.POST)
        if form.is_valid():
            pass
        else:
            request.session['sessionDisplayCode'] = 'dp30' 
            message = '入力にエラーが検出されました！再入力願います。'
            context = contextSetWMessage( request.session['sessionKanriNo'], request.session['sessionEdaban'], message)
            return render(request, 'ankenkanri/mitumorisyoNyuusyuKan3.html', context)
        
        ## 見積単価、見積数、URL、status,statusCodeをDBに記録
        ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=3)
        edabanTemp = request.session['sessionEdaban']
        result = dataCheck(form.cleaned_data.get('mitsumoriTanka'), form.cleaned_data.get('mitsumoriSuu'))
        if result != 'NG':
            gokeiTemp = result 
        else:
            gokeiTemp = 0
        if (edabanTemp is None) or (edabanTemp == ""): 
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
                statusCode = 3,
                mitsumoriTanka = form.cleaned_data.get('mitsumoriTanka'),
                mitsumoriSuu = form.cleaned_data.get('mitsumoriSuu'),
                mitsumoriGokei = gokeiTemp,
                mitsumoriLink = form.cleaned_data.get('mitsumoriLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )
        else:            
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
                statusCode = 3,
                mitsumoriTanka = form.cleaned_data.get('mitsumoriTanka'),
                mitsumoriSuu = form.cleaned_data.get('mitsumoriSuu'),
                mitsumoriGokei = gokeiTemp,
                mitsumoriLink = form.cleaned_data.get('mitsumoriLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )
        print("見積金額、リンク情報をDBへ格納しました。Detected the 確定ボタン")
        request.session['sessionDisplayCode'] = 'dp11'  
        return render(request, 'ankenkanri/page_n.html', context)
    else:
        request.session['sessionDisplayCode'] = 'dp30'
        return render(request, 'ankenkanri/mitumorisyoNyuusyuKan3.html')

## 稟議承認完了画面でボタンが押された
def ringiShoninSave(request):   
    print("Arrived L300 !!!")
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    if "pageTop" in request.POST:
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif "skipPage3to4" in request.POST:
        setStatusCodeCEdaban(request, 4)
        print("Detected the skip-button(in dp40)")
        request.session['sessionDisplayCode'] = 'dp40'
        context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
        return render(request, 'ankenkanri/page_n.html', context)
    elif  "confirm" in request.POST:
        if (request.POST.get('ringiTanka') is None) or (request.POST.get('ringiTanka') == "") :          ### 空文字検出　いまいち！
            print('Detect 空文字！')
            request.session['sessionDisplayCode'] = 'dp40' 
            return render(request, 'ankenkanri/ringiShoninKan4.html', context)

        form = forms.ringiShoninForm(request.POST)
        if form.is_valid():
            pass
        else:
            request.session['sessionDisplayCode'] = 'dp40' 
            message = '入力にエラーが検出されました！再入力願います。'
            context = contextSetWMessage( request.session['sessionKanriNo'], request.session['sessionEdaban'],message)
            return render(request, 'ankenkanri/ringiShoninKan4.html', context)

        ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=4)
        edabanTemp = request.session['sessionEdaban']
        if dataCheck(int(form.cleaned_data.get('ringiTanka')), int(form.cleaned_data.get('ringiSuu'))) != 'NG':
            gokeiTemp = dataCheck(int(form.cleaned_data.get('ringiTanka')), int(form.cleaned_data.get('ringiSuu'))) 
        else:
            gokeiTemp = 0
        if (edabanTemp is None) or (edabanTemp == ""):
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
                statusCode = 4,
                ringiTanka = form.cleaned_data.get('ringiTanka'),
                ringiSuu = form.cleaned_data.get('ringiSuu'),
                ringiGokei = gokeiTemp,
                ringishoLink = form.cleaned_data.get('ringishoLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )
        else:        
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
                statusCode = 4,
                ringiTanka = form.cleaned_data.get('ringiTanka'),
                ringiSuu = form.cleaned_data.get('ringiSuu'),
                ringiGokei = gokeiTemp,
                ringishoLink = form.cleaned_data.get('ringishoLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )
        print("稟議書番号をDBへ格納しました。Detected the 確定ボタン。Detected the 確定ボタン")
        request.session['sessionDisplayCode'] = 'dp11'  
        return render(request, 'ankenkanri/page_n.html', context)
    else:
        request.session['sessionDisplayCode'] = 'dp40'
        return render(request, 'ankenkanri/ringiShoninKan4.html')

## 契約書作成完了画面でボタンが押された
def keiyakusyoSakuseiSave(request): 
    print("Arrived L336 !!!")
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    if "pageTop" in request.POST:
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif "skipPage4to5" in request.POST:
        setStatusCodeCEdaban(request, 5)
        print("Detected the skip-button(in dp50)")
        request.session['sessionDisplayCode'] = 'dp50'
        context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
        return render(request, 'ankenkanri/page_n.html', context)
    elif  "confirm" in request.POST:
        if  (request.POST.get('wfNo') is None) or (request.POST.get('wfNo') == "") \
            or (request.POST.get('keiyakushoNo') is None) or (request.POST.get('keiyakushoNo') == "") \
            or (request.POST.get('keiyakuKingaku') is None) or (request.POST.get('keiyakuKingaku') == "") \
            or (request.POST.get('keiyakushoLink') is None) or (request.POST.get('keiyakushoLink') == ""):           
            print('Detect 空文字！')
            request.session['sessionDisplayCode'] = 'dp50'
            message = '入力に空文字が検出されました。再入力願います。' 
            context = contextSetWMessage( request.session['sessionKanriNo'], request.session['sessionEdaban'], message)
            return render(request, 'ankenkanri/keiyakusyoSakuseiKan5.html', context)

        form = forms.keiyakusyoSakuseiForm(request.POST)
        if form.is_valid():
            pass
        else:
            request.session['sessionDisplayCode'] = 'dp50' 
            message = '入力にエラーが検出されました！再入力願います。'
            context = contextSetWMessage( request.session['sessionKanriNo'], request.session['sessionEdaban'], message)
            return render(request, 'ankenkanri/keiyakusyoSakuseiKan5.html', context)

        ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=5)
        edabanTemp = request.session['sessionEdaban']
        if (edabanTemp is None) or (edabanTemp == ""):
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
                statusCode = 5,
                wfNo = form.cleaned_data.get('wfNo'),
                keiyakushoNo = form.cleaned_data.get('keiyakushoNo'),
                keiyakuKingaku = form.cleaned_data.get('keiyakuKingaku'),
                keiyakushoLink = form.cleaned_data.get('keiyakushoLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )
        else:
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
                statusCode = 5,
                wfNo = form.cleaned_data.get('wfNo'),
                keiyakushoNo = form.cleaned_data.get('keiyakushoNo'),
                keiyakuKingaku = form.cleaned_data.get('keiyakuKingaku'),
                keiyakushoLink = form.cleaned_data.get('keiyakushoLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )
        print("wfno、契約書番号、金額、urlをDBへ格納しました。Detected the 確定ボタン")
        request.session['sessionDisplayCode'] = 'dp11' 
        print("DisplayCode =", request.session['sessionDisplayCode']) 
        return render(request, 'ankenkanri/page_n.html', context)
    else:
        request.session['sessionDisplayCode'] = 'dp50'
        return render(request, 'ankenkanri/keiyakusyoSakuseiKan5.html')

## 契約書締結完了画面でボタンが押された
def keiyakusyoTeiketsuSave(request):
    print("Arrived L366 !!!")
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    if "pageTop" in request.POST:
        print("Detected the pageTop-button(in dp60)")
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif "skipPage5to6" in request.POST:
        setStatusCodeCEdaban(request, 6) 
        print("Detected the skip-button(in dp60)")
        request.session['sessionDisplayCode'] = 'dp60'
        context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
        return render(request, 'ankenkanri/page_n.html', context)
    elif  "confirm" in request.POST:
        if (request.POST.get('onatsuRingiNo') is None) or (request.POST.get('onatsuRingiNo') == "") :          ### 空文字検出　いまいち！
            print('Detect 空文字！')
            request.session['sessionDisplayCode'] = 'dp60' 
            return render(request, 'ankenkanri/keiyakusyoTeiketsuKan6.html', context)

        form = forms.keiyakusyoTeiketsuForm(request.POST)
        if form.is_valid():
            pass
        else:
            request.session['sessionDisplayCode'] = 'dp60' 
            message = '入力にエラーが検出されました！再入力願います。'
            context = contextSetWMessage( request.session['sessionKanriNo'], request.session['sessionEdaban'], message)
            return render(request, 'ankenkanri/keiyakusyoTeiketsuKan6.html', context)

        ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=6)
        edabanTemp = request.session['sessionEdaban']
        if (edabanTemp is None) or (edabanTemp == ""):
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
                statusCode = 6,
                onatsuRingiNo = form.cleaned_data.get('onatsuRingiNo'),
                onatsuRingiLink = form.cleaned_data.get('onatsuRingiLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )
        else:
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
                statusCode = 6,
                onatsuRingiNo = form.cleaned_data.get('onatsuRingiNo'),
                onatsuRingiLink = form.cleaned_data.get('onatsuRingiLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )
        print("Detected the confirm button in dp60 button6")
        request.session['sessionDisplayCode'] = 'dp11'  
        return render(request, 'ankenkanri/page_n.html', context)
    else:
        request.session['sessionDisplayCode'] = 'dp60'
        return render(request, 'ankenkanri/keiyakusyoTeiketsuKan6.html')    

## 注文処理完了画面でボタンが押された
def cyuumonSave(request):
    print("Arrived L398 !!!")
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    if "pageTop" in request.POST:
        print("Detected the pageTop-button(in dp70)")
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif "skipPage6to7" in request.POST:
        setStatusCodeCEdaban(request, 7) 
        print("Detected the skip-button(in dp70)")
        request.session['sessionDisplayCode'] = 'dp70'
        context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
        return render(request, 'ankenkanri/page_n.html', context)
    elif  "confirm" in request.POST:
        if (request.POST.get('chumonTanka') is None) or (request.POST.get('chumonTanka') == "") :          ### 空文字検出　いまいち！
            print('Detect 空文字！')
            request.session['sessionDisplayCode'] = 'dp70' 
            return render(request, 'ankenkanri/cyuumonKan7.html', context)

        form = forms.cyuumonForm(request.POST)
        if form.is_valid():
            pass
        else:
            request.session['sessionDisplayCode'] = 'dp70' 
            message = '入力にエラーが検出されました！再入力願います。'
            context = contextSetWMessage( request.session['sessionKanriNo'], request.session['sessionEdaban'], message)
            return render(request, 'ankenkanri/cyuumonKan7.html', context)

        ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=7)
        edabanTemp = request.session['sessionEdaban']
        if dataCheck(int(form.cleaned_data.get('chumonTanka')), int(form.cleaned_data.get('chumonSuu'))) != 'NG':
            gokeiTemp = dataCheck(int(form.cleaned_data.get('chumonTanka')), int(form.cleaned_data.get('chumonSuu'))) 
        else:
            gokeiTemp = 0
        if (edabanTemp is None) or (edabanTemp == ""):
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
                statusCode = 7,
                chumonTanka = form.cleaned_data.get('chumonTanka'),
                chumonSuu = form.cleaned_data.get('chumonSuu'),
                chumonGokei = gokeiTemp,
                chumonLink = form.cleaned_data.get('chumonLink'),
                nohinKigen = form.cleaned_data.get('nohinKigen'),
                #kenshuKigen = form.cleaned_data.get('kenshuKigen'),
                shiharaiKigen = form.cleaned_data.get('shiharaiKigen'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )
        else:
            AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
                statusCode = 7,
                chumonTanka = form.cleaned_data.get('chumonTanka'),
                chumonSuu = form.cleaned_data.get('chumonSuu'),
                chumonGokei = gokeiTemp,
                chumonLink = form.cleaned_data.get('chumonLink'),
                nohinKigen = form.cleaned_data.get('nohinKigen'),
                #kenshuKigen = form.cleaned_data.get('kenshuKigen'),
                shiharaiKigen = form.cleaned_data.get('shiharaiKigen'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
            )            
        print("Detected the confirm button in dp70 button7")
        request.session['sessionDisplayCode'] = 'dp11'  
        return render(request, 'ankenkanri/page_n.html', context)
    else:
        request.session['sessionDisplayCode'] = 'dp70'
        return render(request, 'ankenkanri/cyuumonKan7.html')   

## kingakuWarning.html(納品処理の入力金額等間違いのワーニング画面)から分岐
def kingakuW(request):
    if "pageTop" in request.POST:
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif "kingakuIA" in request.POST: 
        context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
        return render(request, 'ankenkanri/nouhinKan8.html', context)
    else:
        request.session['sessionDisplayCode'] = 'dp80'
        return render(request, 'ankenkanri/kingakuWarning.html')  

## kingakuWarning2.html(請求書処理の入力金額等間違いのワーニング画面)から分岐
def kingakuW2(request):
    if "pageTop" in request.POST:
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif "kingakuIA" in request.POST: 
        context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
        return render(request, 'ankenkanri/seikyuusyoNyuusyu9.html', context)
    else:
        request.session['sessionDisplayCode'] = 'dp90'
        return render(request, 'ankenkanri/kingakuWarning2.html')  
  
## nouhinkan8.html(納品処理完画面)でボタンを押された
def nouhinSave(request):  
    print("Arrived L435 !!!")
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    if "pageTop" in request.POST:
        print("Detected the pageTop-button(in dp80)")
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif "skipPage7to8" in request.POST:
        setStatusCodeCEdaban(request, 8)  ## statusCode = 8
        print("Detected the skip-button(in dp80)")
        request.session['sessionDisplayCode'] = 'dp80'
        context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
        return render(request, 'ankenkanri/page_n.html', context)
    elif  "confirm" in request.POST:
        if (request.POST.get('nohinTanka') is None) or (request.POST.get('nohinTanka') == "") :          ### 空文字検出　いまいち！
            print('Detect 空文字！')
            request.session['sessionDisplayCode'] = 'dp80' 
            return render(request, 'ankenkanri/nouhinKan8.html', context)
        q = AnkenList.objects.filter(kanriNo=str(request.session['sessionKanriNo']))

        ##  注文書と納品書の金額比較　一致＞支払単価、数、納品書URLをDB登録、不一致＞警告画面
        if q[0].chumonGokei == int(request.POST.get('nohinTanka'))*int(request.POST.get('nohinSuu')):

            form = forms.nohinForm(request.POST)
            if form.is_valid():
                pass
            else:
                request.session['sessionDisplayCode'] = 'dp80' 
                message = '入力にエラーが検出されました！再入力願います。'
                context = contextSetWMessage( request.session['sessionKanriNo'], request.session['sessionEdaban'], message)
                return render(request, 'ankenkanri/nouhinKan8.html', context)

            ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=8)
            edabanTemp = request.session['sessionEdaban']
            if dataCheck(int(form.cleaned_data.get('nohinTanka')), int(form.cleaned_data.get('nohinSuu'))) != 'NG':
                gokeiTemp = dataCheck(int(form.cleaned_data.get('nohinTanka')), int(form.cleaned_data.get('nohinSuu'))) 
            else:
                gokeiTemp = 0
            if (edabanTemp is None) or (edabanTemp == ""):
                AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
                statusCode = 8,
                nohinTanka = form.cleaned_data.get('nohinTanka'),
                nohinSuu = form.cleaned_data.get('nohinSuu'),
                nohinGokei = gokeiTemp,
                nohinLink = form.cleaned_data.get('nohinLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
                )
            else:
                AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
                statusCode = 8,
                nohinTanka = form.cleaned_data.get('nohinTanka'),
                nohinSuu = form.cleaned_data.get('nohinSuu'),
                nohinGokei = gokeiTemp,
                nohinLink = form.cleaned_data.get('nohinLink'),
                status = ankenTemp[0].ankenStatus,
                saishuKoshinsha = str(request.user),
                dataKoshinbi = timezone.now()
                )
            print("請求書金額などをDBへ格納しました。Detected the 確定ボタン")
            request.session['sessionDisplayCode'] = 'dp11'   
            return render(request, 'ankenkanri/page_n.html', context)
        else:
            request.session['sessionDisplayCode'] = 'dp85'  
            return render(request, 'ankenkanri/kingakuWarning.html', context)
    else:
        request.session['sessionDisplayCode'] = 'dp80'
        return render(request, 'ankenkanri/nouhinKan8.html')  

 ## 親案件の場合、計画予算－購入合計（予算消化状況）算出→DBへ書込
def yosanShokaCheck():
    ankenList = AnkenList.objects.all()
    edaban0Record = AnkenList.objects.filter(edaban='0')   ## 枝番=0レコード抽出
    for edaban0Row in edaban0Record:
        edaban0Row.keikakuGokei = 0
        edaban0Row.mitsumoriGokei = 0
        edaban0Row.chumonGokei = 0
        edaban0Row.nohinGokei = 0        
        edaban0Row.konyuGokei = 0
        for ankenListRow in ankenList:
            if (edaban0Row.kanriNo == ankenListRow.kanriNo) and int(ankenListRow.edaban) != 0:
                edaban0Row.keikakuGokei = edaban0Row.keikakuGokei + ankenListRow.keikakuGokei
                edaban0Row.mitsumoriGokei = edaban0Row.mitsumoriGokei + ankenListRow.mitsumoriGokei
                edaban0Row.chumonGokei = edaban0Row.chumonGokei + ankenListRow.chumonGokei
                edaban0Row.nohinGokei = edaban0Row.nohinGokei + ankenListRow.nohinGokei
                edaban0Row.konyuGokei = edaban0Row.konyuGokei + ankenListRow.konyuGokei
        AnkenList.objects.filter(edaban=0).filter(kanriNo=edaban0Row.kanriNo).update(
            #keikakuGokei = edaban0Row.keikakuGokei,  ## ユーザが計画合計値を入力するため不要
            mitsumoriGokei = edaban0Row.mitsumoriGokei,
            chumonGokei = edaban0Row.chumonGokei,
            nohinGokei = edaban0Row.nohinGokei,
            konyuGokei = edaban0Row.konyuGokei            
        )
        # edaban0Row.update(
        #     keikakuGokei = edaban0Row.keikakuGokei,
        #     konyuGokei = edaban0Row.konyuGokei
        # )
    for edaban0Row in edaban0Record:  ## 計画予算（合計）－購入金額（合計）（枝番0のレコード）
        print('edaban0Row.kanriNo =', edaban0Row.kanriNo)
        print('edaban0Row.edaban = ', edaban0Row.edaban)
        print('keikaku_Jisseki =', edaban0Row.keikakuGokei - edaban0Row.konyuGokei)
        AnkenList.objects.filter(edaban='0').filter(kanriNo=edaban0Row.kanriNo).update(
            keikaku_Jisseki = edaban0Row.keikakuGokei - edaban0Row.konyuGokei
        )
        #edaban0Row.update(keikaku_Jisseki = edaban0Row.keikakuGokei - edaban0Row.konyuGokei)

    for row in ankenList:   ## 計画予算－購入金額（枝番なし、枝番0以外のレコード　）
        print('row.kanriNo =', row.kanriNo)
        print('row.edaban = ', row.edaban)
        print('type_edaban =', type(row.edaban))
        print('keikaku_Jisseki =', row.keikakuGokei - row.konyuGokei)
        if (row.edaban != '0')  :
            AnkenList.objects.filter(kanriNo=row.kanriNo).filter(edaban=row.edaban).update(
                keikaku_Jisseki = row.keikakuGokei - row.konyuGokei
            )
        elif (row.edaban is None) or (row.edaban == ''):
            AnkenList.objects.filter(kanriNo=row.kanriNo).update(
                keikaku_Jisseki = row.keikakuGokei - row.konyuGokei
            )
            # obj = AnkenList.objects.filter(~Q(Q(edaban='0'))|Q(edaban__isnull=True))
            # print('obj =', obj)
            # row.keikaku_Jisseki = row.keikakuGokei - row.konyuGokei
            # AnkenList.objects.filter(~Q(Q(edaban='0'))|Q(edaban__isnull=True)).update(
            #        keikaku_Jisseki = row.keikaku_Jisseki 
        


## 請求書情報入力画面でボタンが押された
def seikyuusyoSave(request): 
    print("Arrived L473 !!!")
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    if "pageTop" in request.POST:
        print("Detected the pageTop-button(in dp90)")
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif "skipPage8to9" in request.POST:
        setStatusCodeCEdaban(request, 9)   ## statusCode = 9
        print("Detected the skip-button(in dp90)")
        request.session['sessionDisplayCode'] = 'dp90'
        context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
        return render(request, 'ankenkanri/page_n.html', context)
    elif  "confirm" in request.POST:
        if (request.POST.get('shiharaiTanka') is None) or (request.POST.get('shiharaiTanka') == "") :          ### 空文字検出　いまいち！
            print('Detect 空文字！')
            request.session['sessionDisplayCode'] = 'dp90' 
            return render(request, 'ankenkanri/seikyuusyoNyuusyu9.html', context)
        q = AnkenList.objects.filter(kanriNo=str(request.session['sessionKanriNo'])).filter(edaban=request.session['sessionEdaban'])

        ##  注文書と請求書の金額比較　一致＞支払単価、数、請求書URLをDB登録、不一致＞警告画面
        if q[0].chumonGokei == int(request.POST.get('shiharaiTanka'))*int(request.POST.get('konyuSuu')) \
                               and q[0].keiyakushoNo == request.POST.get('keiyakushoNo'):

            form = forms.seikyuusyoForm(request.POST)
            if form.is_valid():
                pass
            else:
                request.session['sessionDisplayCode'] = 'dp90' 
                message = '入力にエラーが検出されました！再入力願います。'
                context = contextSetWMessage( request.session['sessionKanriNo'], request.session['sessionEdaban'], message)
                return render(request, 'ankenkanri/seikyuusyoNyuusyu9.html', context)

            ankenTemp = AnkenStatus.objects.filter(ankenStatusCode=9)
            edabanTemp = request.session['sessionEdaban']
            result = dataCheck(form.cleaned_data.get('shiharaiTanka'), form.cleaned_data.get('konyuSuu'))
            if result != 'NG':
                gokeiTemp = result 
            else:
                gokeiTemp = 0
            keikakuGokei = AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=request.session['sessionEdaban'])[0].keikakuGokei
            konyuGokei = AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=request.session['sessionEdaban'])[0].konyuGokei
            if (edabanTemp is None) or (edabanTemp == ""):  ## 枝番がなければ、すぐにDBを更新
                AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).update(
                    statusCode = 9,
                    shiharaiTanka = form.cleaned_data.get('shiharaiTanka'),
                    konyuSuu = form.cleaned_data.get('konyuSuu'),
                    konyuGokei = gokeiTemp,
                    seikyushoLink = form.cleaned_data.get('seikyushoLink'),
                    keikaku_Jisseki = (keikakuGokei - konyuGokei),
                    status = ankenTemp[0].ankenStatus,
                    saishuKoshinsha = str(request.user),
                    dataKoshinbi = timezone.now()            
                )
            else:
                if edabanTemp != 0: ## 親案件でなければ、購入合計金額を登録
                    AnkenList.objects.filter(kanriNo=request.session['sessionKanriNo']).filter(edaban=edabanTemp).update(
                        statusCode = 9,               
                        shiharaiTanka = form.cleaned_data.get('shiharaiTanka'),
                        konyuSuu = form.cleaned_data.get('konyuSuu'),
                        seikyushoLink = form.cleaned_data.get('seikyushoLink'),
                        konyuGokei = gokeiTemp,
                        keikaku_Jisseki = (keikakuGokei - konyuGokei),
                        status = ankenTemp[0].ankenStatus,
                        saishuKoshinsha = str(request.user),
                        dataKoshinbi = timezone.now()
                    )
                yosanShokaCheck()  ## 親案件の場合、計画予算－購入合計（予算消化状況）算出→DBへ書込

            print("請求書金額などをDBへ格納しました。Detected the 確定ボタン")
            request.session['sessionDisplayCode'] = 'dp11'   
            return render(request, 'ankenkanri/page_n.html', context)
        else:
            request.session['sessionDisplayCode'] = 'dp95'  
            return render(request, 'ankenkanri/kingakuWarning2.html', context)
    else:
        request.session['sessionDisplayCode'] = 'dp90'
        return render(request, 'ankenkanri/seikyuusyoNyuusyu9.html')  

def kingakuInputAgain(request):
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    request.session['sessionDisplayCode'] = 'dp80'  
    return render(request, 'ankenkanri/nouhinKan8.html', context)

def kingakuInputAgain2(request):
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])
    request.session['sessionDisplayCode'] = 'dp90' 
    return render(request, 'ankenkanri/seikyuusyoNyuusyu9.html', context)

## 支払処理完了確認画面でボタンが押された
def shiharaiSave(request):     ## 多分、支払処理が終わっときのここで、DBへの登録はstatus変更のみでしょう。
    context = contextSet( request.session['sessionKanriNo'], request.session['sessionEdaban'])

    if "pageTop" in request.POST:
        print("Detected the pageTop-button(in dp100)")
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')
    elif  "confirm" in request.POST:
        setStatusCodeCEdaban(request, 10)  ## statusCode = 10
        request.session['sessionDisplayCode'] = 'dp00' 
        return redirect('/ankenkanri2/index')      
    elif "pagePrev" in request.POST:
        request.session['sessionDisplayCode'] = 'dp11' 
        return render(request, 'ankenkanri/page_n.html', context)               
    else:
        request.session['sessionDisplayCode'] = 'dp100'   
        return render(request, 'ankenkanri/shiharaiKan10.html', context)