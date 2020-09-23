from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime as dt

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

    def get_info(self, start_month, start_year, end_month, end_year, regions_directory, ser_key):

        #fetch the regional codes
        reg = self.regional_code(regions_directory)

        #fetch the period of query
        per = self.period_generator(start_month, start_year, end_month, end_year)

        #generate and save the URLs subject to query
        paths = []
        for code in reg:
            for date in per:
                paths.append(self.URL_generator(date, code, ser_key))

        #define required info
        amount = []
        date_of_transaction = []
        district = []
        region_code = []
        floor = []
        year_of_completion = []
        APT_Name = []
        size = []
        street = []
        region = []

        #examine the lengths and contents of all paths
        find_alls = []
        for url in paths:
            find_alls.append(list(BeautifulSoup((requests.get(url, timeout=5)).content, "html.parser").findAll('item')))

        #scrape required info
        for find_all in find_alls:
            for n in range(len(find_all)):
            #get amount
                try:
                    amount_index_start = str(find_all[n]).find('거래금액&gt;')+8
                    amount_index_end = str(find_all[n]).find('<!--거래금액-->&lt')
                    amount.append(int(str(find_all[n])[amount_index_start:amount_index_end].replace(",", "").replace(" ", "")))
                except:
                    amount.append(0)

                #get date of transaction
                try:
                    year_index_start = str(find_all[n]).find('lt;년&gt;')+8
                    year_index_end = str(find_all[n]).find('<!--년-->&lt')
                    yr = int(str(find_all[n])[year_index_start:year_index_end])

                    month_index_start = str(find_all[n]).find('lt;월&gt;')+8
                    month_index_end = str(find_all[n]).find('<!--월-->')
                    mt = int(str(find_all[n])[month_index_start:month_index_end])

                    day_index_start = str(find_all[n]).find('lt;일&gt;')+8
                    day_index_end = str(find_all[n]).find('<!--일-->')
                    dy = int(str(find_all[n])[day_index_start:day_index_end])

                    date_of_transaction.append(dt.datetime.combine(dt.date(yr, mt, dy), dt.time()))

                except:
                    date_of_transaction.append(dt.datetime.combine(dt.date(1900,1,1), dt.time()))

                #get district name
                try:
                    district_index_start = str(find_all[n]).find(';법정동&gt;')+8
                    district_index_end = str(find_all[n]).find('<!--법정동-->')
                    district.append(str(find_all[n])[district_index_start:district_index_end].replace(" ", ""))
                except:
                    district.append("N.A.")

                #get region code and region
                try:
                    code_index_start = str(find_all[n]).find('&lt;도로명시군구코드&gt;')+16
                    code_index_end = str(find_all[n]).find('<!--도로명시군구코드-->')
                    code2_index_start = str(find_all[n]).find('&lt;법정동시군구코드&gt;') + 16
                    code2_index_end = str(find_all[n]).find('<!--법정동시군구코드-->')
                    if len(str(find_all[n])[code_index_start:code_index_end].replace(" ", "")) <= 5:
                        region_code.append(str(find_all[n])[code_index_start:code_index_end].replace(" ", ""))
                    elif len(str(find_all[n])[code2_index_start:code2_index_end].replace(" ", "")) <= 5:
                        region_code.append(str(find_all[n])[code2_index_start:code2_index_end].replace(" ", ""))
                    else:
                        region_code.append("N.A.")
                except:
                    region_code.append("N.A.")

                #get floor
                try:
                    flr_index_start = str(find_all[n]).find('lt;층&gt;')+8
                    flr_index_end = str(find_all[n]).find('<!--층-->')
                    floor.append(int(str(find_all[n])[flr_index_start:flr_index_end]))
                except:
                    floor.append(0)

                #year of completion
                try:
                    yoc_index_start = str(find_all[n]).find('건축년도&gt;')+8
                    yoc_index_end = str(find_all[n]).find('<!--건축년도-->')
                    year_of_completion.append(int(str(find_all[n])[yoc_index_start:yoc_index_end]))
                except:
                    year_of_completion.append(0)

                #APT name
                try:
                    apt_index_start = str(find_all[n]).find(';아파트&gt;')+8
                    apt_index_end = str(find_all[n]).find('<!--아파트-->')
                    APT_Name.append(str(find_all[n])[apt_index_start:apt_index_end])
                except:
                    APT_Name.append("N.A.")

                #size of APT
                try:
                    size_index_start = str(find_all[n]).find('전용면적&gt;')+8
                    size_index_end = str(find_all[n]).find('<!--전용면적-->')
                    size.append(float(str(find_all[n])[size_index_start:size_index_end]))
                except:
                    size.append(0)

                #name of the street
                try:
                    str_index_start = str(find_all[n]).find(';도로명&gt;')+8
                    str_index_end = str(find_all[n]).find('<!--도로명-->')
                    if len(str(find_all[n])[str_index_start:str_index_end]) <= 200:
                        street.append(str(find_all[n])[str_index_start:str_index_end])
                    else:
                        street.append("N.A.")
                except:
                    street.append("N.A.")

        #convert into a dictionary
        dictionary_real_estate = \
            {
                "amount" : amount,
                "date of transaction" : date_of_transaction,
                "district" : district,
                "region code" : region_code,
                "floor" : floor,
                "year of completion" : year_of_completion,
                "APT Name" : APT_Name,
                "size" : size,
                "street" : street
            }

        return dictionary_real_estate

if __name__ == "__main__":
    apt = APT()
    dict = apt.get_info(3, 2019, 5, 2019, "C:\\Users\\Devin\\Downloads\\reg_code_test.xlsx", "wUOXLKQdCOC0%2Bsb3KGxk2OB5gj2x5Xx9f%2FEPusoDZ%2Bu18FxLLpXe6zwa7R4BGIRSWsS7skivQuNt9R48GJ27Hw%3D%3D")
    print(dict)
