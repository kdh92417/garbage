from django.shortcuts   import render
from django.views       import View

from entrance.models         import (
    Car,
    Record,
    PaymentRecord
)

#--- TemplateView
class HomeView(View):
    def get(self, request):
        car_filter = {
            'entry_time__isnull' : False,
            'departure_time__isnull' : True
        }

        car = Record.objects.select_related('car').filter(**car_filter)
        res_data = {
            'car' : car
        }
        return render(request, 'home.html', res_data)

