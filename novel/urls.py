from django.urls import path, include
from . import views

# start with novel
urlpatterns = [
    path('', views.novel_list, name='novel_list'),
    path('<int:novelid>.html', views.novel_detail, name='novel_detail'),
    path('novel_writer/<str:writername>/.html', views.novel_writer, name='novel_writer'),
    path('chapter/<int:chapterid>/.html', views.chapter_detail, name='chapter_detail'),
    path('search/', include('haystack.urls')),
]