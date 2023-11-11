from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.shortcuts import render
from articles.models import Article  # Impo

class IndexTemplateView(TemplateView):
    template_name = 'home.html'

class ProfileTemplateView(TemplateView):
    template_name = 'profile.html'


class Test(TemplateView):
    template_name = 'test.html'

class Thanks(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("test"))
        return super().get(request, *args, **kwargs)



def home_view2(request):
    articles = Article.objects.all().order_by('-created_date')
    context = {'articles': articles}
    return render(request, 'home2.html', context)

def home_view(request):
    if request.user.is_authenticated:
        # Get the groups that the user is a member of
        user_groups = request.user.group_set.all()

        # Filter articles based on the groups the user is following
        articles = Article.objects.filter(group__in=user_groups).order_by('-created_date')
        
    else:
        # If the user is not authenticated, show all articles (adjust this as needed)
        articles = Article.objects.all().order_by('-created_date')

    if articles.exists():
        context = {'articles': articles}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home2.html')



