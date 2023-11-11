from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse
from .models import Article,Like,Bookmark
from django.http import Http404
from django.shortcuts import get_object_or_404



from django.shortcuts import redirect
from groups.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model
from django.views import generic
from django.http import Http404
from django.urls import reverse_lazy,reverse
from django.contrib import messages
# Create your views her

User = get_user_model()

class ArticleList(SelectRelatedMixin,generic.ListView):
    model = Article
    select_related = ('user', 'group')


class SingleArticle(generic.DetailView):
    model = Article

class UserArticles(generic.ListView):
    model = Article  # Set the model to Article

    def get_queryset(self):
        try:
            self.article_user = User.objects.get(username__iexact=self.kwargs.get("username"))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.article_user.articles.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_user'] = self.article_user
        context['no_articles'] = context['article_list'].count() == 0  # Check if the user has no articles
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
    fields = ('title','message','group', 'image')
    model = Article


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)       
    
class ArticleListView(generic.ListView):
    model = Article
    template_name = 'home.html'
    context_object_name = 'articles'

    

class DeleteArticle(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = Article
    select_related = ("user","group")
    success_url  = reverse_lazy("profile")


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
    
    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)




class LikeCreate(LoginRequiredMixin, generic.CreateView):
    model = Like
    fields = []

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        liker = self.request.user

        # Check if the user has already liked the article.
        if Like.objects.filter(article=article, liker=liker).exists():
            # The user has already liked this article, so remove the like (unlike).
            like = Like.objects.get(article=article, liker=liker)
            like.delete()
        else:
            # The user hasn't liked this article, so create a new Like instance (like).
            like = Like(article=article, liker=liker)
            like.save()

        # Manually create a redirect response to the article's detail page
        return redirect('articles:single', username=article.user.username, pk=article.pk)
    

class BookMarkCreate(LoginRequiredMixin, generic.CreateView):
    model = Bookmark
    fields = []


    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        booker = self.request.user
        print("Form is valid. Bookmark will be created.")
        
        if Bookmark.objects.filter(article=article, booker=booker).exists():
            bookmark = Bookmark.objects.get(article=article, booker=booker)
            bookmark.delete()
        else:
            bookmark = Bookmark(article=article,booker=booker)
            bookmark.save()

        return redirect('articles:single', username=article.user.username,pk=article.pk)
        

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Bookmarked(generic.ListView):
    model = Article  # Set the model to Article
    
    def get_queryset(self):
        # Get the currently logged-in user
        user = self.request.user

        # Get a list of article IDs that the user has bookmarked
        bookmarked_article_ids = Bookmark.objects.filter(booker=user).values_list('article', flat=True)

        # Filter articles based on the user's bookmarks
        return Article.objects.filter(pk__in=bookmarked_article_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_articles'] = context['article_list'].count() == 0  # Check if the user has no bookmarked articles
        return context
