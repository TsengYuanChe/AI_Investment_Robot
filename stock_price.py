import yfinance as yf
import datetime as dt

def stock_price(stock_id="大盤", days = 5):
    if stock_id == "大盤":
        stock_id="^TWII"
    else:
        stock_id = str(stock_id) + ".TW"

    end = dt.date.today() # 資料結束時間
    start = end - dt.timedelta(days=days) # 資料開始時間
    # 下載資料
    df = yf.download(stock_id, start=start, end=end, auto_adjust=False)

    # 更換列名
    df.columns = ['調整後收盤價', '收盤價', '最高價', '最低價', '開盤價', '成交量']

    data = {
        '日期': df.index.strftime('%Y-%m-%d').tolist(),
        '收盤價': df['收盤價'].tolist(),
        '每日報酬': df['收盤價'].pct_change().tolist(),
        '漲跌價差': df['調整後收盤價'].diff().tolist()
    }

    return data
