from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from polls.models import Accomodation
from django.views.generic import View

## html 구성
# polls/index.html : 메인페이지
# polls/input.html : 데이터 입력 페이지
# polls/output.html : 데이터 출력 페이지
# polls/search.html : 데이터 검색 페이지


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
    search_keyword = request.POST['search_keyword']
    #search_result_host_info = get_object_or_404(Host_info, host_name = search_keyword)
    #search_result = Accomodation.objects.all().filter(room_name__icontains= search_keyword)
    search_result = Accomodation.objects.all().filter(room_name__icontains=search_keyword)
    return render(request, 'info/searching.html', {'search_result': search_result})


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