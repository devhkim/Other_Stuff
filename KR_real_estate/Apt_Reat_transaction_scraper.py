from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime as dt
import pymongo

class APT:
    def URL_generator(self, yearmonth, region_code, ser_key):
        # Access MOLIT open api to scrape relevant data from
        URL = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?LAWD_CD="+ \
              str(region_code) + \
              "&DEAL_YMD=" + str(yearmonth) + "&serviceKey=" + str(ser_key) + \
              "&numOfRows=10000&pageNo=1"
        return URL

    def regional_code(self, directory):
        reg_code = list(pd.read_excel(directory, "Sheet2")["Code"])
        return reg_code

    def regions(self, directory):
        reg = pd.read_excel(directory, "Sheet2")
        return reg

    def period_generator(self, startmonth, startyear, endmonth, endyear):

        #set start and ending dates in datetime format
        start = dt.date(startyear, startmonth, 15)
        end = dt.date(endyear, endmonth,15)

        #collect all dates between start and ending date
        dates = []
        days = 0
        while dt.timedelta(days) <= end - start:
            dates.append(start + dt.timedelta(days))
            days+=30

        #convert saved dates to MOLIT URL format
        dates_formated = []
        for i in dates:
            dates_formated.append(str(i)[0:4] + str(i)[5:7])

        return dates_formated

    def server_connector(self, id, pw, dbname):
        return "mongodb+srv://"+id+":"+pw+"@devin01.x59h7.mongodb.net/"+dbname+"?retryWrites=true&w=majority"

    def get_to_mdb(self, start_month, start_year, end_month, end_year, regions_directory, ser_key, id, pw, dbname, subdb, collname):

        #connect to mongodb server
        if dbname != 0:
            client = pymongo.MongoClient(self.server_connector(id, pw, dbname))
        else:
            client = pymongo.MongoClient()
        db = client[subdb]
        collection = db[collname]

        # fetch the regional codes
        reg = self.regional_code(regions_directory)

        # fetch the period of query
        per = self.period_generator(start_month, start_year, end_month, end_year)

        # generate and save the URLs subject to query
        paths = []
        for code in reg:
            for date in per:
                paths.append(self.URL_generator(date, code, ser_key))

        # fetch and insert data into mongodb
        for url in paths:
            find_all = list(BeautifulSoup((requests.get(url, timeout=5)).content, "html.parser").findAll('item'))
            for n in range(len(find_all)):
                dictt = {}

                # amount of transaction
                try:
                    dictt["amount"]= \
                        int(str(find_all[n])[str(find_all[n]).find('거래금액&gt;')+8:str(find_all[n]).
                            find('<!--거래금액-->&lt')].replace(",", "").replace(" ", ""))
                except:
                    dictt["amount"] = 0

                #date of transaction
                try:
                    dictt["date of transaction"] =\
                        dt.datetime.combine(dt.date(
                        int(str(find_all[n])[str(find_all[n]).find('lt;년&gt;')+8:str(find_all[n]).find('<!--년-->&lt')]),
                        int(str(find_all[n])[str(find_all[n]).find('lt;월&gt;')+8:str(find_all[n]).find('<!--월-->')]),
                        int(str(find_all[n])[str(find_all[n]).find('lt;일&gt;')+8:str(find_all[n]).find('<!--일-->')])), dt.time())
                except:
                    dictt["date of transaction"] = dt.datetime.combine(dt.date(1900,1,1), dt.time())

                #district name
                try:
                    dictt["district"] =\
                        str(find_all[n])[str(find_all[n]).find(';법정동&gt;')+8:str(find_all[n]).find('<!--법정동-->')].\
                            replace(" ", "")
                except:
                    dictt["district"] = "N.A."

                #region code
                if len(str(find_all[n])[str(find_all[n]).find('&lt;도로명시군구코드&gt;')+
                                        16:str(find_all[n]).find('<!--도로명시군구코드-->')].replace(" ", "")) <= 5:
                    dictt["region code"] = str(find_all[n])[str(find_all[n]).find('&lt;도로명시군구코드&gt;')+16:str(find_all[n]).
                        find('<!--도로명시군구코드-->')].replace(" ", "")
                elif len(str(find_all[n])[str(find_all[n]).find('&lt;법정동시군구코드&gt;') + 16:str(find_all[n]).
                        find('<!--법정동시군구코드-->')].replace(" ", "")) <= 5:
                    dictt["region code"] = str(find_all[n])[str(find_all[n]).find('&lt;법정동시군구코드&gt;') + 16:str(find_all[n]).
                        find('<!--법정동시군구코드-->')].replace(" ", "")
                else:
                    dictt["region code"] = "N.A."

                #get floor
                try:
                    dictt["floor"] =\
                        int(str(find_all[n])[str(find_all[n]).find('lt;층&gt;')+8:str(find_all[n]).find('<!--층-->')])
                except:
                    dictt["floor"] = 0

                # year of completion
                try:
                    dictt["year of completion"] =\
                        int(str(find_all[n])[str(find_all[n]).find('건축년도&gt;')+8:str(find_all[n]).find('<!--건축년도-->')])
                except:
                    dictt["year of completion"] =0

                # Apt name
                try:
                    dictt["APT Name"] = \
                        str(find_all[n])[str(find_all[n]).find(';아파트&gt;')+8:str(find_all[n]).find('<!--아파트-->')]
                except:
                    dictt["APT Name"] = "N.A."

                #size of apt
                try:
                    dictt["size"] = \
                        float(str(find_all[n])[str(find_all[n]).find('전용면적&gt;')+8:str(find_all[n]).find('<!--전용면적-->')])
                except:
                    dictt["size"] =0

                #street of address
                if len(str(find_all[n])[str(find_all[n]).find(';도로명&gt;')+8:str(find_all[n]).find('<!--도로명-->')]) <= 200:
                    dictt["street"] = \
                        str(find_all[n])[str(find_all[n]).find(';도로명&gt;')+8:str(find_all[n]).find('<!--도로명-->')]
                else:
                    dictt["street"] = "N.A."

                # upload the dictionary to the server
                collection.insert(dictt)