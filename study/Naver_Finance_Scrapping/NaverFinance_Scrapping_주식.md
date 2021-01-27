# 네이버 파이낸스 스크래핑 하기 - 주식가격

> 주식에 대해 관심을 갖고 공부하기 시작하기도 했고 직구를 많이 하는 편이라 환율 정보도 스크래핑을 하면 도움이 되겠다 싶어서 스크래핑을 해보게 되었다 , 이번 편에는 주식을, 다음 편에는 환율을 스크래핑해서 xlsx 파일형태로 저장하기



##  0. Import

```python
from selenium import webdriver
import time
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
```



## 1.  스크래핑할 URL 불러오기

```
삼성전자 (코드번호 005930) 을 기준으로 샘플 스크래핑 
```



```python
# 삼성전자 관련 메인 페이지 url
html = urlopen('https://finance.naver.com/item/main.nhn?code=005930')
bsObject = BeautifulSoup(html, "html.parser")
bs = bsObject.select("dl.blind dd")
print(bs)
```



```python
# 원하는 데이터들을 `meta_data` 변수에 저장

meta_data = []
for cover in bs:
    print(cover)
    data = []
    for cover2 in cover.find_all('dd'):
        data.append(cover2.get_text())
        print("//")
        print(cover2)
    meta_data.append(data)
print(meta_data)
```





```python
# Selenium 동적제어로 페이지 넘기기
driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://finance.naver.com/item/sise_day.nhn?code=035720")
driver.page_source
a = driver.find_elements_by_css_selector("span.tah.p10.gray03")
b = driver.find_elements_by_css_selector("span.tah.p11")
```



```python

## 10페이지에 대해서 스크래핑 테스트 / matplotlib 을 이용한 그래프 출력

driver = webdriver.Chrome("./chromedriver.exe")

prices = []
date = []

for page in range(1,11):
    url = "https://finance.naver.com/item/sise_day.nhn?code=035720" + "&page=" + str(page)
    driver.get(url)
    date_sel = driver.find_elements_by_css_selector("span.tah.p10.gray03")
    price_sel= driver.find_elements_by_css_selector("span.tah.p11")
    for d in date_sel:
        date.append(d.text)

    for i,p in enumerate(price_sel):
        if i% 6 == 0:
            prices.append(int(p.text.replace(",","")))
            
df = pd.DataFrame({"price (종가)" : prices})
df.index = date
plt.plot(df["price (종가)"].values)
```



```python
import matplotlib.pyplot as plt
plt.plot(df["price (종가)"].values)
df["price (종가)"]
```



```python

plt.plot(df["price (종가)"].values[0:10])
```



```python
from matplotlib import font_manager , rc
import platform

# matplot 에서 한글 폰트 사용
if platform.system() == "Windows":
    path =  "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font' , family =  font_name)

xticks = []
for i in range(len(df)):
    num_divide = 10
    if i%10 == 0:
        xticks.append(df.index[i])
plt.xticks(xticks)

# 좀 더 그럴듯하게 그려보기
plt.figure(figsize=(12,4))
plt.plot(df.index , df["price (종가)"])
plt.title("주식 가격 그래프")
plt.xlabel("기준 년월")
plt.ylabel("주식 가격 (종가 기준)")

plt.show()
```



```python
code_number = "005930"
driver = webdriver.Chrome("./chromedriver.exe")
url = "https://finance.naver.com/item/sise_day.nhn?code=035720&page=1000"
driver.get(url)

page = 500
prices = []
date = []

pv_date = ""
while(1):
    page += 1
    url = "https://finance.naver.com/item/sise_day.nhn?code=" + code_number + "&page=" + str(page)
    driver.get(url)
    date_sel = driver.find_elements_by_css_selector("span.tah.p10.gray03")
    price_sel= driver.find_elements_by_css_selector("span.tah.p11")
    
    now_date = date_sel[0].text
    if pv_date == now_date: break
    else:
        pv_date = now_date
    for d in date_sel:
        date.append(d.text)

    for i,p in enumerate(price_sel):
        if i% 6 == 0:
            prices.append(int(p.text.replace(",","")))
            

df = pd.DataFrame({"price(종가)" : prices})
df.index = date

df

```





