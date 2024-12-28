import openai
from stock_price import stock_price
from stock_news import stock_news
from stock_value import stock_fundamental
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

stock_list = pd.read_csv('stock_list.csv')
stock_list.set_index('代號', inplace=True)
data = stock_list.to_dict(orient='index')

def get_reply(messages):
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        reply = response["choices"][0]["message"]["content"]
    except openai.OpenAIError as e:
        reply = f"發生錯誤: {str(e)}"
    return reply

def generate_content_msg(stock_id):
    try:
        stock_id = int(stock_id)  # 確保轉為數字類型
    except ValueError:
        return f"無效的股票代號：{stock_id}"

    if stock_id == "大盤":
        stock_name = "大盤"
    elif stock_id in data:
        stock_name = data[stock_id]["股票名稱"]
    else:
        return f"找不到股號 {stock_id} 的資訊。"
    
    price_data = stock_price(stock_id)
    news_data = stock_news(stock_name)[:3]
    
    content_msg = '你現在是一位專業的證券分析師, \
        你會依據以下資料來進行分析並給出一份完整的分析報告:\n'
        
    content_msg += f'近期價格資訊:\n {price_data}\n'
    
    if stock_id != "大盤":
        stock_value_data = stock_fundamental(stock_id)
        content_msg += f'每季營收資訊：\n {stock_value_data}\n'
        
    content_msg += f'近期新聞資訊: \n {news_data}\n'
    content_msg += f'請給我{stock_name}近期的趨勢報告,請以詳細、\
        嚴謹及專業的角度撰寫此報告,並提及重要的數字, reply in 繁體中文'

    return content_msg

def stock_gpt(stock_id):
    content_msg = generate_content_msg(stock_id)
    
    msg = [{
        "role": "system",
        "content": "你現在是一位專業的證券分析師, 你會統整近期的股價\
        、基本面、新聞資訊等方面並進行分析, 然後生成一份專業的趨勢分析報告"
    }, {
        "role": "user",
        "content": content_msg
    }]
    
    total_tokens = sum(len(m["content"]) for m in msg)
    if total_tokens > 16000:  # 給些許餘量
        return "輸入資料過多，請減少查詢範圍或數據量。"

    reply_data = get_reply(msg)

    return reply_data

stock_id = "2330"
print(f"Testing stock_id: {stock_id}")

content_msg = generate_content_msg(stock_id)
print(f"Content message: {content_msg}")

if "找不到" not in content_msg:
    reply = stock_gpt(stock_id)
    print(f"Final reply: {reply}")
else:
    print(content_msg)