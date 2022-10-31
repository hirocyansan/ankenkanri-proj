from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler

from .views.views4 import yosanShokaCheck


def periodic_execution():# 任意の関数名
    # ここに定期実行したい処理を記述する
    pass
    #yosanShokaCheck()
    #print('calculate keikaku_Jisseki by 5seconds ')

def start():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(periodic_execution, 'cron', hour=23, minute=59)# 毎日23時59分に実行
    #scheduler.add_job(periodic_execution, 'interval', seconds=10)
    scheduler.add_job(periodic_execution, 'interval', days=1)
    scheduler.start()