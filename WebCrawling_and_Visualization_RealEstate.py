# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 00:32:47 2022

@author: Jacob
"""

import pandas as pd
import numpy as np
import requests as req
import json    
import time
import random 
import matplotlib.pyplot as plt

def get_page_count(url, header):
    try:
        resp = req.get(url, headers=header)
        resp.raise_for_status()
        data=json.loads(resp.text)
        page_count=data['pa']['totalPageCount']
    except Exception as err:
        print(err)
        page_count=0
    return page_count

def web_one_page(url_p, header, ret_data):
    try:
        response = req.get(url_p, headers=header)
        response.raise_for_status()
        info = json.loads(response.text)
    except Exception as err:
        print(err)
    for a in range(len(info['webRentCaseGroupingList'])):
        ret_data.append(info['webRentCaseGroupingList'][a])
    return ret_data

#---------------------------------------------------------------------------------------------
#homework1
url = 'https://rent.houseprice.tw/ws/list/%E5%8F%B0%E4%B8%AD%E5%B8%82_city/%E8%A5%BF%E5%B1%AF%E5%8D%80_zip/'
header={
  'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
  }
ret_data = []
for i in range(get_page_count(url, header)):
    url_p = 'https://rent.houseprice.tw/ws/list/%E5%8F%B0%E4%B8%AD%E5%B8%82_city/%E8%A5%BF%E5%B1%AF%E5%8D%80_zip/?p={}'.format(i+1)
    web_one_page(url_p, header, ret_data)
    
df = pd.DataFrame(ret_data)
df.columns.unique()
dataset = df.iloc[:, [2, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16, 18, 19, 22, 23, 27, 37]]
#dataset.to_csv('D0790192_rent.csv', index=False)

#homework2
studio = dataset[dataset['rentPurPoseName'].isin(['獨立套房', '分租套房'])]
studio_price = studio['rentPrice']
plt.figure(figsize=(12, 6)).suptitle('台中市西屯區套房租金價格分布圖', fontsize=20)
plt.hist(studio_price, bins=10, edgecolor='white')
plt.ticklabel_format(style='plain')
plt.xticks(np.arange(0, studio_price.max(), 5000))
plt.show()

#homework3
rentPurPoseName = dataset.groupby('rentPurPoseName')['rentPrice'].mean()
rentPurPoseName_ind = rentPurPoseName.reset_index()
plt.figure(figsize=(14, 6)).suptitle('台中市西屯區各類型物件的平均價格', fontsize=20)
plt.rcParams["font.family"]=["Microsoft JhengHei"] 
plt.bar(rentPurPoseName_ind['rentPurPoseName'], rentPurPoseName_ind['rentPrice'])
plt.show()