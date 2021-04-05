# Django Environment activation stage
import os
import django
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('/Users/kirill/own-projects/freelance/pravo_bot/environments.env')
load_dotenv(dotenv_path=env_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
#####


# from quiz.interface import PeriodSessionStatistic
# from django.utils import timezone
#
#
# now = timezone.now()
# delta = timezone.timedelta(days=5)
#
# stat = PeriodSessionStatistic(now-delta, now)
# print(stat.get_json())

from django.db.models import Count, F
from django.db.models.functions import TruncDate, TruncDay
from quiz.models import Session
from django.db import connection
import json


stat = Session.objects.all()\
    .annotate(date=TruncDate('created_at'))\
    .values('date')\
    .annotate(total=Count('id'))\
    .values('date', 'total')
for el in stat:
    el["date"] = el["date"].isoformat()
print(list(stat))