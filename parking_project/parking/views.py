from django.views.generic.base import TemplateView


#--- TemplateView
class HomeView(TemplateView):

    template_name = 'home.html'
