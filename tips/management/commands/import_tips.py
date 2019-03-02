import sys

from bs4 import BeautifulSoup
import requests

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from tips.models import Tip

PYBITES = 'pybites'
PYBITES_HAS_TWEETED = f'{PYBITES}/status'
TIPS_PAGE = 'https://codechalleng.es/tips'


class Command(BaseCommand):
    """Quick and dirty, using bs4 from last article:
       https://github.com/pybites/blog_code/blob/master/tips/tips.py

       About django-admin commands:
       https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/
    """
    help = 'Script to insert pybites tips from platform'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=PYBITES)
        except User.DoesNotExist:
            error = 'Cannot run this without SU pybites'
            sys.exit(error)

        tips = Tip.objects.count()
        if tips > 0:
            error = 'Tips already imported'
            sys.exit(error)

        html = requests.get(TIPS_PAGE)
        soup = BeautifulSoup(html.text, 'html.parser')
        trs = soup.findAll("tr")

        tips = []
        for tr in trs:
            tds = tr.find_all("td")
            tip_html = tds[1]

            links = tip_html.findAll("a", class_="left")
            first_link = links[0].attrs.get('href')

            pre = tip_html.find("pre")
            code = pre and pre.text or None

            # skip if tweeted or not code in tip
            share_link = None
            if PYBITES_HAS_TWEETED in first_link:
                share_link = first_link

            tip = tip_html.find("blockquote").text
            src = len(links) > 1 and links[1].attrs.get('href') or None

            tips.append(Tip(tip=tip, code=code, link=src,
                            user=user, approved=True,
                            share_link=share_link))

        Tip.objects.bulk_create(tips)

        print(f'Done: {len(tips)} tips imported')
