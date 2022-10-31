from django import forms
from django.core import validators
from .models import AnkenList



class kanriNoForm(forms.Form):
    kanriNo = forms.CharField()
    edaban = forms.CharField(required=False)

    class Meta:
        model = AnkenList
        fields = '__all__'

class mitsumorisyoForm(forms.Form):
    mitsumoriTanka = forms.IntegerField()
    mitsumoriSuu = forms.IntegerField()
    mitsumoriLink = forms.URLField()

    class Meta:
        model = AnkenList
        fields = '__all__'

class ringiShoninForm(forms.Form):
    ringiTanka = forms.IntegerField()
    ringiSuu = forms.IntegerField()
    ringishoLink = forms.URLField()

    class Meta:
        model = AnkenList
        fields = '__all__'

class keiyakusyoSakuseiForm(forms.Form):
    wfNo = forms.CharField()
    keiyakushoNo = forms.CharField()
    keiyakuKingaku = forms.IntegerField()
    keiyakushoLink = forms.URLField()

    class Meta:
        model = AnkenList
        fields = '__all__'

class keiyakusyoTeiketsuForm(forms.Form):
    onatsuRingiNo = forms.CharField()
    keiyakushoNo = forms.CharField()
    ringishoLink = forms.URLField()

    class Meta:
        model = AnkenList
        fields = '__all__'

class cyuumonForm(forms.Form):
    chumonTanka = forms.IntegerField()
    chumonSuu = forms.IntegerField()
    nohinKigen = forms.DateTimeField()
    kenshuKigen = forms.DateTimeField()
    shiharaiKigen = forms.DateTimeField()

    class Meta:
        model = AnkenList
        fields = '__all__'

class nohinForm(forms.Form):
    nohinTanka = forms.IntegerField()
    nohinSuu = forms.IntegerField()

    class Meta:
        model = AnkenList
        fields = '__all__'

class seikyuusyoForm(forms.Form):
    shiharaiTanka = forms.IntegerField()
    konyuSuu = forms.IntegerField()
    keiyakushoNo = forms.CharField()

    class Meta:
        model = AnkenList
        fields = '__all__'


