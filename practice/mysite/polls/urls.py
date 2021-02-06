from django.urls import path
from polls import views


app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),    # /polls/
    path('<int:host_info_id>/', views.detail, name='detail'),       # /polls/5/
    path('searching/' , views.searching , name = 'searching'),
    path('searching/test' , views.test , name = 'test'),
    
    path('base/' , views.base , name = 'base'),
    path('search/' , views.search , name = 'search'),
    path('search/test' , views.test , name = 'test'),
    # path('<int:question_id>/results/', views.results, name='results'),     # /polls/5/results/
    # path('<int:question_id>/vote/', views.vote, name='vote'),      # /polls/5/vote/

    
]
