from django.urls    import path
from .              import views

app_name = 'entrance'
urlpatterns = [
    path('in/', views.InView.as_view(), name='in'),
    path('out/', views.OutView.as_view(), name='out'),
    path('discount/<int:record_id>', views.DiscountView.as_view(), name='discount'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('pay/<int:record_id>', views.PayView.as_view(), name='pay')
]



