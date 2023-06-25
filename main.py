from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
import requests
import json
# 创建 Chrome 浏览器实例
CORP_ID = "wwc307dfc2cab1e8ed"

SECRET = "q_ml2ucAQg_GG0PCE4T-eSPhkqKI-cU5tAZEQw7sHrg"
driver = webdriver.Chrome()
shoes="lv trainer 黑牛仔 4码"
# 访问网页
driver.get("https://it.louisvuitton.com/ita-it/prodotti/sneaker-lv-trainer-nvprod3150035v/1A9JGS")
# p_input = driver.find_element(By.ID, 'key')
# p_input.send_keys('python编程')  # 找到输入框输入
time.sleep(1)
# 点击搜素按钮
sale_on=driver.find_element(By.CLASS_NAME,"ucm-popin-close-text").click()
# time.sleep(1)
all_book_info = []
head=['书名', '价格']
#csv文件的路径和名字
path='./file/book.csv'
def write_csv(head,all_book_info,path):
    with open(path, 'w', newline='',encoding='utf-8') as file:
        fileWriter = csv.writer(file)
        fileWriter.writerow(head)
        fileWriter.writerows(all_book_info)
# 爬取一页
def get_onePage_info():
    # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
    res=[]
    # 书籍列表
    sale = driver.find_element(By.CLASS_NAME, "lv-product-purchase__button").text
    if sale == "Prodotto non disponibile":
        res="无货"
        print(res)
    elif sale == "Aggiungi alla shopping bag":
        res="有货"
        print(res)
    return res
    # all_book_info.append(res)
class WeChatPub:
    s = requests.session()
    token = None

    def __init__(self):
        self.token = self.get_token(CORP_ID, SECRET)
        print("token is " + self.token)

    def get_token(self, CORP_ID, SECRET):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(CORP_ID, SECRET)
        rep = self.s.get(url)
        if rep.status_code == 200:
            return json.loads(rep.content)['access_token']
        else:
            print("request failed.")
            return None

    def send_msg(self, content,res):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        url = f"https://sctapi.ftqq.com/SCT214361T7tWl9uKZfNvPkiCy2SUi19so.send?title={shoes} is {res}"
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "@all",  # 接收人
            "msgtype": "text",
            "agentid": 1000002,  # 应用ID
            "text": {
                'content':"hello world"
            },
            "safe": 0
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code == 200:
            return json.loads(rep.content)
        else:
            print("request failed.")

res = get_onePage_info()
# driver.find_element(By.CLASS_NAME, 'pn-next').click()  # 点击下一页
time.sleep(2)
# write_csv(head, all_book_info, path)
driver.close()

wechat = WeChatPub()

now  = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

res=wechat.send_msg(f"<div class=\"gray\">{now}</div> <div class=\"normal\">注意！</div><div class=\"highlight\">今日有新债，坚持打新！</div>",res)

print(res)
print( '消息已发送！')