from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse


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
    