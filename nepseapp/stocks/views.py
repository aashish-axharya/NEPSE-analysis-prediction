from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .forms import BlogPostForm
from .models import StockData
import csv, os
import pandas as pd
from .models import StockData, BlogPost
from django.contrib.admin.views.decorators import staff_member_required
import plotly.graph_objs as go
import plotly.io as pio

def get_file_choices():
    file_list = os.listdir(os.path.join('static', 'data'))
    file_choices = []
    for file in file_list:
        if file.endswith('.csv'):
            file_choices.append(file)
    #show most recent first 
    file_choices = sorted(file_choices,reverse=True)
    return file_choices

def index(request):
    file_choices = get_file_choices()
    stocks = StockData.objects.all()
    return render(request, 'index.html', {'stocks': stocks, 'file_choices': file_choices})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f"Account created successfully for {username}!")
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Add a message to inform the user that the login failed
            message = 'Invalid username or password'
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('index')

def getStockData(request, file_name):
    csv_file = os.path.join('static/data', file_name)
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
    StockData.objects.all().delete()  # Delete all existing objects
    StockData.objects.bulk_create([StockData(**item) for item in data])  # Create new objects from CSV data
    return redirect('index')

def analysis(request):
    return render(request, 'analysis.html')

def blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogPostForm()
    posts = BlogPost.objects.order_by('-created_date')
    return render(request, 'blog.html', {'form': form, 'posts': posts})

def stocks(request):
    file_path = 'static/individual/ADBL.csv'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            stock_data = [row for row in reader]
    else:
        stock_data = []
    return render(request, 'stocks.html', {'stock_data': stock_data})


def predictions(request):
    # Read the prediction data from the CSV file
    df = pd.read_csv('static/predictions/ADBL.csv')

    # Create the plotly graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Predicted Prices'], mode='lines+markers'))
    fig.update_layout(title='Predicted Stock Prices', xaxis_title='Time', yaxis_title='Price')

    # Convert the plotly graph to HTML format
    plot_div = pio.to_html(fig, full_html=False)

    # Render the predictions.html template with the plotly graph
    return render(request, 'predictions.html', {'plot_div': plot_div})

# def predictions(request):
#     file_path = os.path.join('static', 'predictions', 'ADBL.csv')
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             reader = csv.reader(f)
#             next(reader)  # Skip header row
#             predicted_prices = [float(row[0]) for row in reader]
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x=list(range(len(predicted_prices))),
#                                  y=predicted_prices,
#                                  mode='lines+markers'))
#         fig.update_layout(title='Predicted Stock Prices',
#                           xaxis_title='Time',
#                           yaxis_title='Price')
#         plot_div = fig.to_html(full_html=False)
#     else:
#         plot_div = '<p>No predictions available.</p>'
#     return render(request, 'predictions.html', {'plot_div': plot_div})