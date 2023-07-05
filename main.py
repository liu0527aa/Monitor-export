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


"""-------反爬设置------"""
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
})


# 访问网页
driver.get("https://www.louisvuitton.cn/zhs-cn/homepage")
time.sleep(1)
# 点击搜素按钮
driver.find_element(By.CLASS_NAME, "ucm-button.ucm-button--default.ucm-choice__yes").click()
driver.find_element(By.CLASS_NAME, "lv-button").click() # 点击搜索按钮
element = driver.find_element_by_id('searchHeaderInput')
element.send_keys("LV TRAINER")  # 输入搜索内容
element.send_keys(Keys.ENTER)   # 回车
time.sleep(2)
driver.find_element_by_id('product-1ABLY1').click()  # 点击商品进去详情页
time.sleep(2)
# good_id = driver.find_element(By.CLASS_NAME, "lv-product__sku").text
# good_name = driver.find_element(By.CLASS_NAME, "lv-product__name").text
# good_price = driver.find_element(By.CLASS_NAME, "notranslate").text
# good_style = driver.find_elements(By.CLASS_NAME, "lv-product-variation-selector__value")
# # good_size = driver.find_element(By.CLASS_NAME, "lv-product-variation-selector__value").text
# print(good_id)
# print(good_name)
# print(good_price)
# print(good_style[0].text)
# print(good_style[1].text)

# time.sleep(1)

# 鞋子款式list
shoes = []

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
    time.sleep(1)
    # 进入款式列表
    driver.find_elements(By.CLASS_NAME, "lv-product-variation-selector__value")[0].click()
    time.sleep(1)
    # 获取款式list
    items = driver.find_elements(By.CLASS_NAME, "lv-choice-group__item.lv-product-panel-grid__list-item")
    length = items.__len__()
    # 多款鞋尺码及库存
    MulSize_stocks = [[] for i in range(length)]
    for i in range(length):
        # 依次点击不同款式
        driver.find_elements(By.CLASS_NAME, "lv-choice-group__item.lv-product-panel-grid__list-item")[i].click()
        time.sleep(1)
        # 获取商品信息
        name = driver.find_element(By.CLASS_NAME, "lv-product__name").text
        color = driver.find_elements(By.CLASS_NAME, "lv-product-variation-selector__value")[0].text
        shoes.append(f"{name}--{color}")
        one_stocks = get_sizeStock_info()
        MulSize_stocks[i].append(one_stocks)
        if i == items.__len__()-1:
            break
        driver.find_elements(By.CLASS_NAME, "lv-product-variation-selector__value")[0].click()
        time.sleep(1)

    return MulSize_stocks


def get_sizeStock_info():
    # 进入尺码列表查看库存
    time.sleep(1)
    driver.find_elements(By.CLASS_NAME, "lv-product-variation-selector__value")[1].click()
    time.sleep(1)
    sizes = driver.find_elements(By.CLASS_NAME, "lv-product-panel-list__item-name")
    stocks = driver.find_elements(By.CLASS_NAME, "lv-product-panel-list__item-status")
    size_stocks = []
    for i in range(sizes.__len__()):
        if stocks[i].text == "":
            size_stocks.append(f"{sizes[i].text}--可选购")
        else:
            size_stocks.append(f"{sizes[i].text}--{stocks[i].text}")
    time.sleep(1)
    # 关闭尺码表
    driver.find_element(By.CLASS_NAME, "lv-modal__close.lv-icon-button.-light").click()
    time.sleep(1)
    return size_stocks


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

    def send_msg(self, content, res):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        url = f"https://sctapi.ftqq.com/SCT214982TPYjiDoACeUsOEsCeOpvpUWbR.send?title={shoes[0]} is {res[0]}"
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