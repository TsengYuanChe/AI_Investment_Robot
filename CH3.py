import requests
import pandas as pd
import datetime as dt # 時間套件
from dateutil.relativedelta import relativedelta
from datetime import datetime
from bs4 import BeautifulSoup
import time

# 輸入股票代號
stock_id = '2330'
# 當日時間
date = dt.date.today().strftime("%Y%m%d")
# 取得證交所網站資料
stock_data = requests.get(f'https://www.twse.com.tw/rwd/zh/ \
            afterTrading/STOCK_DAY?date={date}&stockNo={stock_id}')
json_data = stock_data.json()
df = pd.DataFrame(data=json_data['data'],
                  columns=json_data['fields'])

# 設定抓取幾個月資料
month_num=3
date_now = dt.datetime.now()

# 建立日期串列
date_list = [(date_now - relativedelta(months=i)).replace(day=1).\
             strftime('%Y%m%d') for i in range(month_num)]

date_list.reverse()
all_df = pd.DataFrame()

# 使用迴圈抓取連續月份資料
for date in date_list:
  url = f'https://www.twse.com.tw/rwd/zh/afterTrading/\
      BWIBBU?date={date}&stockNo={stock_id}'
  try:
    json_data = requests.get(url).json()
    df = pd.DataFrame(data=json_data['data'],
                  columns=json_data['fields'])
    all_df = pd.concat([all_df, df], ignore_index=True)
  except Exception as e:
    print(f"無法取得{date}的資料, 可能資料量不足.")

def yahoo_stock(stock_id):
    url = f'https://tw.stock.yahoo.com/quote/{stock_id}.TW'
    # 使用 requests 取得網頁內容
    response = requests.get(url)
    html = response.content
    # 使用 Beautiful Soup 解析 HTML 內容
    soup = BeautifulSoup(html, 'html.parser')
    # 使用 find 與 find_all 定位元素
    time_element = soup.find('section',\
                {'id': 'qsp-overview-realtime-info'}).find('time')
    table_soups = soup.find('section',\
                {'id': 'qsp-overview-realtime-info'}).find('ul')\
                                   .find_all('li')
    fields = []
    datas = []
    for table_soup in table_soups:
        table_datas = table_soup.find_all('span')
        for num,table_data in enumerate(table_datas):
            if table_data.text =='':
                continue
            if num == 0:
                fields.append(table_data.text)
            else:
                datas.append(table_data.text)
    # 建立 DataFrame
    df = pd.DataFrame([datas], columns=fields)
    # 增加日期和股號欄位
    df.insert(0,'日期',time_element['datatime'])
    df.insert(1,'股號',stock_id)
    # 回傳 DataFrame
    return df

print(yahoo_stock(stock_id))
