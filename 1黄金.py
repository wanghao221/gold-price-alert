from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re
import datetime
import ctypes  # ✅ 用于弹窗提醒

# === 用户输入 ===
x = float(input("请输入买入时金价（元/克）: "))
y = float(input("请输入买入金额（元）: "))
# 固定手续费率
fee_rate = 0.004  # 固定手续费率

# 计算买入克数
buy_weight = y / x
print(f"买入克数: {buy_weight:.4f} 克")

# 设置无头浏览器
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 目标页面
url = 'https://m.jr.jd.com/finance-gold/msjgold/homepage?from=fhc&ip=66.249.71.78&orderSource=6&ptag=16337378.0.1'

# 弹窗函数
def popup(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)

try:
    while True:
        driver.get(url)
        time.sleep(3)  # 等待JS渲染

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 提取实时金价
        all_titles = soup.find_all('span', class_='gold-price-persent-title')
        gold_price = None
        for title in all_titles:
            if '实时金价' in title.get_text():
                match = re.search(r'(\d+\.\d+)', title.get_text())
                if match:
                    gold_price = float(match.group(1))
                    break

        if gold_price:
            # 盈亏计算 ✅ 不算手续费
            current_value = gold_price * buy_weight
            profit = current_value - y

            # 当前时间
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"{now} 实时金价: {gold_price} 元/克，当前盈亏: {profit:.2f} 元")

            # 提醒逻辑（弹窗+打印）
            if profit >= 40:
                msg = f"{now}\n📈 恭喜！可以卖了，赚了40元以上！\n当前盈亏: {profit:.2f} 元"
                print(msg)
                popup("卖出提醒", msg)
            elif profit <= -30:
                msg = f"{now}\n📉 注意！已经亏了30元以上！\n当前盈亏: {profit:.2f} 元"
                print(msg)
                popup("亏损提醒", msg)

        else:
            print("未找到实时金价")

        # 每30秒检测一次
        time.sleep(30)

except KeyboardInterrupt:
    print("已停止监控")

finally:
    driver.quit()
