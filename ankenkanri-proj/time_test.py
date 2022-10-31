from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

# today
today = date.today()
print(today) # => 2016-04-19

# 1ヶ月後
dt = today + relativedelta(months=1)
print(dt) # => 2016-05-19

# 1年後
dt = today + relativedelta(years=1)
print(dt) # => 2017-04-19

# 月末
dt = today + relativedelta(months=1) - timedelta(days=today.day)
print(dt) # => 2016-04-30

print('timedelta(days=today.day) =', timedelta(days=today.day))

# 月初（これはtimedeltaで普通にできるけど、一応書いてみる）
dt = today - timedelta(days=today.day-1)
print(dt) # => 2016-04-01