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

from quiz.interface import SessionUserInterface
from quiz.interface import StageResponseSerializer
from pdf.main import PdfFromHtmlDocument


inter = SessionUserInterface("356080087", 16)
lang = inter.get_language_model()
stages = inter.get_stages_queryset()
stages_json = [StageResponseSerializer(stage, lang).json() for stage in stages]

rep = PdfFromHtmlDocument("/Users/kirill/own-projects/freelance/pravo_bot/back/pdf/templates", "report.html")
rep.to_pdf(
        pdf_path="pdf.pdf",
        logo=rep.image_to_base64("/Users/kirill/own-projects/freelance/pravo_bot/back/pdf/images/logo.png"),
        title="",
        stages=stages_json
    )