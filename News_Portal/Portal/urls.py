from django.urls import path
from .views import PostsList, PostDetail, PostCreate


urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create')

]
