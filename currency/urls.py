from django.urls import path
from . import views

urlpatterns = [
        path('', views.CurrencyPairListView.as_view(), name='currencypairs'),
        path('get_rates', views.ChartData.as_view(), name='get_rates'),

]
