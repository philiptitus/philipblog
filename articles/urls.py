from django.urls import path,re_path
from . import views


app_name = 'articles'


urlpatterns = [
    path('',views.ArticleList.as_view(),name='all'),
    path('new/',views.CreateArticle.as_view(),name='create'),
    path('delete/<int:pk>/',views.DeleteArticle.as_view(),name='delete'),
    path('by/<str:username>/<int:pk>/',views.ArticleDetail.as_view(),name='single'),
    path('by/<str:username>/',views.UserArticles.as_view(),name="for_user"),
    re_path(r'^posts/in/(?P<message_html>[-\w]+)/$', views.SingleArticle.as_view(), name='single_article'),





]