class formAnkenList(forms.ModelForm):



        
    keiriShonin = forms.BooleanField(label='経理承認',required=False)
    # statusCode = forms.IntegerField(label='ステータスコード',required=False)
    statusCode = forms.ChoiceField(label='ステータスコード',choices=(
        (0,'案件入力（作成中）'),
        (1,'案件入力（完成）'),
        (2,'見積書（作成依頼）'),
        (3,'見積書（入手済み）'),
        (4,'稟議書（承認完了）'),
        (5,'契約書（作成完了）'),
        (6,'契約書（締結完了）'),
        (7,'注文処理（完了）'),
        (8,'納品（完了）'),
        (9,'請求書（入手済み）'),
        (10,'支払処理（完了）'),
        (20,'案件無効状態'),
        (99,'親案件用')
    ))
    status = forms.CharField(label='案件ステータス',required=False)
    # status = forms.ChoiceField(label='案件ステータス',choices=(
    #     (0,'案件入力（作成中）'),
    #     (1,'案件入力（完成）'),
    #     (2,'見積書（作成依頼）'),
    #     (3,'見積書（入手済み）'),
    #     (4,'稟議書（承認完了）'),
    #     (5,'契約書（作成完了）'),
    #     (6,'契約書（締結完了）'),
    #     (7,'注文処理（完了）'),
    #     (8,'納品（完了）'),
    #     (9,'請求書（入手済み）'),
    #     (10,'支払処理（完了）')
    # ))
    edabanGroup = forms.IntegerField(label='枝番グループ',required=False)
    # shiharaiPattern = forms.IntegerField(label='支払パターン',required=False)
    shiharaiPattern = forms.ChoiceField(label='支払パターン',choices=(
        (0,'1回の支払いで完了'),
        (1,'繰り返し（月1回）、終了期限あり'),
        (2,'繰り返し（月1回）、終了期限なし'),
        (3,'繰り返し（年1回）、終了期限あり'),
        (4,'繰り返し（年1回）、終了期限なし'),
    ))
    kanriNo = forms.CharField(label='管理No.')
    edaban = forms.CharField(label='枝番')
    ankenMei = forms.CharField(label='案件名',max_length=100)
    # torihikisakiCode = forms.IntegerField(label='取引先コード',required=False)
    torihikisakiCode = forms.ChoiceField(label='取引先コード',choices=(
        (100001,'富士通JAPAN㈱'),
        (100002,'ミツイワ㈱'),
        (100003,'ソフトバンク㈱'),
        (100004,'㈱大塚商会'),
        (100005,'リコージャパン㈱'),
        (100006,'日立システムズ'),
        (100007,'三菱UFJリサーチ＆コンサルティング㈱'),
        (100008,'コムテック㈱'),
        (100009,'キャノンマーケティングジャパン㈱'),
        (100010,'GMOグローバルサインHD㈱'),
        (100000,'')
    ))
    torihikisakiMei = forms.CharField(label='取引先名',required=False)
    kanjokamokuCode= forms.ChoiceField(label='勘定科目コード',choices=(
        (10001,'現金'),
        (10002,'当座預金'),
        (10003,'普通預金'),
        (10004,'定期預金'),
        (10005,'受取手形'),
        (10006,'電子記録債権'),
        (10007,'売掛金'),
        (10008,'有価証券'),
        (10009,'濾紙商品（製品）'),
        (10010,'理化商品（製品）'),
        (10011,'半製品'),
        (10012,'仕掛品'),
        (10013,'仕入品'),
        (10014,'原材料'),
        (10015,'薬品'),
        (10016,'燃料'),
        (10017,'原紙'),
        (10018,'貯蔵品'),
        (10019,'短期貸付金'),
        (10020,'前払金'),
        (10021,'前払費用'),
        (10022,'立替金'),
        (10023,'未収入金'),
        (10024,'仮払金'),
        (10025,'仮払消費税'),
        (10026,'その他流動資産'),
        (10027,'貸倒引当金'),
        (10028,'建物'),
        (10029,'建物付属設備'),
        (10030,'構築物'),
        (10031,'機械及び装置'),
        (10032,'車両運搬具'),
        (10033,'工具、器具及び備品'),
        (10034,'金型'),
        (10035,'減価償却累計額'),
        (10036,'一括償却資産'),
        (10037,'土地'),
        (10038,'建設仮勘定'),
        (10039,'ソフトウェア'),
        (10040,'工業所有権'),
        (10041,'施設利用権'),
        (10042,'その他無形固定資産'),
        (10043,'ソフトウェア仮勘定'),
        (10044,'投資有価証券'),
        (10045,'関係会社株式'),
        (10046,'出資金'),
        (10047,'長期貸付金'),
        (10048,'差入保証金'),
        (10049,'敷金'),
        (10050,'長期前払費用'),
        (10051,'破産債権等'),
        (10052,'その他投資等'),
        (10053,'繰延資産'),
        (10054,'保証債務見返'),
        (10055,'支払手形'),
        (10056,'電子記録債務'),
        (10057,'買掛金'),
        (10058,'短期借入金'),
        (10059,'一年以内返済長期借入金'),
        (10060,'未払法人税等'),
        (10061,'仮受消費税'),
        (10062,'賞与引当金'),
        (10063,'未払金'),
        (10064,'前受金'),
        (10065,'預り金'),
        (10066,'前受収益'),
        (10067,'仮受金'),
        (10068,'その他流動負債'),
        (10069,'社債'),
        (10070,'長期借入金'),
        (10071,'役員退職慰労引当金'),
        (10072,'預り保証金'),
        (10073,'預り敷金'),
        (10074,'圧縮記帳引当金'),
        (10075,'間接費引当金'),
        (10076,'その他固定負債'),
        (10077,'保証債務'),
        (10078,'本社勘定'),
        (10079,'資本金'),
        (10080,'資本準備金'),
        (10081,'その他資本剰余金'),
        (10082,'利益準備金'),
        (10083,'退職手当基金'),
        (10084,'退職積立金'),
        (10085,'特別償却準備金'),
        (10086,'買換資産特別勘定'),
        (10087,'その他準備金'),
        (10088,'別途積立金'),
        (10089,'繰越利益剰余金'),
        (10090,'自己株式'),
        (10091,'有価証券評価差額金'),
        (10000,'')
    ))
    kanjokamoku = forms.CharField(label='勘定科目',required=False)
    keikakuTanka = forms.IntegerField(label='計画単価',required=False)
    keikakuSuu = forms.IntegerField(label='計画数',required=False)
    keikakuGokei = forms.IntegerField(label='計画合計金額',required=False)
    mitsumoriTanka = forms.IntegerField(label='見積単価',required=False)
    mitsumoriSuu = forms.IntegerField(label='見積数',required=False)
    mitsumoriGokei = forms.IntegerField(label='見積合計金額',required=False)
    mitsumoriLink = forms.URLField(label='見積書リンク',required=False)
    ringiTanka = forms.IntegerField(label='稟議書単価',required=False)
    ringiSuu = forms.IntegerField(label='稟議書数',required=False)
    ringiGokei = forms.IntegerField(label='稟議書合計',required=False)
    ringishoNo = forms.CharField(label='稟議書No.',required=False)
    ringishoLink = forms.URLField(label='稟議書リンク',required=False)
    wfNo = forms.CharField(label='ワークフローNo.',required=False)
    keiyakuKingaku = forms.IntegerField(label='契約金額',required=False)
    keiyakushoNo = forms.CharField(label='契約書No.',required=False)
    keiyakushoLink = forms.URLField(label='契約書リンク',required=False)
    onatsuRingiNo = forms.CharField(label='押捺稟議No.',required=False)
    onatsuRingiLink = forms.URLField(label='押捺稟議リンク',required=False)
    chumonTanka = forms.IntegerField(label='注文単価',required=False)
    chumonSuu = forms.IntegerField(label='注文数',required=False)
    chumonGokei = forms.IntegerField(label='注文合計金額',required=False)
    chumonLink = forms.URLField(label='注文書リンク',required=False)
    nohinKigen = forms.DateTimeField(label='納品日期限',required=False)
    kenshuKigen = forms.DateTimeField(label='検収日期限',required=False)
    shiharaiKigen = forms.DateTimeField(label='支払日期限',required=False)
    nohinTanka = forms.IntegerField(label='納品単価',required=False)
    nohinSuu = forms.IntegerField(label='納品数',required=False)
    nohinGokei = forms.IntegerField(label='納品合計金額',required=False)
    nohinLink = forms.URLField(label='納品書リンク',required=False)
    shiharaiTanka = forms.IntegerField(label='支払単価',required=False)
    konyuSuu = forms.IntegerField(label='購入数',required=False)
    konyuGokei = forms.IntegerField(label='購入合計金額',required=False)
    seikyushoLink = forms.URLField(label='請求書リンク情報',required=False)
    keikaku_Jisseki = forms.IntegerField(label='計画－実績',required=False)
    kurikaeshiKigen = forms.DateTimeField(label='支払繰返し期限',required=False)
    konyuKaisha = forms.CharField(label='購入会社',required=False)
    dataKoshinbi = forms.DateTimeField(label='最終データ更新日',required=False)
    saishuKoshinsha = forms.CharField(label='最終更新者',required=False)
    # shainNo = forms.IntegerField(label='社員番号',required=False)
    shainNo = forms.ChoiceField(label='社員番号',choices=(
        (90001,'伊豆猛'),
        (18083,'長田秀行'),
        (99003,'志田慶介'),
        (17048,'市ノ川弘彰'),
        (4023,'八木原暁宣'),
        (99005,'平原道高'),
        (17059,'荒木歩'),
        (0,'')
    ))
    tantosha = forms.CharField(label='担当者名',required=False)
    comment = forms.CharField(label='コメント',required=False)
    hyojijun = forms.IntegerField(label='表示順',required=False)

 
    class Meta:
        model = AnkenList
        fields = '__all__'

    # def __init__(self,*args,**kwargs):
    #     self.request = kwargs.pop("request")
    #     super (formAnkenList,self).__init__(*args,**kwargs)
        

