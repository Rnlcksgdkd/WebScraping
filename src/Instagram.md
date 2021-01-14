# 인스타그램 스크래핑

> 인스타그램에서 "태그" 키워드를 통해 검색해서 데이터를 찾는 스크래핑 코드입니다 , Selenium 을 이용한 동적 제어를 기반으로 검색



## 1.  사용 라이브러리

```python
from selenium import webdriver
import time
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
```

---



## 2. 크롬 드라이버 관련 함수

```python
# 크롬 드라이버 초기화
def init_driver():
    return webdriver.Chrome("./chromedriver.exe")

# 인스타 로그인
def login_instagram(driver , ID = 'dksehgis@gmail.com' , PWD = 'skeoen29' ):
    driver.get("https://www.instagram.com/")
    time.sleep(2)
    driver.find_element_by_name('username').send_keys(ID)
    driver.find_element_by_name('password').send_keys(PWD)
    driver.find_element_by_css_selector("div.Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB").click()

# 인스타 검색 > 첫번째 게시물 클릭
def select_first(driver):
    first = driver.find_element_by_css_selector('div._9AhH0')
    first.click()
    time.sleep(3)
    
# 인스타 검색 > 다음 게시물 이동
def move_next(driver):
    right = driver.find_element_by_css_selector(
        "a._65Bje.coreSpriteRightPaginationArrow")
    right.click()
    time.sleep(3)

```

---



##  3. 인스타 게시물 스크래핑 함수

```python
# 인스타 게시물 내에서 필요한 정보 스크래핑
def insta_get_content(driver): 
    
    html = driver.page_source
    bs = BeautifulSoup(html , 'lxml')
    
    try: content = bs.select('div.C4VMK > span')[0].text
    except: content = ""
    # 태그 추출
    tags = re.findall(r'#[^\s#,\\]+', content)
    try: date = bs.select("time._1o9PC.Nzb55")[0].get("datetime")[:-5]
    except: date = ""
    try: like = int( (bs.select('div.Nm9Fw span')[0].text).replace("," , ""))
    except : like = 0
    # 장소는 없을 수도 있다
    try: place = bs.select('div.M30cS')[0].text
    except: place = ""
    if content == "": return
    
    data = [content , date, like, place, tags]
    return data

```

---



##  4. 스크래핑을 통한 인스타 검색 함수 /  데이터 저장 함수

```python
# 키워드로 인스타 검색 , maxitem 으로 검색할 게시물 숫자 조정    
def instagram_searching(word , maxitem = 1000):
    
    driver = init_driver()
    time.sleep(3)
    login_instagram(driver)
    time.sleep(3)
    
    # 크롬드라이브로 인스타그램 접속
    url = "https://www.instagram.com/explore/tags/" + word
    driver.get(url)
    time.sleep(3)
    index = 0
    meta_data = []
    
    while(1):
        if int(maxitem/20) > 0: percent_index = int(maxitem/20)
        else: percent_index = 1
        if index > maxitem : break      
        if index % percent_index == 0: print("현재 작업 중 : {} % ....".format(round(index/maxitem*100,3)
                                                                         ))  
        try:                            
            if index == 0: select_first(driver)      
            else: move_next(driver)
            if insta_get_content(driver):
                meta_data.append(insta_get_content(driver))
                time.sleep(1)
            index += 1
        except: 
            print("예상치 않는 에러로 스크래핑을 종료했습니다")
            break
            
    save_data_pd(meta_data , word)
    
# 스크래핑 데이터 > 데이터프레임 > 엑셀 저장
def save_data_pd(data , word):
    df = pd.DataFrame(data , columns= ["제목" , "시간" , "좋아요" , "위치" , "태그"])
    df.to_excel("인스타그램 " + word + " 검색 결과.xlsx", encoding="utf-8")
    print("엑셀파일 저장 완료")
    return
```

---



## 5. 추가 업데이트 사항

- folium 라이브러리를 이용한 지도 시각화
- 엑셀 저장될때 한글 자음/모음 분리 현상 (한글 자체가 깨지는건 아닌듯 함) 디버깅
- 유사한 광고 게시물 (완전 똑같진 않아서 중복 삭제에 안걸림) 판별 및 삭제 함수
- TimeSleep 변수로 조정해보기 (로드가 못따라가서 TimeSleep 을 안섞어주면 중간에 튕긴다)
- 중간에 튕길 경우 마지막 링크 저장해놓고 종료하기 (이어서 스크래핑하게)

---



## 6. 참고 자료들



- https://github.com/Play-with-data/datasalon 	//	직장인을 위한 데이터 분식 실무 with 파이썬 (추천)