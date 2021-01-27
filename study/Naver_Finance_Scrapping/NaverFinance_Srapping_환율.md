# 네이버 파이낸스 스크래핑 하기 - 환율

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





> NaverFinance 에 환율이 등록된 나라들 정보

``` python

hompage_link = "https://finance.naver.com/"
base_link = "https://finance.naver.com/marketindex/exchangeList.nhn"
html = urlopen(base_link)
bsObject = BeautifulSoup(html, "html.parser")
cover = bsObject.select("td.tit>a")

country_index = []
exchanges_daily_link = []

for i,cover2 in enumerate(cover):
    country_index.append(cover2.get("href")[-6:])
print(country_index)
    
base_link = "https://finance.naver.com//marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_"  
link_lst = []
for country_link in country_index:
    link = base_link + country_link
    link_lst.append(link)
    
country_index
```



> 환율 스크래핑 (모든국가를  다 하는)

```python
import time
start = time.time()
from tqdm.notebook import tqdm

country_index
link_lst

# 한 국가에 대해서 테스트 중인데 상당히 오래걸린다 , 아마 Selenium을 써야할 듯하다

df = pd.DataFrame( [] , columns=country_index)

# 전체 국가에 대해서
date_index = []
for i,link in tqdm(enumerate(link_lst)):
    country_exchange = []
    
    page = 1
    maxpage = 2
    
    if i > 8:
        break
        
    # 한 나라에 대해서
    while(True):
        html = urlopen(link + "&page=" + str(page))
        bs = BeautifulSoup(html, "html.parser")
        bs_select =bs.select("table.tbl_exchange.today tbody tr")
        if not len(bs_select): break

        # 페이지 스크래핑 
        for bs_sub in bs_select:
            bs_sub2 = bs_sub.select("td")
            date = bs_sub2[0].get_text()
            exchange = float(bs_sub2[1].get_text().replace("," , ""))
            if len(date_index) <= len(country_exchange):
                date_index.append(date)
            country_exchange.append(exchange)
        page += 1
  
    if len(df[country_index[0]]) == 0:
        df[country_index[i]] = country_exchange
    else:
        df[country_index[i]][0:len(country_exchange)] = country_exchange

df.index = date_index
df.to_excel("Total_exchange.xlsx")
   
    
print(" 실행 시간 : " + time.time()-start + "  초")

```

