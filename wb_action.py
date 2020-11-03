from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import util

def initialize():
    opt = webdriver.ChromeOptions()
    opt.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
    opt.add_argument('--hide-scrollbars')           # 隐藏滚动条，应对一些特殊页面
    browser = webdriver.Chrome(chrome_options=opt)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    browser.minimize_window()
    return browser

try:
    browser = initialize()
    util.push("INITIALIZING","SUCCESS")
except:
    exit(0)

def login():
    browser.get("https://weibo.com/")
    time.sleep(5)
    while True:
        try:
            browser.find_element_by_xpath(xpath="//a[contains(text(),'登录')]").click()
            break
        except:
            util.push("正在寻找登录按钮","FAILED")
            time.sleep(1)
            continue

    time.sleep(1)

    while True:
        try:
            browser.find_element_by_xpath(xpath="(//a[contains(text(),'安全登录')])[2]").click()
            break
        except:
            util.push("正在寻找安全登录","WARNING")
            time.sleep(1)
            continue
    qr_browser = webdriver.Chrome()
    while True:
        try:
            qr_browser.get(browser.find_element_by_xpath(xpath="//div[2]/div/img").get_attribute("src"))
            break
        except:
            util.push("正在获取二维码","WARNIGN")
            time.sleep(1)
            continue

    while True:
        try:
            if browser.find_element_by_xpath(xpath="//div[2]/div/img"):
                util.push("请扫码登录","WARNING")
                time.sleep(1)
                browser.save_screenshot('./ch.png')
        except NoSuchElementException as e:
            util.push("登陆成功！","SUCCESS")
            qr_browser.close()
            browser.minimize_window()
            return True