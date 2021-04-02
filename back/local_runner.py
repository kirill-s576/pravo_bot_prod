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


from quiz.models import Message, QButton
import openpyxl

msgs = QButton.objects.all()

wb = openpyxl.Workbook()
ws = wb.active

ws.cell(1, 1).value = "Id"
ws.cell(1, 2).value = "Text"

for number, msg in enumerate(msgs):
    ws.cell(number + 2, 1).value = msg.id
    ws.cell(number + 2, 2).value = msg.default_text

wb.save("buttons_dump.xlsx")