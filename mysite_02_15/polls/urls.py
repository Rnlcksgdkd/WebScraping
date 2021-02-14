

from django.urls import path

from polls.views import Info_View
from django.contrib.auth import views as auth_views
from . import views

app_name = 'polls'

urlpatterns = [

    # 메인 페이지 URL
    path('', views.base, name='base'),   
    path('index', views.index , name = 'index'),

    ## 숙소 정보 URL
    path('info/searching/', Info_View().searching , name = 'Info_searching'),
    path('info/searching/detail/<int:Accomodation_id>' , Info_View().detail , name = 'Info_detail'),
    path('info/searching/map', Info_View().map , name = 'Info_map'),

    ## 커뮤니티 게시판 URL
    path('community', views.index2, name='question_list'),
    path('community/detail/<int:question_id>/', views.detail2, name='question_detail'),
    path('community/question/create/', views.question_create, name='question_create'),
    path('community/answer/create/<int:question_id>/', views.answer_create, name='answer_create'),

    ## 로그인 URL
    path('login/', auth_views.LoginView.as_view(template_name='info/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
