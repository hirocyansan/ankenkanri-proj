from django.db import models
from django.utils import timezone

# Create your models here.
class AnkenList(models.Model):
    keiriShonin = models.BooleanField(null=True,blank=True)
    statusCode = models.IntegerField(null=True,blank=True)
    status = models.CharField(null=True,blank=True,max_length=30)
    edabanGroup = models.IntegerField(null=True,blank=True)
    shiharaiPattern = models.IntegerField(null=True,blank=True)
    kanriNo = models.CharField(null=True,blank=True,max_length=30)
    edaban = models.CharField(null=True,blank=True,max_length=30)
    ankenMei = models.CharField(null=True,blank=True,max_length=100)
    torihikisakiCode = models.IntegerField(null=True,blank=True)
    torihikisakiMei = models.CharField(null=True,blank=True,max_length=30)
    kanjokamokuCode = models.IntegerField(null=True,blank=True)
    kanjokamoku = models.CharField(null=True,blank=True,max_length=30)
    keikakuTanka = models.IntegerField(null=True,blank=True)
    keikakuSuu = models.IntegerField(null=True,blank=True)
    keikakuGokei = models.IntegerField(null=True,blank=True)
    mitsumoriTanka = models.IntegerField(null=True,blank=True)
    mitsumoriSuu = models.IntegerField(null=True,blank=True)
    mitsumoriGokei = models.IntegerField(null=True,blank=True)
    mitsumoriLink = models.URLField(null=True,blank=True)
    ringiTanka = models.IntegerField(null=True,blank=True)
    ringiSuu = models.IntegerField(null=True,blank=True)
    ringiGokei = models.IntegerField(null=True,blank=True)
    ringishoNo = models.CharField(null=True,blank=True,max_length=30)
    ringishoLink = models.URLField(null=True,blank=True)
    wfNo = models.CharField(null=True,blank=True,max_length=30)
    keiyakuKingaku = models.IntegerField(null=True,blank=True)
    keiyakushoNo = models.CharField(null=True,blank=True,max_length=30)
    keiyakushoLink = models.URLField(null=True,blank=True)
    onatsuRingiNo = models.CharField(null=True,blank=True,max_length=30)
    onatsuRingiLink = models.URLField(null=True,blank=True)
    chumonTanka = models.IntegerField(null=True,blank=True)
    chumonSuu = models.IntegerField(null=True,blank=True)
    chumonGokei = models.IntegerField(null=True,blank=True)
    chumonLink = models.URLField(null=True,blank=True)
    nohinKigen = models.DateField(null=True,blank=True)
    # kenshuKigen = models.DateTimeField(null=True,blank=True)
    shiharaiKigen = models.DateField(null=True,blank=True)
    nohinTanka = models.IntegerField(null=True,blank=True)
    nohinSuu = models.IntegerField(null=True,blank=True)
    nohinGokei = models.IntegerField(null=True,blank=True)
    nohinLink = models.URLField(null=True,blank=True)
    shiharaiTanka = models.IntegerField(null=True,blank=True)
    konyuSuu = models.IntegerField(null=True,blank=True)
    konyuGokei = models.IntegerField(null=True,blank=True)
    seikyushoLink = models.URLField(null=True,blank=True)
    keikaku_Jisseki = models.IntegerField(null=True,blank=True)
    kurikaeshiKigen = models.DateField(null=True,blank=True)
    konyuKaisha = models.CharField(null=True,blank=True,max_length=30)
    dataKoshinbi = models.DateTimeField(default=timezone.datetime.now)
    saishuKoshinsha = models.CharField(null=True,blank=True,max_length=30)
    shainNo = models.IntegerField(null=True,blank=True)
    tantosha = models.CharField(null=True,blank=True,max_length=30)
    comment = models.CharField(null=True,blank=True,max_length=30)
    hyojijun = models.IntegerField(null=True,blank=True)

    class Meta:
        db_table = 'ankenListTable'
    def __str__(self):
        return f'{self.ankenMei}'      

    
class AnkenStatus(models.Model):
    ankenStatusCode = models.IntegerField(null=True,blank=True)
    ankenStatus = models.CharField(null=True,blank=True,max_length=30)

    class Meta:
        db_table = 'ankenStatusTable'
    def __str__(self):
        return f'{self.ankenStatus}'      


class AnkenShiharaiPattern(models.Model):
    ankenShiharaiPatternCode = models.IntegerField(null=True,blank=True)
    abkenShiharaiPattern = models.CharField(null=True,blank=True,max_length=30)

    class Meta:
        db_table = 'ankenShiharaiPatternTable'
    def __str__(self):
        return f'{self.abkenShiharaiPattern}'      

class AnkenTorihikisaki(models.Model):
    ankenTorihikisakiCode = models.IntegerField(null=True,blank=True)
    ankenTorihikisakiKaisha = models.CharField(null=True,blank=True,max_length=30)
    ankenTorihikisakiTantosha = models.CharField(null=True,blank=True,max_length=30)
    ankenTorihikisakiJusho = models.CharField(null=True,blank=True,max_length=30)
    ankenTorihikisakiTel = models.CharField(null=True,blank=True,max_length=30)

    class Meta:
        db_table = 'ankenTorihikisakiTable'
    def __str__(self):
        return f'{self.ankenTorihikisakiKaisha}'   
    
    
class AnkenTantosha(models.Model):
    ankenTantoshaCode = models.IntegerField(null=True,blank=True)
    ankenTantoshaMei = models.CharField(null=True,blank=True,max_length=30)

    class Meta:
        db_table = 'ankenTantoshaTable'
    def __str__(self):
        return f'{self.ankenTantoshaMei}'      
   

class AnkenKanjokamoku(models.Model):
    ankenKanjokamokuCode = models.IntegerField(null=True,blank=True)
    ankenKanjokamoku = models.CharField(null=True,blank=True,max_length=30)

    class Meta:
        db_table = 'ankenKanjokamokuTable'
    def __str__(self):
        return f'{self.ankenKanjokamoku}'      
