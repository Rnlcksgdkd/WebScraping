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

