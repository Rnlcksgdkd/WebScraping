
# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.views.generic import View
from django.template import loader
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from polls.models import Accomodation
from polls.models import Room_detail
from django.contrib.auth import authenticate, login
from polls.forms import UserForm
from .forms import QuestionForm, AnswerForm
from .models import Question
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

## html 구성
# polls/index.html : 메인페이지
# polls/input.html : 데이터 입력 페이지
# polls/output.html : 데이터 출력 페이지
# polls/search.html : 데이터 검색 페이지
import pandas as pd
import folium
import math
from django.db.models import Q


# 나중에 지울꺼 지금은 메인페이지 대신
def index(request):
    
    return render(request, 'index.html')

# 나중에 지울꺼 지금은 메인페이지 대신
def base(request):
    
    return render(request, 'base.html')


# 맵 정보를 HTML 로 저장
def save_Map(NAME, Y, X):
    save_dir = "./"
    if len(NAME) == 0:
        map_searching = folium.Map(location = [2000 , 2000], zoom_start = 20)
        map_searching.save('polls/templates/info/map.html')
        return 

    if len(NAME) == 1:
        map_searching = folium.Map(location = [Y[0] , X[0]] , zoom_start = 15)
        folium.Marker((Y[0],X[0]) , radius = 10 , color = "red" , popup = NAME[0]).add_to(map_searching)
        map_searching.save('polls/templates/info/map.html')
        return

    df = pd.DataFrame({"X" : X , "Y" : Y})
    df["X"] = pd.to_numeric(df["X"])
    df["Y"] = pd.to_numeric(df["Y"])
    zoom = 12

    dist_var = math.sqrt(df["Y"].var()*1000*df["Y"].var()*1000 +  df["X"].var()*1000* df["X"].var()*1000)
    if dist_var < 0.1 : zoom = 15
    elif dist_var < 1 : zoom = 14
    elif dist_var < 5 : zoom = 13
    elif dist_var < 12: zoom = 12
    elif dist_var < 40 : zoom = 11
    elif dist_var < 250: zoom = 10
    elif dist_var < 700 : zoom = 9
    elif dist_var < 1300 : zoom = 8
    else: zoom = 7
    print("x분산 : {} , y 분산 : {}  , 분산 합 : {} , zoom : {}".format(df["Y"].var()*1000 ,  df["X"].var()*1000, dist_var ,   zoom ))
    
    map_searching = folium.Map(location = [df["Y"].mean() , df["X"].mean()], zoom_start = zoom)
    for i in range(len(NAME)):
        folium.Marker((Y[i],X[i]) , radius = 10 , color = "red" , popup = NAME[i]).add_to(map_searching)
    map_searching.save('polls/templates/info/map.html')
    



# 숙소 정보에 대한 클래스 뷰
class Info_View(View):

    # 숙소 검색 // 숙소이름/지역을 LIKE 검색해서 모두 찾는다
    def searching(self , request):

        # GET 방식으로 불러오기
        if request.method == "GET":
            search_keyword = request.GET['search_keyword']
            page = int(request.GET.get('page' , 1))
            search_result = Accomodation.objects.filter( Q(room_name__icontains=search_keyword) | Q(location__icontains=search_keyword))

            # 페이징 작업 
            paginated_by = 9
            total_count = len(search_result)
            total_page = math.ceil(total_count/paginated_by)
            page_range = range(1,total_page + 1)
            start_idx = paginated_by*(page - 1)
            end_idx = paginated_by*page
            search_result = search_result[start_idx:end_idx]

            # 검색데이터 -> map.html 구성 및 저장
            NAME = []
            X = []
            Y = []
           
            for acmd in search_result:
                NAME.append(acmd.room_name)
                X.append(acmd.latitude)
                Y.append(acmd.longitude)        
            save_Map(NAME , X, Y)

            return render(request, 'info/searching.html', {'search_result': search_result , 'search_keyword' : search_keyword , 'page_range' : page_range})

        return render(request , 'info/searching.html')

    # 숙소의 자세한 정보
    def detail(self, request , Accomodation_id):
        acmd = get_object_or_404(Accomodation, pk=Accomodation_id)
        room_detail_lst = Room_detail.objects.all().filter(room_id = acmd)
        print(acmd , room_detail_lst)
        save_Map([acmd.room_name] , [acmd.latitude] , [acmd.longitude] )
        return render(request, 'info/detail.html', {'acmd': acmd , 'room_detail_lst' : room_detail_lst })

    # 매핑 렌더링
    def map(self, request):
        return render(request, 'info/map.html')


# 회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('base')
    else:
        form = UserForm()
    return render(request, 'info/signup.html', {'form': form})


#게시판
def index2(request):
    """
    게시글 목록 출력
    """
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'info/question_list.html', context)


def detail2(request, question_id):
    """
    게시글 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'info/question_detail.html', context)

@login_required(login_url='polls:login')   #로그인 필수 함수
def question_create(request):
    """
    게시판 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('polls:question_list')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'info/question_form.html', context)

@login_required(login_url='polls:login')  #로그인 필수 함수
def answer_create(request, question_id):
    """
    게시글 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    # ---------------------------------- [edit] ---------------------------------- #
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('polls:question_detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'info/question_detail.html', context)


