from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Article
from groups.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model
from django.views import generic
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views her

User = get_user_model()

class ArticleList(SelectRelatedMixin,generic.ListView):
    model = Article
    select_related = ('user', 'group')


class SingleArticle(generic.DetailView):
    model = Article

class UserArticles(generic.ListView):

    def get_queryset(self):
        try:
            self.article_user = User.objects.prefetch_related("articles").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.article_user.articles.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_user'] = self.article_user
        return context
        

class ArticleDetail(SelectRelatedMixin,generic.DetailView):
    model = Article
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
                         user__username__iexact=self.kwargs.get("username")

        )
    

class CreateArticle(LoginRequiredMixin, SelectRelatedMixin,generic.CreateView):
    fields = ('title','message','group')
    model = Article


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    

class DeleteArticle(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = Article
    select_related = ("user","group")
    success_url  = reverse_lazy("articles:all")


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
    
    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
    