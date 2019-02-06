from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import numpy as np
from openpyxl import load_workbook
import time

class find_news:

    def generate_url(self, keywords, itemnum):
        return "https://search.naver.com/search.naver?&where=news&query=" + \
               self.generate_keyword(keywords) + \
               "&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=23&start=" + \
               str(itemnum) + \
               "&refresh_start=0"

    def generate_sheet(self, keywords):
        kw = ''
        for i in range(len(keywords)):
            if i == len(keywords)-1:
                kw += keywords[i]
            else:
                kw += keywords[i]+"+"
        return kw

    def generate_keyword(self, keywords):
        kw = ''
        for i in range(len(keywords)):
            if i == len(keywords) - 1:
                kw += keywords[i]
            else:
                kw += keywords[i] + "%20"
        return kw

    def find_title_navernews(self, url):

        page_response = requests.get(url, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        urls = page_content.findAll('a', attrs={"class": "_sp_each_title"})

        start = '+urlencode(this.href));" target="_blank" title='
        end = '<strong class="hl"'

        url_list = []

        for i in range(len(urls)):
            url_list.append(str(urls[i])[str(urls[i]).find(start) + len(start):str(urls[i]).find(end)].
                            replace("\'","").replace('"','').replace(">","").replace("<","").replace("/a",""))

        return url_list

    def find_url_navernews(self, url):

        page_response = requests.get(url, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        urls = page_content.findAll('a', attrs={"class": "_sp_each_title"})

        start = 'href="'
        end = '" onclick="return goOtherCR'

        url_list = []

        for i in range(len(urls)):
            url_list.append(str(urls[i])[str(urls[i]).find(start)+len(start):str(urls[i]).rfind(end)])

        return url_list

if __name__ == "__main__":

    while True:

        insert_keywords = [['정태영'],
                           ['현대카드'],
                           ['현대캐피탈'],
                           ['현대카드', '정태영'],
                           ['현대커머셜']]
        now = datetime.datetime.now()
        tr = find_news()
        excelname = 'Naver_News_' + now.strftime("%Y%m%d-%H%M") + '.xlsx'
        try:
            for i in range(len(insert_keywords)):
                for j in range(3):
                    page = lambda x: 1+x*10
                    page_link = tr.generate_url(insert_keywords[i], page(j))

                    if j == 0:
                        d = {'뉴스제목': tr.find_title_navernews(page_link),
                             'URL': tr.find_url_navernews(page_link)}
                    else:
                        d['뉴스제목'].extend(tr.find_title_navernews(page_link))
                        d['URL'].extend(tr.find_url_navernews(page_link))

                if i == 0:
                    pd.DataFrame(data=d).to_excel(excelname, sheet_name=tr.generate_sheet(insert_keywords[i]), index=False)
                else:
                    path = excelname

                    book = load_workbook(path)

                    writer = pd.ExcelWriter(path, engine='openpyxl')
                    writer.book = book

                    pd.DataFrame(data=d).to_excel(writer, sheet_name=tr.generate_sheet(insert_keywords[i]),
                                                  index=False)

                    writer.save()
                    writer.close()
        except:
            pass

        print(excelname)

        time.sleep(250)