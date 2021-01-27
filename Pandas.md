# Pandas

> 판다스란 무엇인가



## 0. Series



## 1. DataFrame

`df.info()`

`df.describe()`



## 2. 리스트로 데이터 프레임 생성하기



> 1. 행 데이터들을 통해서 데이터 프레임 생성

```python
lst = [["도현" , "M" , "True"] , ["병철" , "M" , "True"] , ["영화" , "F" , "False"] , ["현기" , "M" , "False"]]       
df = pd.DataFrame(lst , columns = ["Name","Sex","glass"])
```




>2. 열 데이터들을 통해서 데이터 프레임 생성

```python
name = ["도현" , "병철" , "영화" , "현기"]
sex = ["M", "M" , "F", "M"]
glass = [True,True,False,False]
df = pd.DataFrame({"Name" : name , "Sex" : sex , "glass" : glass})
```





`df.scribe`  : 숫자형 변수에 대해서만 통계 출력

`df.to_excel`  dataframe 을 엑셀로 저장

`df[col].unique()` 

`df.pivot_table(values , index , column , aggfunc)`

`df.reset_index(drop = True)`  :  인덱스 초기화 , drop 옵션은 인덱스 칼럼 추가 여부



`df.sort_values(by = "col" , ascending = True)` 

### 칼럼 생성

`df["new_col"] = "new_value"`  : 일괄 값 넣기

`df["new_col"] = lst`	:	칼럼에 리스트 추가

`sum()`



### 칼럼 삭제

df.drop(["column1" , "column2"] , axis = 1 , inplace = True)



### 칼럼 합치기

`merge`

`append`

`join`

    temp = pd.Series(reversed(e) , name = exchange_names[i] )
    df = df.join(temp)
### 칼럼 값 참조

`df['column1'].value_counts()`



### 숫자 세서 프레임 뒤집기

`df['column1'].value_counts()`



### 인덱스

df.index = lst



### 조작

`df.pivottable()`



### 주의!

빈 df 만들어놓고  인덱싱한 값으로 참고하면에러

```
df["col"][0:len(lst)] = lst
```





Serial.mean()





```python
# 로우 드롭
df.drop(대충 index , axis = 0)
df = df.drop(df.head(10).index , axis = 0)

# 칼럼 드롭
df.drop(대충 칼럼명 튜플 , axis = 1)

df.head(5).index
df.loc["1996.06.29":] = df.loc["1996.06.29":]/50
```



