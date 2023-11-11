from django.urls import path,re_path
from . import views


app_name = 'articles'


urlpatterns = [
    path('',views.ArticleList.as_view(),name='all'),
    path('bookmarks/',views.Bookmarked.as_view(),name='bookmarks'),
    path('new/',views.CreateArticle.as_view(),name='create'),
    path('delete/<int:pk>/',views.DeleteArticle.as_view(),name='delete'),
    path('by/<str:username>/<int:pk>/',views.ArticleDetail.as_view(),name='single'),
    path('by/<str:username>/',views.UserArticles.as_view(),name="for_user"),
    path('list/',views.ArticleListView.as_view(),name='list'),
    path('article/<int:pk>/like/', views.LikeCreate.as_view(), name='like_article'),
    path('article/<int:pk>/bookmark/', views.BookMarkCreate.as_view(), name='bookmark_article'),

    re_path(r'^posts/in/(?P<message_html>[-\w]+)/$', views.SingleArticle.as_view(), name='single_article'),





]



