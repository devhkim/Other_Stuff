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

print(str(datetime.datetime.now() - now) + " elapsed")
