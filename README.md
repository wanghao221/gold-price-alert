在日常投资中，很多朋友喜欢在京东金融买点黄金，低买高卖赚点小差价。但黄金价格实时波动频繁，总是盯着手机太累了，于是我用Python写了一个**实时金价监控+自动提醒脚本**，可以帮我在金价波动达到盈亏阈值时**自动弹窗提醒**，告别手动盯盘！


## 🌟 工具能干啥？

简单来说就是：
- 自动盯着京东黄金价格👀
- 赚了40块会开心提醒我"可以卖啦！"🎉
- 亏了60块会哭唧唧提醒我"注意止损！"😭
- 每30秒偷偷看一眼价格，完全不用我操心⏰

## 🛠️ 手把手教你用

### 1️⃣ 先装好这些"食材"
```bash
pip install selenium webdriver-manager beautifulsoup4
```

### 2️⃣ 代码实现讲解


代码分为几个关键模块，下面我们逐段解析。

### 📌1. 用户输入参数

```python
x = float(input("请输入买入时金价（元/克）: "))
y = float(input("请输入买入金额（元）: "))
buy_weight = y / x
print(f"买入克数: {buy_weight:.4f} 克")
```

用户只需输入两项：**买入时金价**和**买入金额**，程序会自动帮你算出买入的黄金克数（忽略手续费）。

---

### 📌2. 设置无头浏览器（Selenium）

```python
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无界面运行
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
```

我们使用 `Selenium + webdriver-manager` 来实现网页访问，并设置浏览器为“无头模式”，即后台运行，不弹出浏览器窗口，运行更轻便。

---

### 📌3. 抓取实时金价（BeautifulSoup + 正则）

```python
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
all_titles = soup.find_all('span', class_='gold-price-persent-title')
...
```

通过 `BeautifulSoup` 来解析页面HTML内容，找到金价字段并用正则提取数字，兼容京东移动端页面结构（这个页面PC访问可能为空白，但移动端HTML源码中是有数据的）。

---

### 📌4. 盈亏计算与提醒逻辑

```python
current_value = gold_price * buy_weight
profit = current_value - y
...
if profit >= 40:
    popup("卖出提醒", msg)
elif profit <= -60:
    popup("亏损提醒", msg)
```

这里是盈利逻辑的核心部分，实时计算你当前账户中黄金价值与初始投资的差额，并在盈亏超过指定值时通过弹窗提醒。

📢 弹窗是通过 `ctypes.windll.user32.MessageBoxW` 实现的，兼容 Windows 系统，效果如下：



![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a494a470335f46cb89354d294fa27ef8.png)


---

### 📌5. 自动循环 + 中断退出

```python
while True:
    ...
    time.sleep(30)
```

脚本默认每30秒刷新一次网页获取新金价，并自动循环运行。如果你按下 `Ctrl + C`，脚本会优雅退出并关闭浏览器。

---

## 🔧完整代码

代码开源如下，可直接复制运行：

👉 [点击查看完整代码](https://github.com/wanghao221/gold-price-alert/)


---

## 🎯项目实测效果

实际运行过程中，当我输入：

```
请输入买入时金价（元/克）: 780.52
请输入买入金额（元）: 10000
```

程序每半分钟自动更新一次金价，并在达到设定盈亏条件时自动弹出提醒框，及时提示买卖时机，非常实用！

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8657cecaf66a4e9c944c9a16c3649d20.png)

---

## 💡可以拓展的功能

这个项目只是一个基础框架，你可以根据自己的需求继续拓展：

* 💹 自动绘制金价走势图📈；
* 📧 集成邮件或微信推送，可以把`popup`换成微信机器人通知；
* ⏱ 设置运行时间区间（如早9点到晚8点）；
* 🤖 接入AI判断买卖信号
* 🌟可以同时监控支付宝、银行APP的价格……
