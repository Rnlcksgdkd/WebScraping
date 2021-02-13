

from django.urls import path
from polls import views

from polls.views import Info_View
from . import views
app_name = 'polls'

urlpatterns = [

    # 메인 페이지 URL
    path('', views.base, name='base'),   
    path('index', views.index , name = 'index'),
    ## 숙소 정보 URL
    path('info/searching/' , Info_View().searching , name = 'Info_searching'),
    path('info/searching/detail/<int:Accomodation_id>' , Info_View().detail , name = 'Info_detail'),
    path('info/searching/map' , Info_View().map , name = 'Info_map'),


    ## 커뮤니티 게시판 URL
    path('pybo', views.index2 ,name = 'question_list'),
    path('pybo/detail/<int:question_id>', views.detail2 ,name = 'question_detail'),
    path('', views.index),

    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),




    ## 로그인 URL

]
