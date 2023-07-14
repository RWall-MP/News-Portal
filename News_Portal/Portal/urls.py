from django.urls import path
from .views import (PostsList, PostDetail, NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate, PostDelete,
                    CategoryListView, subscribe, unsubscribe, subscriptions)


urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('atricle/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('atricle/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    path('subscriptions/', subscriptions, name='subscriptions'),

]
