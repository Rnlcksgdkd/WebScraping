

# 질문 리스트



``` 
1. python manage.py migrate : 컴파일 같은 기능? , 바뀐거 수정할라면 실행?
	- migrate 필요없이 html 은 바로 적용되네
2. { % } , { {변수}}
	- 무슨 문법? html? javascript? django?
	- 두개 차이 ? 
	- { } 는 무엇?
	- 내 생각 {% } : 함수같은 문법 , {{}} : 변수사용
	
3. {% csrf_token %} 뜻?
4. html 중간에 없는 변수를 선언한다던가 에러가 나는 행동을 하면 어떻게 처리?
5. label - for가 먹든 안먹든 따로 자동매칭이아닌가본데?
6. html -> view 함수가 작동되는 시간이 언제지??
	get_object_or404 함수
	choice_set.get(pk =    request.POST['choice']  ) 
```





```
question = get_object_or_404(Question, pk=question_id)


```



`__str__`  의미



`model.id`  :  django 가 부여한 자동 increment 키 value 



` question = get_object_or_404(Question, pk=question_id)`

`selected_choice = question.choice_set.get(pk=request.POST['choice'])`

`request.POST["value_name"]` 











![image-20210203013817755](C:\Users\Ando\AppData\Roaming\Typora\typora-user-images\image-20210203013817755.png)







## models.py



> models.py 예제

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

```

- models.py 는 웹 사이트 구성에 사용할 데이터형태(테이블) 에 대한 정의
- models.Model 로부터 상속
- models.CharField() , models.IntegerField 등 을 통해 형 타입 선언
- Primary Key 는 따로 지정 안해도 알아서 만들어줌
- models.ForeignKey("데이터 클래스" )  ,  외래어키로 받아온다 , 옵션은 밑에 참고





## views.py



- index : 메인 페이지
- input : 입력 페이지
- output : 출력 페이지
- search : 검색 페이지