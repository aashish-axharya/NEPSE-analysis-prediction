from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .forms import BlogPostForm
from .models import StockData
import csv, os
import pandas as pd
import numpy as np
from .models import StockData, BlogPost
from django.contrib.admin.views.decorators import staff_member_required
import plotly.graph_objs as go
from datetime import datetime
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

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

def blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = BlogPostForm()
    posts = BlogPost.objects.order_by('-created_date')
    return render(request, 'blog.html', {'form': form, 'posts': posts})

def stocks(request):
    # create a list of stock symbols
    symbols = get_symbol_list()
    
    # read the stock data from the CSV file
    stock = request.GET.get('stock', 'ADBL')
    file_path = os.path.join('static', 'individual', f'{stock}.csv')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            stock_data = [row for row in reader]
    else:
        stock_data = []

    # pass the stock data and symbols to the template
    context = {'stock_data': stock_data, 'stock_names': symbols, 'selected_stock': stock}
    return render(request, 'stocks.html', context)

def predictions(request):
    stock = request.POST.get('stock', 'ADBL')
    # Load the model
    model_path = os.path.join('static', 'models', stock + '.h5')
    if os.path.exists(model_path):
        model = load_model(model_path)
    else:
        return render(request, 'predictions.html', {'message': 'Model not found'})
        
    # Load the data
    data_path = os.path.join('static', 'data', stock + '.csv')
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        return render(request, 'predictions.html', {'message': 'Data not found'})
    
    # Preprocess the data
    scaler = MinMaxScaler(feature_range=(0,1))
    closedf = df['Close'].dropna()
    df1 = scaler.fit_transform(np.array(closedf).reshape(-1,1))
    
    # Prepare the input data for the model
    time_steps = 60
    recent_data = df1[-time_steps:]
    x_recent = recent_data.reshape(1, 1, time_steps)
    
    # Generate the predictions for the next 7 days
    predicted_prices = []
    for i in range(7):
        predicted_price = model.predict(x_recent)
        predicted_prices.append(predicted_price[0][0])
        x_recent = np.append(x_recent[:, :, 1:], [[predicted_price]], axis=2)
    
    # Scale the predicted prices back to their original range
    predicted_prices = scaler.inverse_transform(np.array(predicted_prices).reshape(-1,1)).flatten()
    
    # Generate the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Actual Prices', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=pd.date_range(df['Date'].iloc[-1], periods=8, freq='D')[1:],
                             y=predicted_prices,
                             name='Predicted Prices',
                             mode='lines+markers'))
    fig.update_layout(title=stock + ' Stock Prices',
                      xaxis_title='Date',
                      yaxis_title='Price')
    plot_div = fig.to_html(full_html=False)
    
    return render(request, 'predictions.html', {'plot_div': plot_div})

def analysis(request):
    stock = request.POST.get('stock', 'ADBL') #ADBL is default

    file_path = os.path.join('static', 'individual', f'{stock}.csv')
    data = pd.read_csv(file_path)
    
    # Convert the Date column to a datetime format
    data['Date'] = data['Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
    
    # Set the Date column as the index of the DataFrame
    data.set_index('Date', inplace=True)
    
    # Resample the data to the desired time frame and aggregate the High, Low, and Close values
    resampled_data = data.resample('D').agg({'High': 'max', 'Low': 'min', 'Close': 'last'})
    
    # Calculate additional columns such as Moving Average and Relative Strength Index (RSI) for the stock data
    resampled_data['Delta'] = resampled_data['Close'].diff()
    resampled_data['Gain'] = resampled_data['Delta'].apply(lambda x: x if x > 0 else 0)
    resampled_data['Loss'] = resampled_data['Delta'].apply(lambda x: abs(x) if x < 0 else 0)
    resampled_data['AvgGain'] = resampled_data['Gain'].rolling(window=14).mean()
    resampled_data['AvgLoss'] = resampled_data['Loss'].rolling(window=14).mean()
    resampled_data['RS'] = resampled_data['AvgGain'] / resampled_data['AvgLoss']
    resampled_data['RSI'] = 100 - (100 / (1 + resampled_data['RS']))
    
    # Create the candlestick chart with the stock data and technical indicators
    fig = go.Figure(data=[go.Candlestick(x=resampled_data.index,
                                          high=resampled_data['High'],
                                          low=resampled_data['Low'],
                                          close=resampled_data['Close']),
                          go.Scatter(x=resampled_data.index, y=resampled_data['RSI'], name='RSI')])

    fig.update_layout(xaxis_rangeslider_visible=False, title=f'{stock} Trading Graph')
    
    # Add dotted lines at RSI values of 30 and 70
    fig.add_shape(type="line",
                  x0=resampled_data.index[0], y0=30, x1=resampled_data.index[-1], y1=30,
                  line=dict(color="grey", width=1, dash="dot"))
    fig.add_shape(type="line",
                  x0=resampled_data.index[0], y0=70, x1=resampled_data.index[-1], y1=70,
                  line=dict(color="grey", width=1, dash="dot"))

    # Render the chart in the Django template
    context = {'graph': fig.to_html(full_html=False)}
    return render(request, 'analysis.html', context)

def get_symbol_list():
    symbols = ['ADBL', 'MEGA', 'NABIL', 'NICA']
    return symbols

def get_file_choices():
    file_list = os.listdir(os.path.join('static', 'data'))
    file_choices = []
    for file in file_list:
        if file.endswith('.csv'):
            file_choices.append(file)
    #show most recent first 
    file_choices = sorted(file_choices,reverse=True)
    return file_choices
