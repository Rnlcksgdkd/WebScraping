## Naver 에서 주식가격/환율 정보를 스크래핑 해오는 코드입니다

> BeautifulSoup 를 이용한 스크래핑 코드



### 1. 현재 환율 구하기

```python
# 현재 환율을 구해서 출력합니다
def get_now_exchange():
    
    html = urlopen("https://finance.naver.com/marketindex/exchangeList.nhn")
    bsObject = BeautifulSoup(html, "html.parser")

    exchange_data = []
    bs = bsObject.select('div.tbl_area tbody tr')
    for i,temp in enumerate(bs):
        if i < 2: continue
        country = temp.select("a")[0].get_text().strip()
        exchange = temp.select("td")[1].get_text()
        exchange_data.append([country , exchange]) 
    
    for e in exchange_data:
        print(e)
    return
```

---



### 2.  각 나라의 지난 환율가격들을 보여주는 링크 구하기

```python
# 각 나라마다 환율 정보가 담긴 홈페이지 링크를 주기 , 저장
def get_country_exchange_link():
    hompage_link = "https://finance.naver.com/"
    base_link = "https://finance.naver.com/marketindex/exchangeList.nhn"
    html = urlopen(base_link)
    bsObject = BeautifulSoup(html, "html.parser")
    cover = bsObject.select("td.tit>a")

    country_index = []
    exchanges_daily_link = []
    
    for i,cover2 in enumerate(cover):
        country =  cover2.get("href")[-6:-1]
        country_link = hompage_link + cover2.get("href")
        country_html = urlopen(country_link)
        country_bs = BeautifulSoup(country_html, "html.parser")
        country_daily_link = hompage_link + country_bs.select("iframe[title=일별시세]")[0].get("src")
        
        country_index.append(country)
        exchanges_daily_link.append(country_daily_link)
    
    df = pd.DataFrame([exchanges_daily_link] , columns=country_index)
    df.to_excel("countries daily exchange link.xlsx" , index=False)
    print("complete saving link")
```

---



### 3. 전체 환율 정보 스크래핑 함수

> 1). 환율정보 링크가 제대로 걸려있는지 확인

```python
# 전체 나라들에 대해서 환율 스크래핑 
def get_exchange():
    
    df = pd.read_excel("countries daily exchange link.xlsx" , engine="openpyxl")
    date_index = []
    exchanges = []
    for link in df.loc[0]:
        # 각 나라의 환율정보가 들어가 있는 홈페이지 링크 출력
        print(link)
```



>2).  BeautifulSoup 를 이용해서 환율 정보 파싱

```
# 전체 나라들에 대해서 환율 스크래핑 
def get_exchange():
    
    df = pd.read_excel("countries daily exchange link.xlsx" , engine="openpyxl")
    date_index = []
    exchanges = []
    for link in df.loc[0]:
        # 각 나라의 환율정보가 들어가 있는 홈페이지 링크 출력
        
        html = urlopen(link)
        bs = BeautifulSoup(html, "html.parser")
        bs_select = bs.select("table.tbl_exchange.today tbody tr")
        
        for bs_sub in bs_select:
            bs_sub2 = bs_sub.select("td")
            date = bs_sub2[0].get_text()
            exchange = bs_sub2[1].get_text()
            print(date , exchange)
            print("----------")
            
        break
```





## 주식 가격 스크래핑 해오기

```python
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
            prices.append(p.text)
            
df = pd.DataFrame({"price (종가)" : prices})
df.index = date
df
```



1. ![Screenshot_12](C:\Users\Ando\Documents\Screenshot_12.png)



```python
import matplotlib.pyplot as plt
plt.plot(df["price (종가)"].values)
df["price (종가)"]
```

![Screenshot_11](C:\Users\Ando\Documents\Screenshot_11.png)



```python
plt.plot(df["price (종가)"].values[0:10])
```



![Screenshot_13](C:\Users\Ando\Documents\Screenshot_13.png)

```
    for i,p in enumerate(price_sel):
        if i% 6 == 0:
            prices.append(int(p.text.replace(",","")))
```



![Screenshot_14](C:\Users\Ando\Documents\Screenshot_14.png)



```
from matplotlib import font_manager , rc
import platform

# matplot 에서 한글 폰트 사용
if platform.system() == "Windows":
    path =  "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font' , family =  font_name)

# 좀 더 그럴듯하게 그려보기
plt.figure(figsize=(12,4))
plt.plot(df.index , df["price (종가)"])
plt.title("주식 가격 그래프")
plt.xlabel("기준 년월")
plt.ylabel("주식 가격 (종가 기준)")

plt.show()
```

![Screenshot_16](C:\Users\Ando\Documents\Screenshot_16.png)

```python
xticks = []
for i in range(len(df)):
    num_divide = 10
    if i%10 == 0:
        xticks.append(df.index[i])
xticks.append(df.index[-1])

plt.xticks(xticks)
```

![Screenshot_17](C:\Users\Ando\Documents\Screenshot_17.png)

```
def get_stock_prices(code_number):

    driver = webdriver.Chrome("./chromedriver.exe")
    url = "https://finance.naver.com/item/main.nhn?code=" + code_number
    driver.get(url)
    if driver.find_elements_by_css_selector("div.error_content"):
        print("잘못된 코드번호 입니다")
        return
    
    stock_name = driver.find_element_by_css_selector("div.wrap_company a").text
    print("코드 종목 : {} / 코드 번호 : {}".format(stock_name , code_number))
```



```python
## 코드넘버 > 스크래핑 > df > xlsx 저장
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
    prices = []
    date = []
    for page in range(1,11):
        url = "https://finance.naver.com/item/sise_day.nhn?code=" + code_number + "&page=" + str(page)
        driver.get(url)
        date_sel = driver.find_elements_by_css_selector("span.tah.p10.gray03")
        price_sel= driver.find_elements_by_css_selector("span.tah.p11")
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
```



```

```

