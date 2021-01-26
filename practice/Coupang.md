

# 쿠팡 스크래핑 하기



>요즘 쿠팡에 없는게 없고 많이 사용하기도 해서 가격을 잘 모르는 물건이나 전체으로 물건들은 한번에 비교해보면 재미있을것 같아서 특정 검색어 기준으로 검색했을 때 나오는 결과들을 스크래핑 해보았다. 우선 필자가 평소에 많이 먹는 우유를 검색어로 테스트 해보겠다



## 0. Import

```python
import requests
import urllib.request
from selenium import webdriver
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
```

 :  스크래핑을 위한 urlopen , BeautifulSoup , Selenium 과 데이터분석을 위한 pandas , re  를 임포트 했음



## 1. 검색 URL 가져오기

:  우선 쿠팡 내에서 "우유" 라는 검색어를 통한 url 을 받을려고 했는데 시작부터 문제가 발생했다...



> ### 1) 쿠팡 url 불러오기 (실패1 - urlopen)

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.coupang.com/")
bs = BeautifulSoup(html , 'lxml')
```

 :  ulropen 을 통해서 쿠팡 홈페이지를 읽어볼려고 했는데 `403 Forbidden`에러가 나오면서 읽히지 않는다... 



> ### 2) 쿠팡 url 불러오기 (실패2 - Selenium)

```python
from selenium import webdriver

# 크롬 드라이버 초기화
def init_driver():
    return webdriver.Chrome("./chromedriver.exe")

