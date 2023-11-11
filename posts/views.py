from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models,forms
from articles.models import Article
from django.contrib import messages
from .forms import CreatePostSpecificForm
from django.shortcuts import get_object_or_404
from django.views import generic
from django.http import Http404,HttpResponse
from django.urls import reverse_lazy
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model


# Create your views here.
User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
     model = models.Post
     select_related = ('user','article')



class UserPosts(generic.ListView):
     model = models.Post
     template_name = 'posts/user_post_list'

 
     def get_queryset(self):
                try:
                    self.post_user = User.objects.prefetch_related("posts").get(
                        username__iexact=self.kwargs.get("username")
                        # to get posts related to the user
                    )
                except User.DoesNotExist:
                      raise Http404
                else:
                      return self.post_user.posts.all()
                
     def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['post_user'] = self.post_user
           return context
                
class PostDetail(SelectRelatedMixin, generic.DetailView):
      model = models.Post
      select_related = ("user","article")

      def get_queryset(self):
            queryset = super().get_queryset()
            return queryset.filter(
                              user__username__iexact=self.kwargs.get("username")

            )
      
class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    
    fields = ('message','article')
    model = models.Post

    

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    
class CreatePostSpecific(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    model = models.Post
    form_class = CreatePostSpecificForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['article_id'] = self.kwargs.get('article_id')  # Pass article_id from URL parameters to the form
        return kwargs





class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
      model = models.Post
      select_related = ("user","article")
      success_url = reverse_lazy("profile")        
                

      def get_queryset(self):
        queryset = super().get_queryset()
        if queryset.exists():
            return queryset.filter(user_id=self.request.user.id)
        else:
             HttpResponse('You already deleted this comment silly:)')

      def delete(self, *args, **kwargs):
          messages.success(self.request, "Post Deleted")
          return super().delete(*args, **kwargs)