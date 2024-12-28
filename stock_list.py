import pandas as pd
import requests
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
html_data = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",headers=headers)
x = pd.read_html(html_data.text)
x=x[0]
x.columns = x.iloc[0,:]
x = x.iloc[1:,:]
x['代號'] = x['有價證券代號及名稱'].apply(lambda x: x.split()[0])
x['股票名稱'] = x['有價證券代號及名稱'].apply(lambda x: x.split()[-1])
x['上市日'] = pd.to_datetime(x['上市日'], errors='coerce')
x = x.dropna(subset=['上市日'])
x = x.drop(['有價證券代號及名稱','國際證券辨識號碼(ISIN Code)','CFICode','備註'], axis=1)
x = x[['代號','股票名稱','上市日','市場別','產業別']]
x = x.dropna(subset=['產業別'])
x = x[x["代號"].str.isdigit()]
print(x)
x.to_csv('stock_list.csv')