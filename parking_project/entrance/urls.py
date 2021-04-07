from django.urls    import path
from .              import views

app_name = 'entrance'
urlpatterns = [
    path('in/', views.InView.as_view(), name='in'),
    path('out/', views.OutView.as_view(), name='out'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('result/', views.PayView.as_view(), name='pay')
]



