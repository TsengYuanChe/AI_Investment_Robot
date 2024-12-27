from openai import OpenAI, OpenAIError # OpenAI 官方套件
import getpass # 保密輸入套件
api_key = getpass.getpass("請輸入金鑰：")
client = OpenAI(api_key = api_key) # 建立 OpenAI 物件