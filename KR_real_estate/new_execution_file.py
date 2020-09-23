import Apt_Reat_transaction_scraper as apt
import datetime
import pandas as pd
import pymongo

#to track time
now = datetime.datetime.now()

#make batches to

#get the apt price class
apt_price = apt.APT()

#import the dictionary via the method
#to use local, type in 0 for dbname (5th parameter)
# get the "xxx" values from Google Keep
apt_price.get_to_mdb(1, 2015, 8, 2020,
                   "C:\\Users\\Devin\\Downloads\\reg_code_test.xlsx",
                   "xxx",
                   "xxx",
                   "xxx",
                   0,
                   "Real_Estate",
                   "Seoul_real_price_201501_now")

#convert the dictionary to a dataframe
# dff = pd.DataFrame(dic)

#save the DF to local as an excel file
# xlsxname = 'AptTransInfo_'+now.strftime("%Y%m%d-%H%M") + '.xlsx'
# dff.to_excel('C:\\Users\\Devin\\Desktop\\NYSE_listing\\'+xlsxname, index = False)

#save the dictionary to MongoDB
# client = pymongo.MongoClient('mongodb+srv://devin:Deutsches7@devin01.x59h7.mongodb.net/test?retryWrites=true&w=majority')
# db = client['01_realestate']
# collection = db['01_APT_transaction_realprice']
# collection.insert(dic)
#collection.find()

print(str(datetime.datetime.now() - now) + " elapsed")
