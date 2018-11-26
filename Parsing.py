import re
import requests
import datetime
from bs4 import BeautifulSoup as BS

def get_html(url):
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html

def get_diet(ymd, weekday, code):
    schYmd = ymd
    schMmealSccode = code
    num = weekday + 1      # 일:0 월:1, ... , 토:6
    schCode = open("data\\URL.txt", 'r').readline().replace('\n', '')
    URL = (
            "https://stu.dge.go.kr/sts_sci_md01_001.do?"
            "&schulCode=%s&schulCrseScCode=4&schulKndScCode=04"
            "&schMmealScCode=%d&schYmd=%s" % (schCode, schMmealSccode, schYmd)
        )
    html = get_html(URL)
    soup = BS(html, "html.parser")
    element = soup.find_all("tr")
    element = element[2].find_all("td")
    element = element[num]
    element = str(element)
    element = element.replace('[', '')
    element = element.replace(']', '')
    element = element.replace('<br/>', '\n')
    element = element.replace('<td class="textC last">', '')
    element = element.replace('<td class="textC">', '')
    element = element.replace('</td>', '')
    element = element.replace('(h)', '')
    element = element.replace('.', '')
    element = re.sub(r"\d", "", element)

    return element


def dietExtract(meal):
    nowTime = datetime.datetime.now()
    todayDate = str(nowTime.date()).replace('-', '.')

    diet = get_diet(todayDate, nowTime.weekday(), meal)
    return diet