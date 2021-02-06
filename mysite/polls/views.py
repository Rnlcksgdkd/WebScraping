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

def base(request):
    
    return render(request, 'base.html')


def map(request):


    return render(request, 'info/map.html')


# def search(request):

#     all_host_list = Host_info.objects.all()
#     context = {'all_host_list': all_host_list}
#     return render(request, 'polls/search.html', context)


# def index(request):
    
#     all_host_list = Host_info.objects.all()
#     context = {'all_host_list': all_host_list}
#     return render(request, 'polls/index.html', context)

# def detail(request, host_info_id):
#     host_info = get_object_or_404(Host_info, pk=host_info_id)
#     return render(request, 'polls/detail.html', {'host_info': host_info})


def detail(request , Accomodation_id  = 3):
    acmd = get_object_or_404(Accomodation, pk=Accomodation_id)
    return render(request, 'info/detail.html', {'acmd': acmd})

def searching(request):
    # template = loader.get_template('info/map.html')
    # return render(request , template)

    if request.method == "POST":
        search_keyword = request.POST['search_keyword']
        search_result = Accomodation.objects.all().filter(room_name__icontains=search_keyword)
        
        NAME = []
        X = []
        Y = []
        for acmd in search_result:
            NAME.append(acmd.room_name)
            X.append(acmd.latitude)
            Y.append(acmd.longitude)
        
        save_Map(NAME , X, Y)

        return render(request, 'info/searching.html', {'search_result': search_result})

    return render(request , 'info/searching.html')




# HTML 로 저장한다
def save_Map(NAME, Y, X):
    save_dir = "./"

    df = pd.DataFrame({"X" : X , "Y" : Y})
    df["X"] = pd.to_numeric(df["X"])
    df["Y"] = pd.to_numeric(df["Y"])
    map_searching = folium.Map(location = [df["Y"].mean() , df["X"].mean()], zoom_start = 13)

    for i in range(len(NAME)):
        folium.Marker((Y[i],X[i]) , radius = 10 , color = "red" , popup = NAME[i]).add_to(map_searching)
    map_searching.save('polls/templates/info/map.html')
    


class Info_View(View):
    def searching(self , request):
        #search_keyword = request.POST['search_keyword']
        #search_result_host_info = get_object_or_404(Host_info, host_name = search_keyword)
        search_result = Accomodation.objects.all().filter(room_name__icontains="호텔")
        #search_result_host_info = Host_info.objects.all().filter(host__icontains=search_keyword)
        return render(request, 'info/searching.html', {'search_result': search_result})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

