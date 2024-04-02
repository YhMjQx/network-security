from selenium import webdriver
import time,uiautomation
from selenium.webdriver.common.by import By
# 如果要操作windows元素，使用 uiautomation 库；如果要处理移动端，使用Appium

def autologwoniusales():
    # 第一步，实例化webdriver对象，用于初始化浏览器操作,但是如下的简单操作会让浏览器打开很快就关闭了
    # driver = webdriver.Chrome()
    # driver = webdriver.Edge()
    # driver = webdriver.Firefox()

    # 于是使用如下代码可以使得浏览器作为后台进程运行不关闭
    # 不自动关闭浏览器
    # 使用Chrom浏览器
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    # 使用 edge 浏览器
    # options = webdriver.EdgeOptions()
    # options.add_experimental_option('detach',True)
    # driver = webdriver.Edge(options=options)

    # 使用 firefox 浏览器
    # options = webdriver.FirefoxOptions
    # driver = webdriver.Firefox()

    # 第二步：访问目标服务器网站
    driver.get('http://192.168.230.147:8080/woniusales/')
    driver.maximize_window()
    print(driver.title)
    print(driver.page_source)
    # chrome_driver.refresh()
    # chrome_driver.back()
    # chrome_driver.forward()
    time.sleep(1)

    # 第三步，利用DOM的识别机制，去识别和操作页面元素
    driver.find_element(by=By.ID, value='username').send_keys('admin')
    time.sleep(1)
    # CSS样式可以直接在浏览器的F12下复制
    driver.find_element(by=By.CSS_SELECTOR, value='#password').send_keys('admin123')
    time.sleep(1)
    # 元素的XPath可以直接在浏览器的F12下复制
    driver.find_element(by=By.XPATH, value='//input[@id="verifycode"]').send_keys('0000')
    time.sleep(1)
    driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/form/div[6]/button').click()

    # 如果可以扫描商品条码，则说明登录成功
    try:
        time.sleep(1)
        driver.find_element(by=By.ID, value='barcode').send_keys('1234567890')
        print('登录成功')
    except:
        print('登录失败')

    if ' 查询会员信息' in driver.page_source:
        print('登录成功')
    else:
        print('登录失败')

    time.sleep(1)
    driver.close()

# 使用uiautomation库识别windows元素
def autowincalc():
    calc = uiautomation.WindowControl(name='计算器')  # 会自动执行windows内置的运行窗口的程序
    calc.WindowControl(AutomationId='num5Button').Click()
    calc.WindowControl(Name='二').Click()
    calc.WindowControl(AutomationId='plusButton').Click()
    calc.WindowControl(AutomationId='num0Button').Click()
    calc.WindowControl(AutomationId='equalButton').Click()

if __name__ == '__main__':
    # autowincalc()   # 这里有点问题
    autologwoniusales()