driver = init_driver()
url = "https://www.coupang.com/"
driver.get(url)
driver.find_element_by_css_selector("div.header-searchForm input").value
```

 : 필자는 html 과 스크래핑에 얕은 지식밖에 없으므로 일단 `Selenium` 을 통해 Chrome Web Driver 로 불러봤지만 크롬드라이브로 쿠팡 실행까진 되지만 이상하게 검색해주는 입력값에 대한 Value 를 찾을 수가 없다. 내가 모르는 html  구조상 문제가 있는건가 싶다.. 



> ### 3) 쿠팡 url 불러오기 - requests.get(url , header)

```python
url = "https://www.coupang.com/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
res = requests.get(url, headers = headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")
```

 :  열씸히 구글링 하다보니 쿠팡에 대해 스크래핑 하신 분의 블로그를 발견해서 답을 찾을 수 있었다.   감사합니다. 코드는 대충 봐도 내가 모르는 내용이다..  일단 체크해두고 다음 스텝으로 진행하겠다



> ### 4) 쿠팡 검색어 url  불러오기


```python
def get_source(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    return BeautifulSoup(res.text, "lxml")

search_url = "https://www.coupang.com/np/search?component=&q="
keyword = "우유"
bs = get_source(search_url + keyword)
bs
```

​	:   헤더를 통해 url 을 읽어와서 `BeautifulSoup` 로 html 을 꺼내오는 부분은 자주 쓸 거같아서 함수 `get_source` 로 정의해두었다. 다음은 쿠팡 홈페이지를 확인해서 검색어를 입력했을때 나오는 url 을 기본 url 로 지정해두고 keyword 를 붙여서  검색에 사용할 url 을 가져왔다.  결과가 출력될때 로딩이 좀 있어도 잘 나오니 긴장하지 말고 기다리자



## 2. 스크래핑



>  ### 0) 필요한 데이터 항목들

```
1. 물건 이름 
2. 물건 가격
3. 물건 단위당 가격 (ex 100ml 당 400원)
4. 로켓배송/로켓직구/로켓와우
5. 배송예정일
6. 상품 평점/후기 수
7. 적립금 
```

![Coupang_example (3)](https://github.com/Rnlcksgdkd/WebScraping.git/practice/img/Coupang_example(3).png)

> ###  1) 첫 페이지에 대해서 스크래핑 하기


```python
items = bs.select('li.search-product')

for n,i in enumerate(items):
    
    # 1. 상품 이름
    print(i.select('div.name')[0].text.strip())
    
    # 2. 상품 가격
    print(i.select('div.price-area strong')[0].text)

    # 3. 상품 단위 가격 (명시되지 않는 경우도 있음)
    try: print(i.select('div.price-area span.unit-price')[0].text)
    except : pass   
    
    # 4. 로켓배송/로킷직구/로켓와우 
    try: print(i.select('div.price-area div.delivery span.badge.falcon img')[0].get('alt'))
    except : pass
    
    # 5. 배송 예정일
    print(i.select('div.price-area div.delivery')[0].text)
    
    # 6. 후기 별점(후기수)
    try : print(i.select('div.other-info')[0].text)
    except : pass   
      
    # 7. 적립금
    print(i.select('div.benefit-badges')[0].text)
    
    print("-----------")
    
    if n > 4:
        break
```

​	:   열씸히 쿠팡 사이트를 찾아가며 내가 필요한 정보가 담긴 태그들을 찾아 파싱을 하였다. 각 상품들이 `li.search-product` 태그안에 들어가 있으며  상품단위가격/배송방법(로켓 배송등)/별점은 없는 경우에 에러가 나므로 `try/except` 문을 넣어두었고 한번에 너무 많이 보려면 현기증이 나니 5개만 보도록 하자


![Coupang_example (2)](https://github.com/Rnlcksgdkd/WebScraping.git/practice/img/Coupang_example (2).png)


> ### 2) Pandas 데이터 프레임 형태로 저장

```python
import pandas as pd

css_items = bs.select('li.search-product')
items = []
for n,i in enumerate(css_items):
    
    # 1. 상품 이름
    name = i.select('div.name')[0].text.strip()
    
    # 2. 상품 가격
    price = int(i.select('div.price-area strong')[0].text.replace(",", ""))

    # 3. 상품 단위 가격 (명시되지 않는 경우도 있음)
    unit_price = ""
    try: unit_price = i.select('div.price-area span.unit-price')[0].text
    except : pass   
    
    # 4. 로켓배송/로킷직구/로켓와우 
    delivery_type = ""
    try: delivery_type = i.select('div.price-area div.delivery span.badge.falcon img')[0].get('alt')
    except : pass
    
    # 5. 배송 예정일
    delivery_date = ""
    try: delivery_date = i.select('div.price-area div.delivery')[0].text
    except : pass 
    # 6. 후기 별점(후기수)
    try : rate = i.select('div.other-info')[0].text
    except : pass

    # 7. 적립금
    plus = i.select('div.benefit-badges')[0].text    
    items.append([name,price,unit_price,delivery_type,delivery_date,rate,plus])

df = pd.DataFrame(items)
df.columns = ["Name" , "Price" , "Unit_Price" , "Delivery_type" , "Delivery_Date" , "Rate" , "Plus"]
df.head(5)
```

​	:   위 코드에서는 print 로 테스트를 해보았고 이번에는 `items` 라는 변수에 각 데이터들을 담아두었고 `Pandas` 라이브러리의 데이터프레임형태로 저장해두고 칼럼명들을 지정해주었다.  값이 주어지지 않은 경우에는 None 값을 주었음 , 또 가격의 경우 str 형에다가 3자리마다 `,` 가 붙어있어서 replace 로 지워주고 int형으로 바꿔주었다.


![Coupang_example (4)](https://github.com/Rnlcksgdkd/WebScraping.git/practice/img/Coupang_example (4).png)
=======




> ### 3) Selenium 을 이용해서 전체 페이지에 대해서 스크래핑 하기

 	Selenium 을 이용해서 한 페이지가 아닌 이동하면서 전체 페이지에 대해서 스크래핑 하도록 while 문 설정 / 데이터 프레임 xlsx 파일로 저장

```python
# 크롬 드라이버 초기화 함수
def init_driver():
    return webdriver.Chrome("./chromedriver.exe")

items = []
driver = init_driver()
page_url = "https://www.coupang.com/np/search?q=%EC%9A%B0%EC%9C%A0&channel=user&page="
page = 0

while(1):
    page += 1
    url = page_url + str(page)
    driver.get(url)
    bs = get_source(url)
    css_items = bs.select('li.search-product')
    try : driver.find_element_by_css_selector('a.btn-next')
    except : break
    
    for n,i in enumerate(css_items):

        # 1. 상품 이름
        name = i.select('div.name')[0].text.strip()

        # 2. 상품 가격
        price = int(i.select('div.price-area strong')[0].text.replace(",", ""))

        # 3. 상품 단위 가격 (명시되지 않는 경우도 있음)
        unit_price = ""
        try: unit_price = i.select('div.price-area span.unit-price')[0].text
        except : pass   

        # 4. 로켓배송/로킷직구/로켓와우 
        delivery_type = ""
        try: delivery_type = i.select('div.price-area div.delivery span.badge.falcon img')[0].get('alt')
        except : pass

        # 5. 배송 예정일
        delivery_date = ""
        try: delivery_date = i.select('div.price-area div.delivery')[0].text
        except : pass 
        
        # 6. 후기 별점(후기수)
        try: rate = i.select('div.other-info')[0].text
        except : pass

        # 7. 적립금
        plus = i.select('div.benefit-badges')[0].text

        items.append([name,price,unit_price,delivery_type,delivery_date,rate,plus])

df = pd.DataFrame(items)
df.columns = ["Name" , "Price" , "Unit_Price" , "Delivery_type" , "Delivery_Date" , "Rate" , "Plus"]
df.to_excel("Coupang {} Searching Result.xlsx".format(keyword) , index=False)
```

- Selenium 을 이용해 1페이지가 아닌 전체 페이지를 이동하면서 스크래핑하도록 While 문 
- DataFrame 을 `to_excel()`을 통해 xlsx로 저장



![Coupang_example (5)](./img/Coupang_example (5).png)

 :  다음과 같이 xlsx 파일로 성공적으로 저장이 되었고 파일 내용들을 보다보니 밑의 사진과 같이 정체를 알 수 없는 우유들이 섞여있었다.

![Coupang_example (6)](./img/Coupang_example (6).png)

이외에도 우유가 아닌 요구르트/우유맛 무언가들이 같이 검색이 된 걸 확인 할 수 있었고 우유가 아닌 것들을 제외해야 할 것 같다.



> ### 4)  데이터 정제하기

```
불필요한 물건을 제외하기 위해거 Re 모듈을 이용해서 상품이름에 "우유" 가 들어가 있지 않은 물건은 제외하고 del_items 에 따로 확인하기 위해 빼두었음
```



```python
## Re 패키지를 이용해서 키워드가 들어가있는지 확인 예제

ob = re.search("우유" , "릴리푸리 여아용 MILK 상하복")
if ob == None : 
    print("우유가 없어요")

```

​	:   re.search(keyword , string) 을 이용하면 string 내 keyword 가 존재하는지 확인할 수 있다

```python
items = []
del_items = []

driver = init_driver()
page_url = "https://www.coupang.com/np/search?q=%EC%9A%B0%EC%9C%A0&channel=user&page="
page = 0

while(1):
    page += 1
    url = page_url + str(page)
    driver.get(url)
    bs = get_source(url)
    css_items = bs.select('li.search-product')
    try : driver.find_element_by_css_selector('a.btn-next')
    except : break
    
    for n,i in enumerate(css_items):

        # 1. 상품 이름
        name = i.select('div.name')[0].text.strip()
        # 광고성 / 물건 이름에 키워드가 들어가지 않는 경우는 제외
        ob = re.search(keyword , name)
        if ob == None : 
            del_items.append(name)
            continue

        # 2. 상품 가격
        price = int(i.select('div.price-area strong')[0].text.replace(",", ""))

        # 3. 상품 단위 가격 (명시되지 않는 경우도 있음)
        unit_price = ""
        try: 
            unit_price = i.select('div.price-area span.unit-price')[0].text
            u
        except : pass   

        # 4. 로켓배송/로킷직구/로켓와우 
        delivery_type = ""
        try: delivery_type = i.select('div.price-area div.delivery span.badge.falcon img')[0].get('alt')
        except : pass

        # 5. 배송 예정일
        delivery_date = ""
        try: delivery_date = i.select('div.price-area div.delivery')[0].text
        except : pass 
        
        # 6. 후기 별점(후기수)
        try: rate = i.select('div.other-info')[0].text
        except : pass

        # 7. 적립금
        plus = i.select('div.benefit-badges')[0].text

        items.append([name,price,unit_price,delivery_type,delivery_date,rate,plus])

df = pd.DataFrame(items)
df.columns = ["Name" , "Price" , "Unit_Price" , "Delivery_type" , "Delivery_Date" , "Rate" , "Plus"]
df.to_excel("Coupang {} Searching Result.xlsx".format(keyword) , index=False)

del_df = pd.DataFrame(del_items)
print(del_df)
```

​	:  상품 이름을 불러오는 부분에서 키워드가 들어가 있는지 확인하고 없다면 del_items 에 따로 넣어두고 루프를 진행함



[del_df :  이름에 "우유"가 안 들어가 있는 상품들]


![Coupang_example (8)](./img/Coupang_example (8).png)



## 3.  전체 코드

```
키워드를 입력받아서 쿠팡 홈페이지에서 키워드로 검색한 결과를 스크래핑 한 후에 xlsx 형태로 저장
```

```python

### 전체 코드

## IMPORT
import requests
import urllib.request
from selenium import webdriver
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# url-request 함수 , html 리턴
def get_source(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    return BeautifulSoup(res.text, "lxml")

# Selenium 드라이버 실행 , driver 리턴
def init_driver():
    return webdriver.Chrome("./chromedriver.exe")

# 키워드를 입력받아서 스크래핑 후 xlsx 저장
def search_coupang(keyword):
    items = []
    driver = init_driver()
    page_url = "https://www.coupang.com/np/search?q=%EC%9A%B0%EC%9C%A0&channel=user&page="
    page = 0
    while(1):
        page += 1
        url = page_url + str(page)
        driver.get(url)
        bs = get_source(url)
        css_items = bs.select('li.search-product')
        try : driver.find_element_by_css_selector('a.btn-next')
        except : break
        for n,i in enumerate(css_items):
            # 1. 상품 이름
            name = i.select('div.name')[0].text.strip()
            # 광고성 / 물건 이름에 키워드가 들어가지 않는 경우는 제외
            ob = re.search(keyword , name)
            if ob == None : 
                continue
            # 2. 상품 가격
            price = int(i.select('div.price-area strong')[0].text.replace(",", ""))
            # 3. 상품 단위 가격 (명시되지 않는 경우도 있음)
            unit_price = ""
            try: 
                unit_price = i.select('div.price-area span.unit-price')[0].text
            except : pass   
            # 4. 로켓배송/로킷직구/로켓와우 
            delivery_type = ""
            try: delivery_type = i.select('div.price-area div.delivery span.badge.falcon img')[0].get('alt')
            except : pass
            # 5. 배송 예정일
            delivery_date = ""
            try: delivery_date = i.select('div.price-area div.delivery')[0].text
            except : pass 
            # 6. 후기 별점(후기수)
            try: rate = i.select('div.other-info')[0].text
            except : pass
            # 7. 적립금
            plus = i.select('div.benefit-badges')[0].text
            items.append([name,price,unit_price,delivery_type,delivery_date,rate,plus])
    df = pd.DataFrame(items)
    df.columns = ["Name" , "Price" , "Unit_Price" , "Delivery_type" , "Delivery_Date" , "Rate" , "Plus"]
    df.to_excel("Coupang {} Searching Result.xlsx".format(keyword) , index=False)
    print("Saving Succesfully")

```

```python
keyword = "우유"
search_coupang(keyword)
```



---



다음 편에는 스크래핑한 결과를 갖고 본격적으로 데이터 분석해보도록 해보곘습니다 
