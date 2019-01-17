from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import numpy as np
from openpyxl import load_workbook

class find_news:

    def generate_url(self, keywords):
        return "https://search.naver.com/search.naver?query="+self.generate_keyword(keywords)+"&where=news&ie=utf8&sm=nws_hty'"

    def generate_keyword(self, keywords):
        kw = ''
        for i in range(len(keywords)):
            if i == len(keywords)-1:
                kw += keywords[i]
            else:
                kw += keywords[i]+"+"
        return kw

    def find_title_navernews(self, url):

        page_response = requests.get(url, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        urls = page_content.findAll('a', attrs={"class": "_sp_each_url _sp_each_title"})

        start = '+urlencode(this.href));" target="_blank" title='
        end = '<strong class="hl"'

        url_list = []

        for i in range(len(urls)):
            url_list.append(str(urls[i])[str(urls[i]).find(start) + len(start):str(urls[i]).find(end)].
                            replace("\'","").replace('"','').replace(">","").replace("<",""))

        return url_list

    def find_url_navernews(self, url):

        page_response = requests.get(url, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        urls = page_content.findAll('a', attrs={"class": "_sp_each_url _sp_each_title"})

        start = 'href="'
        end = '" onclick="return goOtherCR'

        url_list = []

        for i in range(len(urls)):
            url_list.append(str(urls[i])[str(urls[i]).find(start)+len(start):str(urls[i]).rfind(end)])

        return url_list

if __name__ == "__main__":
    insert_keywords = [['현대카드', '정태영'],
                       ['현대', '카드사업', '오토에버'],
                       ['현대카드', '부진', '책임'],
                       ['현대카드', '약진'],
                       ['정태영', '리더십'],
                       ['정태영', '리더', '존경', '경영자']]
    tr = find_news()

    for i in range(len(insert_keywords)):
        page_link = tr.generate_url(insert_keywords[i])
        now = datetime.datetime.now()

        d = {'뉴스제목': tr.find_title_navernews(page_link),
             'URL': tr.find_url_navernews(page_link)}

        if i == 0:
            pd.DataFrame(data=d).to_excel('C:/Users/Devin/Naver_News_'+now.strftime("%Y%m%d-%H")+'.xlsx',
                                      sheet_name=tr.generate_keyword(insert_keywords[i]), index=False)
        else:
            path = 'C:/Users/Devin/Naver_News_'+now.strftime("%Y%m%d-%H")+'.xlsx'

            book = load_workbook(path)

            writer = pd.ExcelWriter(path, engine='openpyxl')
            writer.book = book

            pd.DataFrame(data=d).to_excel(writer, sheet_name=tr.generate_keyword(insert_keywords[i]),
                                          index=False)

            writer.save()
            writer.close()