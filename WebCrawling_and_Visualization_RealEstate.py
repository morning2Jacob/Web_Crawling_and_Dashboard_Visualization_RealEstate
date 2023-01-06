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
#Web Crawling
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

#台中市西屯區套房租金價格分布圖
studio = dataset[dataset['rentPurPoseName'].isin(['獨立套房', '分租套房'])]
studio_price = studio['rentPrice']
plt.figure(figsize=(12, 6)).suptitle('台中市西屯區套房租金價格分布圖', fontsize=20)
plt.hist(studio_price, bins=10, edgecolor='white')
plt.ticklabel_format(style='plain')
plt.xticks(np.arange(0, studio_price.max(), 5000))
plt.show()

#台中市西屯區各類型物件的平均價格分布圖
rentPurPoseName = dataset.groupby('rentPurPoseName')['rentPrice'].mean()
rentPurPoseName_ind = rentPurPoseName.reset_index()
plt.figure(figsize=(14, 6)).suptitle('台中市西屯區各類型物件的平均價格分布圖', fontsize=20)
plt.rcParams["font.family"]=["Microsoft JhengHei"] 
plt.bar(rentPurPoseName_ind['rentPurPoseName'], rentPurPoseName_ind['rentPrice'])
plt.show()

#Dashboard
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)

dataset = pd.read_csv('C:\\Users\\Jacob Kai\\D0790192_rent.csv')
dataset_cp = dataset.copy()

app.layout = html.Div([
    
    html.H1("Web Application Dashboards with Dash", style={'text-align' : 'center'}),
    
    dcc.Dropdown(['台中市西屯區套房租金價格分布圖', '台中市西屯區各類型物件的平均價格分布圖'],
                 '台中市西屯區套房租金價格分布圖',
                 id='slct_data'),
    html.Div(id='output_container', children=[]),
    html.Br(),
    
    dcc.Graph(id='data_plot', figure={})

])

@app.callback(
    Output('output_container', 'children'),
    Output('data_plot', 'figure'),
    Input('slct_data', 'value')
)

def update_graph(slct_option):
    
    container = "The option you've selected was {}".format(slct_option)
    
    if (slct_option == '台中市西屯區套房租金價格分布圖'):
        studio_cp = dataset_cp[dataset_cp['rentPurPoseName'].isin(['獨立套房', '分租套房'])]
        studio_price_cp = studio_cp['rentPrice']
        fig = px.histogram(studio_price_cp, x='rentPrice', nbins=10)
        
        
    if (slct_option == '台中市西屯區各類型物件的平均價格分布圖'):
        rentPurPoseName_cp = dataset_cp.groupby('rentPurPoseName')['rentPrice'].mean()
        rentPurPoseName_ind_cp = rentPurPoseName_cp.reset_index()
        fig = px.bar(rentPurPoseName_ind_cp, x='rentPurPoseName', y='rentPrice')

        
    return container, fig

        
if __name__ == '__main__':
    app.run_server(port=8030)
        
        