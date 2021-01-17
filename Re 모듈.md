### Re 모듈

> 
> 
> 



## 1. Re 패키지 기본 메소드

> import re  필요
>
> 문자열과 패턴이 유사 or 일치 하는지 확인하는 메소드들
>
> 공통적으로 (pattern , string , flags) 인자를 가짐
>
> matchObj  객체를 리턴으로 갖는 메소드가 많음 

### `re.math(pattern , string , flags)`

> string 이 pattern 으로 시작되는지 확인

```python
import re

matchObJ = re.match('a' , 'a')
print(matchObj) 
print(re.match('a' , 'aba'))
print(re.match('a' , 'bbc'))
print(re.match("abc" , "abeeeee"))
print(re.match("abc" , "abcabce"))

```



### `re.search(pattern , string ,flags)`

> re.match 와 유사하지만 , 문자열의 처음부터 일치하지 않아도 된다

```python
print(re.search("a" , "bbbbcccac"))
print(re.search("abc" , "abcsdawdasdsad"))
print(re.search("abc" , "absdwdsdaabcasdaw"))
```



### `re.findall(pattern , string ,flags)`

> 패턴과 일치되는 모든 부분을 찾는다

```python
print(re.findall('a' , 'aba'))
print(re.findall("ab" , "bababbaB"))	# 소문자 대문자 구분함
```



### `re.finditer(pattern , string ,flags)`

> findall 함수와 유사하지만 리스트 대신 matchObj  리스트를 반환

```python
matchObj_iter = re.finditer("ab" , "bababbaA")

print(matchObj_iter)	# matchObj 들이 리스트로 들어가있음 , 직접 확인 X

for matchObj in matchObj_iter:	# for문을 통해 matchObj 순회
    print(matchObj)
    
```



### `re.fullmatch(pattern , string ,flags)`

> pattern 과 string 이 완벽하게 일치하는지 검사

```python
print(re.fullmatch('a' , 'aba'))
print(re.fullmatch('a' , 'ccc'))
print(re.fullmatch('abc' , 'abc'))
print(re.fullmatch("What?" , "What?"))		# ? 는 비교자체가 안됨  None 리턴
```





---



## 2. match Object 의 메서드들

> matchObj 객체를 출력해서 쓰기에는 상당히 마음에 안들것이다 ,  matchObject 의 메서드들을 이용하여 원하는 값을 빼올 수 있다



| Method           | Description                                        |
| ---------------- | -------------------------------------------------- |
| matchObj.group() | 일치된 문자열 반환                                 |
| matchObj.start() | 일치된 문자열 시작 위치                            |
| matchObj.end()   | 일치된 문자열 끝 위치                              |
| matchObj.span()  | 일치된 문자열의 span (시작위치 , 끝위치) 튜플 반환 |

```python
matchObj_iter = re.finditer("ab" , "abbabcbaabBaBab")

for matchObj in matchObj_iter:
    print("match Obj : " , matchObj)
    print("matchObj.group() : " , matchObj.group())
    print("matchObj.start() : " , matchObj.start())
    print("matchObj.end() : " , matchObj.end())
    print("matchObj.span() : " , matchObj.span())
```

---



## 3. 메타문자 

> 메타문자란?

```
mobj = re.fullmatch("What is Your goal?" , "What is Your goal?")
print(mobj)
```

# `$()*+.?[\^{|`



## `.`

>

```

```



## `[]`

```

```



## `\`

```

```



## `+`

> 반복되는 패턴이 하나 이상일 경우  가능한 많은 부분을 중첩시키도록 검색

```python
s = "aaaaaaaaaaaaabbaacacdea"
print(re.findall("a" , s))
print(re.findall("a+" , s))

s = "abababaaccabcdeab"
print(re.findall("ab" , s))
print(re.findall("ab+" , s))

```



## `*`

>ㄴㅇ

```

```



## `&`

>ㄴㅇ

```

````



## `$`

>ㄴㅇ

```

```





```python
tags = re.findall(r'#[^\s#,\\]', content)

r 
^
\s : 공백문자
# : #
, : ,
\\ : 특수문자 + 공백
```