```python


def get_stock_prices(code_number):

    driver = webdriver.Chrome("./chromedriver.exe")
    url = "https://finance.naver.com/item/main.nhn?code=" + code_number
    driver.get(url)
    if driver.find_elements_by_css_selector("div.error_content"):
        print("잘못된 코드번호 입니다")
        return
    
    stock_name = driver.find_element_by_css_selector("div.wrap_company a").text
    print("코드 종목 : {} / 코드 번호 : {}".format(stock_name , code_number))
    
    
    # 스크래핑
    page = 0
    prices = []
    date = []
    pv_date = ""
    while(1):
        page += 1
        url = "https://finance.naver.com/item/sise_day.nhn?code=" + code_number + "&page=" + str(page)
        driver.get(url)
        date_sel = driver.find_elements_by_css_selector("span.tah.p10.gray03")
        price_sel= driver.find_elements_by_css_selector("span.tah.p11")

        now_date = date_sel[0].text
        if pv_date == now_date: break
        else:
            pv_date = now_date
        for d in date_sel:
            date.append(d.text)

        for i,p in enumerate(price_sel):
            if i% 6 == 0:
                prices.append(int(p.text.replace(",","")))
    prices.reverse()
    df = pd.DataFrame({"price(종가)" : prices})
    df.index = date
    save_name = stock_name + " stock price.xlsx"
    df.to_excel(save_name , engine="openpyxl")
    print("Succesful Saving")            
    return


get_stock_prices("035720")      

```







> 오늘 작업한 최종 코드

```python
# Import
from selenium import webdriver
import time
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# 파일 경로를 입력받아 그래프 출력/저장
def draw_graph(savefile = ""):
    
    # 로드
    df = pd.read_xlsx(savefile)
    # matplot 에서 한글 폰트 사용
    if platform.system() == "Windows":
        path =  "c:/Windows/Fonts/malgun.ttf"
        font_name = font_manager.FontProperties(fname=path).get_name()
        rc('font' , family =  font_name)
    xticks = []
    for i in range(len(df)):
        num_divide = 10
        if i%10 == 0:
            xticks.append(df.index[i])
    plt.xticks(xticks)
    # 좀 더 그럴듯하게 그려보기
    plt.figure(figsize=(12,4))
    plt.plot(df.index , df["price (종가)"])
    plt.title("주식 가격 그래프")
    plt.xlabel("기준 년월")
    plt.ylabel("주식 가격 (종가 기준)")
    plt.show()
    plt.savefile(".png")

# 코드번호를 입력받아 모든 주식가격 (일일 기준) 을 스크래핑해서 xlsx 파일로 저장 후 리턴
def get_stock_prices(code_number):

    driver = webdriver.Chrome("./chromedriver.exe")
    url = "https://finance.naver.com/item/main.nhn?code=" + code_number
    driver.get(url)
    if driver.find_elements_by_css_selector("div.error_content"):
        print("잘못된 코드번호 입니다")
        return
    stock_name = driver.find_element_by_css_selector("div.wrap_company a").text
    print("코드 종목 : {} / 코드 번호 : {}".format(stock_name , code_number))
    
    # 스크래핑
    page = 0
    prices = []
    date = []
    pv_date = ""
    while(1):
        page += 1
        url = "https://finance.naver.com/item/sise_day.nhn?code=" + code_number + "&page=" + str(page)
        driver.get(url)
        date_sel = driver.find_elements_by_css_selector("span.tah.p10.gray03")
        price_sel= driver.find_elements_by_css_selector("span.tah.p11")
        now_date = date_sel[0].text
        if pv_date == now_date: break
        else:
            pv_date = now_date
        for d in date_sel:
            date.append(d.text)
        for i,p in enumerate(price_sel):
            if i% 6 == 0:
                prices.append(int(p.text.replace(",","")))
    prices.reverse()
    df = pd.DataFrame({"price(종가)" : prices})
    df.index = date
    save_name = stock_name + " stock price.xlsx"
    df.to_excel(save_name , engine="openpyxl")
    print("Succesful Saving")            
    return save_name

```



> 메인 실행문

``` python
xlsx_path = get_stock_prices("005930")	# 삼성전자 (005930)
draw_graph(xlsx_path)
```

