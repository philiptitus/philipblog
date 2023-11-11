from django.urls import path, re_path
from . import views

app_name = 'posts'

urlpatterns = [
    path("", views.PostList.as_view(), name="all"),
    path("new/", views.CreatePost.as_view(), name="create"),
    path('articles/comment/<int:article_id>/',views.CreatePostSpecific.as_view(), name='specific'),

    path("by/<str:username>/", views.UserPosts.as_view(), name="for_user"),
    path("by/<str:username>/<int:pk>/", views.PostDetail.as_view(), name="single"),
    path("delete/<int:pk>/", views.DeletePost.as_view(), name="delete"),
]
