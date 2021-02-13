from django.shortcuts import render
from .forms import QuestionForm, AnswerForm
# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.views.generic import View
from django.template import loader
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from polls.models import Accomodation
from .models import Question
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

    df = pd.DataFrame({"X" : X , "Y" : Y})
    df["X"] = pd.to_numeric(df["X"])
    df["Y"] = pd.to_numeric(df["Y"])
    map_searching = folium.Map(location = [df["Y"].mean() , df["X"].mean()], zoom_start = 13)

    for i in range(len(NAME)):
        folium.Marker((Y[i],X[i]) , radius = 10 , color = "red" , popup = NAME[i]).add_to(map_searching)
    map_searching.save('polls/templates/info/map.html')

def index2(request):
        """
        pybo 목록 출력
        """

        question_list = Question.objects.order_by('-create_date')
        context = {'question_list': question_list}
        return render(request, 'polls/question_list.html', context)

def detail2(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'polls/question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    # ---------------------------------- [edit] ---------------------------------- #
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'polls/question_detail.html', context)

def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('polls:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'polls/question_form.html', context)





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
    def detail(self, request , Accomodation_id  = 3):
        acmd = get_object_or_404(Accomodation, pk=Accomodation_id)
        return render(request, 'info/detail.html', {'acmd': acmd})

    # 매핑 렌더링
    def map(self, request):
        return render(request, 'info/map.html')

