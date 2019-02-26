from django.urls import path
from . import views

# start with novel
urlpatterns = [
    path('<int:novelid>.html', views.comment_views, name='comment_views'),
    path('update_comment', views.update_comment, name='update_comment'),
]