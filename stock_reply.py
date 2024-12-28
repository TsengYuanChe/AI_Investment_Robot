import openai
from stock_price import stock_price
from stock_news import stock_news
from stock_value import stock_fundamental
import pandas as pd

stock_list = pd.read_csv('stock_list.csv')
stock_list.set_index('代號', inplace=True)
data = stock_list.to_dict(orient='index')

def get_reply(messages):
    try:
        response = openai.ChatCompletion.creat(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        reply = response["choices"][0]["message"]["content"]
    except openai.OpenAIError as erro:
        reply = f"發生 {erro.error.type} 錯誤\n {erro.error.message}"
    return reply

def generate_content_msg(stock_id):
    if stock_id == "大盤":
        stock_name = "大盤"
    elif stock_id in data:
        stock_name = data[stock_id]["股名"]
    else:
        return f"找不到股號 {stock_id} 的資訊。"
    
    price_data = stock_price(stock_id)
    news_data = stock_news(stock_name)
    
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

    reply_data = get_reply(msg)

    return reply_data