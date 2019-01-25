import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime
from openpyxl import load_workbook

class find_tweet:

    def generate_url(self, keywords):
        return "https://twitter.com/search?q=" + self.generate_keyword(keywords) + "&src=typd&lang=ko"

    def generate_keyword(self, keywords):
        kw = ''
        for i in range(len(keywords)):
            if i == len(keywords) - 1:
                kw += keywords[i]
            else:
                kw += keywords[i] + "%20"
        return kw

    def generate_sheet(self, keywords):
        kw = ''
        for i in range(len(keywords)):
            if i == len(keywords)-1:
                kw += keywords[i]
            else:
                kw += keywords[i]+"+"
        return kw

    def find_tweet_title_url(self, keywords):
        browser = webdriver.Ie(executable_path=
                               "/Users/Devin/Downloads/python-3.5.2-0/Lib/twitterscraper/chromedriver")
        browser.get(self.generate_url(keywords))
        time.sleep(1)

        body = browser.find_element_by_tag_name('body')

        for _ in range(5):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

        tweets = browser.find_elements_by_class_name('tweet-text')
        urls = browser.find_element_by_xpath('.//a')

        dict, listoftweets, listofurls, urlss, lasturl = {}, [], [], [], []

        for tweet in tweets:
            listoftweets.append(tweet.text)

        for url in browser.find_elements_by_xpath('.//a'):
            listofurls.append(url.get_attribute('href'))

        for i in range(len(listofurls)):
            urlss.append(str(listofurls[i]))

        urlss = [s for s in urlss if 'status' in s]

        for i in urlss:
            if i == "http://status.twitter.com/":
                pass
            else :
                lasturl.append(i)

        dict["Tweet"], dict["URL"] = listoftweets, list(self.f7(lasturl))

        return dict

    def f7(self, seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

if __name__ == "__main__":

    insert_keywords = [['현대카드', 'RPA'],
                       ['정태영', '현대'],
                       ['Bill Gates', 'Microsoft']]
    now = datetime.datetime.now()
    lt = find_tweet()
    excelname = 'C:/Users/Devin/Twitter_Posts_' + now.strftime("%Y%m%d-%H%M") + '.xlsx'

    for i in range(len(insert_keywords)):
        page_link = lt.generate_url(insert_keywords[i])
        d = lt.find_tweet_title_url(insert_keywords[i])

        if i == 0:
            pd.DataFrame(data=d).to_excel(excelname, sheet_name=lt.generate_sheet(insert_keywords[i]), index=False)
        else:
            path = excelname

            book = load_workbook(path)

            writer = pd.ExcelWriter(path, engine='openpyxl')
            writer.book = book

            pd.DataFrame(data=d).to_excel(writer, sheet_name=lt.generate_sheet(insert_keywords[i]), index=False)

            writer.save()
            writer.close()
