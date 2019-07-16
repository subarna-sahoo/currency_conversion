from django.shortcuts import render
from django.views import generic
from .models import Currency
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from .forms import NameForm,DateForm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests 
import requests_cache
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

requests_cache.install_cache('api_calls_cache', backend='sqlite', expire_after=180)


api_url_1 = 'https://api.exchangeratesapi.io/history?start_at=2018-01-01&end_at=2018-09-01&base=USD&symbols=INR'
api_url_str = 'https://api.exchangeratesapi.io/history?start_at={0}&end_at={1}&base={2}&symbols={3}'

class CurrencyPairListView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Currency
    context_object_name = 'currency_list'   # your own name for the list as a template variable
    queryset = Currency.objects.all()
    #print(queryset)
    template_name = 'currency_list.html'  # Specify your own template name/location

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        print(request.POST)
        base_curr = request.POST['base_curr']
        target_curr = request.POST['target_curr']
        to_date= request.POST['ref_date']
        #start_date = '2019-05-01'
        from_date_time = datetime.strptime(to_date, '%Y-%m-%d') +  relativedelta(months=-2)  
        from_date = from_date_time.strftime('%Y-%m-%d')
        time_period = int(request.POST['wait_time']) if type(request.POST['wait_time'])!=int else request.POST['wait_time']
        api_url = api_url_str.format(from_date,to_date,base_curr,target_curr)
        r = requests.get(api_url)
        print("Time: {0} / Used Cache: {1}".format(datetime.now(), r.from_cache))    
        result = r.json()
        rates = result['rates']
        dates = list(rates.keys())
        dates.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d')) 
        
        exchanges_rates = {'dates' : [], 'rates': []}
        for date in dates:
            exchanges_rates['dates'].append(date)
            exchanges_rates['rates'].append(rates[date][target_curr])
        
        all_rates = exchanges_rates['rates'].copy()
        
        ma_params = [0.05,0.05,0.05,0.05,0.1,0.1,0.1,0.2,0.3]
        for t in range(time_period):
            hist_price = all_rates[-len(ma_params):]
            next_price = sum([a*b for a,b in zip(hist_price,ma_params)])
            all_rates.append(next_price)
        projected_rates = {'dates' : next_n_business_days(datetime.strptime(to_date, '%Y-%m-%d'),time_period), 'rates': all_rates[-time_period:]}
        return Response(projected_rates)

def next_n_business_days(from_date, no_of_days):
    next_days = []
    current_date = from_date
    
    for n in range(no_of_days):
        next_day = current_date + relativedelta(days=1)
        next_days.append(next_day.strftime('%Y-%m-%d'))
        current_date = next_day
    return next_days
