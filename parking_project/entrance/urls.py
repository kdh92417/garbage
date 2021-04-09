from django.urls    import path
from .              import views

app_name = 'entrance'
urlpatterns = [
    path('in/', views.InView.as_view(), name='in'),
    path('out/<int:car_id>/', views.OutView.as_view(), name='out'),
    # path('search/', views.SearchCarView.as_view(), name='search'),
    path('discount/<int:record_id>/', views.DiscountView.as_view(), name='discount'),
    path('payment/<int:record_id>/', views.PaymentView.as_view(), name='payment'),
    path('manager/', views.ManagerView.as_view(), name='manager'),
    path('manager/car/', views.CarManagerView.as_view(), name='car_manager'),
]



