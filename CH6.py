from openai import OpenAI, OpenAIError # 串接 OpenAI API
import yfinance as yf
import pandas as pd # 資料處理套件
import numpy as np
import datetime as dt # 時間套件
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import openai
from replit import db

load_dotenv()  # 讀取 .env 檔案
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)






def get_stock_name(stock_id, name_df):
    return name_df.set_index('股號').loc[stock_id, '股名']

