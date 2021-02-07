from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from polls.models import Accomodation
from django.views.generic import View
from django.template import loader
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
            paginated_by = 10
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

