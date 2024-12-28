from openai import OpenAI, OpenAIError
from googlesearch import search
api_key = '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'
client = OpenAI(api_key = api_key) # 建立 OpenAI 物件

def get_reply(messages):
    try:
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        reply = response.choices[0].message.content
    except OpenAIError as err:
        reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
    return reply

hist = []       # 歷史對話紀錄
backtrace = 2   # 記錄幾組對話

def chat(sys_msg, user_msg):
    hist.append({"role":"user", "content":user_msg})
    reply = get_reply(hist
                      + [{"role":"system", "content":sys_msg}])
    while len(hist) >= 2 * backtrace: # 超過記錄限制
        hist.pop(0)                   # 移除最舊紀錄
    hist.append({"role":"assistant", "content":reply})
    return reply

hist = []       # 歷史對話紀錄
backtrace = 2   # 記錄幾組對話

def chat_w(sys_msg, user_msg, search_g = True):
    web_res = []
    if search_g == True: # 代表要搜尋網路
        content = "以下為已發生的事實：\n"
        for res in search(user_msg, advanced=True,
                          num_results=3, lang='zh-TW'):
            content += f"標題：{res.title}\n" \
                       f"摘要：{res.description}\n\n"
        content += "請依照上述事實回答問題 \n"
        web_res = [{"role": "user", "content": content}]
    web_res.append({"role": "user", "content": user_msg})
    while len(hist) >= 2 * backtrace: # 超過記錄限制
        hist.pop(0)  # 移除最舊的紀錄
    reply_full = ""
    for reply in get_reply(
        hist                          # 先提供歷史紀錄
        + web_res                     # 再提供搜尋結果及目前訊息
        + [{"role": "system", "content": sys_msg}]):
        reply_full += reply           # 記錄到目前為止收到的訊息
        yield reply                   # 傳回本次收到的片段訊息
    hist.append({"role": "user", "content": user_msg})
    while len(hist) >= 2 * backtrace: # 超過記錄限制
        hist.pop(0)                   # 移除最舊紀錄
    hist.append({"role":"assistant", "content":reply_full})
    
sys_msg = '小助理'

while True:
    msg = input("你說：")
    if not msg.strip(): break
    print(f"{sys_msg}：", end = "")
    for reply in chat_w(sys_msg, msg, search_g = True):
        print(reply, end = "")
    print('\n')
hist = []

