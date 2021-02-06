

from django.urls import path
from polls import views

from polls.views import Info_View

app_name = 'polls'
urlpatterns = [

    path('', views.base, name='base'),    # /polls/
    # path('<int:host_info_id>/', views.detail, name='detail'),       # /polls/5/
    path('info/searching/' , views.searching , name = 'Info_searching'),
    # path('searching/test' , views.test , name = 'test'),
    
    # path('base/' , views.base , name = 'base'),
    # path('search/' , views.search , name = 'search'),
    path('info/searching/detail/<int:Accomodation_id>' , views.detail , name = 'Info_detail'),
    path('info/searching/map' , views.map , name = 'Info_map'),
    # path('<int:question_id>/results/', views.results, name='results'),     # /polls/5/results/
    # path('<int:question_id>/vote/', views.vote, name='vote'),      # /polls/5/vote/

    
]
