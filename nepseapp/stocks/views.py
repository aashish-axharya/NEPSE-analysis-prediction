from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import StockData
import csv
from .models import StockData

def index(request):
    stocks = StockData.objects.all()
    return render(request, 'index.html', {'stocks': stocks})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')

def logout(request):
    logout(request)
    return redirect('index')

def getStockData(request):
    csv_file = "static/data/2023-03-15.csv"
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stock_data = {
                'sn': row['SN'],
                'symbol': row['Symbol'],
                'company_name': row['Name'],
                'conf': row['Conf'],
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'vwap': row['VWAP'],
                'volume': row['Vol'],
                'prev_close': row['Prev Close'],
                'turnover': row['Turnover'],
                'trans': row['Trans'],
                'diff': row['Diff'],
                'range': row['Range'],
                'diff_percent': row['Diff Percent'],
                'range_percent': row['Range Percent'],
                'vwap_percent': row['VWAP%'],
                'days120': row['120 days'],
                'days180': row['180 days'],
                'weeks52_high': row['52 weeks high'],
                'weeks52_low': row['52 weeks low']
            }
            data.append(stock_data)
    StockData.objects.bulk_create([StockData(**item) for item in data])
    return render(request, 'index.html', {'data': data})