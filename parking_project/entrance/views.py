from django.shortcuts   import render
from django.views       import View

class InView(View):
    def get(self, request):


        return render(request, 'entrance/in.html')
