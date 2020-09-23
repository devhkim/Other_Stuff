import Apt_Real_Transaction_Price_Scraper as apt
import datetime
import pandas as pd
import pymongo

#to track time
now = datetime.datetime.now()

#make batches to

#get the apt price class
apt_price = apt.APT()

#import the dictionary via the method
dic = apt_price.get_info(7, 2020, 8, 2020, "C:\\Users\\Devin\\Downloads\\reg_code_test.xlsx", "wUOXLKQdCOC0%2Bsb3KGxk2OB5gj2x5Xx9f%2FEPusoDZ%2Bu18FxLLpXe6zwa7R4BGIRSWsS7skivQuNt9R48GJ27Hw%3D%3D")

#convert the dictionary to a dataframe
# dff = pd.DataFrame(dic)

#save the DF to local as an excel file
# xlsxname = 'AptTransInfo_'+now.strftime("%Y%m%d-%H%M") + '.xlsx'
# dff.to_excel('C:\\Users\\Devin\\Desktop\\NYSE_listing\\'+xlsxname, index = False)

#save the dictionary to MongoDB
client = pymongo.MongoClient('mongodb+srv://devin:Deutsches7@devin01.x59h7.mongodb.net/test?retryWrites=true&w=majority')
db = client['01_realestate']
collection = db['01_APT_transaction_realprice']
collection.insert(dic)
#collection.find()

print(str(datetime.datetime.now() - now) + " elapsed")