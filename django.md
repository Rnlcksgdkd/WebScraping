# django



- django 는 프로젝트 자체가 하나의 덩어리 소스 ,  개별.py 파일로는 돌아가지 않는다
- MVT 구조를 가진다 , 프로젝트 구조의 형태가 거의 정해져 있다



## MVT 구조

> Model / View / Templates

- Model 은 기존의 데이터베이스에서 테이블 생성 하는방법을 클래스로 바꿔놓음
- 어떤 방법으로 url 에 접속하든 urls > views > html (렌더링) 단계를 거친다



## 문법 관련

- django 만의 문법 {{ }} , {% %}  , 특히 {% 은 같이 붙이지 않으면 에러난다
- template 작성할때 html 주석이 아닌 `#- -#`  으로 주석처리를 한다
- 동적변수는 주로 데이터베이스에서 쿼리를 동적으로 가져오거나 사용자의 입력을 받는 경우

- 동적변수를 처리하는 방식은

  html > urls > views :  get/post 방식으로 받음 , urls 은 중간에 이어주는 역활만 한다

  view > html (렌더링) :  렌더링할때 딕셔너리변수로 껴줌

- 파이썬 소스를 처리할 수 있는 곳은 VIEW 이다

- get 으로 다중 파라미터를 가져올때 문법  `"?param1 ={{param1}}&&param2={{param2}}"`
  	- 이거 때매 개고생했다

- request.GET 은 딕셔너리형태로 가져오고 request.GET.get() 은 괄호 안에 key 를 입력하면 value 를 가져온단다 , request.GET.get() 은 에러를 발생시키지 않는다

  

## DB 관련

- django는 데이터베이스 테이블과 `models.py` 를 1대1 매핑하는 ORM 기능이 지원된다

- bulkcreate(object_lst) 를 이용해서 한꺼번에 insert 가 가능하다. 유용한 듯 하다
- .objects.all() : 모든 테이블데이터를 불러온다
- .filter() : 거의 만능 함수이다 , 데이터를 특정조건으로 가져온다
  - Q() 활용 : or / and 조건을 추가해줄 수 있다
- .create() / .save() : insert 기능을 해준다
- delete() : delete 기능을 해준다

 

## 에러 관련

- 장고는 기본적으로 디버깅이 힘든거같다 
- django shell 을 통해 파이썬 + 쿼리 등에 대해 테스트할 수 있다
- python 처리하는 부분 (view.py 나 다른 py 파일들)  은 서버가 돌아가는 프롬프트에 결과가 출력된다. 이를 이용해서 디버깅에 활용할 수 있다.
- 접속 사이트에서 뜨는 template 에러는 주로 html / 렌더링과 관련된 부분이다.

- 404 에러

