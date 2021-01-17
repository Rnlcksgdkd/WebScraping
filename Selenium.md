## Selenium

> webdriver 라는 API 를 통해 Chrome 등의 브라우저를 제어 가능
>
> BeautifulSoup랑 다르게 직접 제어해서 웹 브라우저가 동작하기 때문에 동적 제어 가능



1. 크롬드라이버 웹 브라우저 열기

2. 드라이버를 통해 태그/값 불러오기
3. 셀레니움 - 클릭/로그인 등 동적 제어



### WebDriver 객체



### WebContent 객체







> 예제 1) 크롬 드라이브를 이용해서 구글 열기

```python
from selenium import webdriver
driver = webdriver.Chrome(chromedriver.exe)
driver.get('https://google.com')
```

| 메서드                                   | Description                                    |
| ---------------------------------------- | ---------------------------------------------- |
| find_element_by_name('HTML_name')        |                                                |
| find_element_by_id('HTML_name')          |                                                |
| find_element_by_xpath'HTML_name')        |                                                |
| find_element_by_css_selector'HTML_name') | BeautifulSou 의 select 와 사용방법이 거의 같음 |
| find_element_by_class_name('HTML_name')  |                                                |
| find_element_by_tag_name('HTML_name')    |                                                |

driver.page_source



> 예제 2) 크롬 드라이브를 이용해서 로그인하기

```python
driver.get('https://nid.naver.com/nidlogin.login')
driver.find_element_by_name('id').send_keys('naver_id')
driver.find_element_by_name('pw').send_keys('password')
driver.find_element_by_css_selector("input.btn_global").click()

## 어떤 사이트든 상관없이 ID 입력란 , PWD 입력란 , 클릭 세가지 부분만 찾으면 로그인 가능
```

### `send_keys`

> 아마 input 태그에 한해서 가능할듯?

### `Click`

> 클릭 가능 , css_selector 로 원하는 범위의 css 를 긁어오고 .click() 함수로 누르는 동작이 가능



---



iframe 에 대해서 긁어올수 있나?

## Selenium vs BeautifulSoup

- 페이지 이동 : 클릭 vs urlopen