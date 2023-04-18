from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import BlogPostForm
from .models import StockData
import csv
import os
import pandas as pd
import numpy as np
from .models import StockData, BlogPost, Favorite
import plotly.graph_objs as go
from datetime import datetime
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(
                request, f"Account created successfully for {username}!")
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


def index(request):
    selected_date = '2023-03-16' #setting default date
    try:
        date_selected = request.GET.get('selected_date')
        date_obj = datetime.strptime(date_selected, '%m/%d/%Y')
        selected_date = date_obj.strftime('%Y-%m-%d')
    except:
        pass
    print(selected_date)
    stocks = None  # Initialize stocks variable to None
    if selected_date:
        csv_file = os.path.join('static/data', f'{selected_date}.csv')
        if os.path.isfile(csv_file):  # Check if file exists
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
            # Create new objects from CSV data
            StockData.objects.bulk_create([StockData(**item) for item in data])
            stocks = StockData.objects.all()
            paginator = Paginator(stocks, 25)  # Limiting to 25 stocks per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'index.html', {'page_obj': page_obj, 'selected_date': selected_date})
        else:
            error_message = f"Data not found for {selected_date}"
            # Render the template with the error message
            return render(request, 'index.html', {'error_message': error_message})
    
    return render(request, 'index.html', {'selected_date': selected_date})


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

    # create a Paginator object with stock data and 10 items per page
    paginator = Paginator(stock_data, 10)

    # get the current page number from the query string, default to 1
    page_number = request.GET.get('page', 1)

    # get the Page object for the current page
    page_obj = paginator.get_page(page_number)

    # pass the Page object and symbols to the template
    context = {'page_obj': page_obj,
               'stock_names': symbols, 'selected_stock': stock}
    return render(request, 'stocks.html', context)


def predictions(request):
    symbols = get_symbol_list()
    stock = request.POST.get('stock', 'ADBL')

    # Load the model
    model_path = os.path.join('static', 'models', stock + '.h5')
    if os.path.exists(model_path):
        model = load_model(model_path)
    else:
        return render(request, 'predictions.html', {'message': 'Model not found'})

    # Load the data
    data_path = os.path.join('static', 'individual', stock + '.csv')
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        return render(request, 'predictions.html', {'message': 'Data not found'})

    closedf = df.reset_index()['Close']
    scaler = MinMaxScaler(feature_range=(0,1))
    df1 = scaler.fit_transform(np.array(closedf).reshape(-1,1)) 
    recent_data = df1[-60:]

    # Reshape the data for the LSTM model
    x_recent = recent_data.reshape(1, 1, 60)

    # Predict the stock prices for the next day and append to the input data
    predicted_price = model.predict(x_recent)
    df1 = np.append(df1, predicted_price)

    # Shift the input data by one day
    for i in range(6):
        recent_data = df1[-60:]
        x_recent = recent_data.reshape(1, 1, 60)
        predicted_price = model.predict(x_recent)
        df1 = np.append(df1, predicted_price)
        
    # Inverse transform the predicted prices
    predicted_prices = scaler.inverse_transform(df1[-7:].reshape(-1, 1))

    # Add the predicted prices to the dataframe
    last_date = pd.to_datetime(df['Date'].max())
    pred_dates = pd.date_range(last_date, periods=8, freq='D')[1:]
    pred_df = pd.DataFrame({'Date': pred_dates, 'Close': predicted_prices.ravel()})
    df = pd.concat([df, pred_df], ignore_index=True)

    # Generate the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Close'], name='Predicted Prices', mode='lines+markers'))

    fig.update_layout(
        title=f'{stock} Stock Prices Prediction',
        xaxis_title='Date',
        yaxis_title='Price',
    )

    fig.update_yaxes(range =[df['Close'].min()-10, df['Close'].max()+10])
    fig.update_xaxes(tickformat="%d")

    plot_div = fig.to_html(full_html=False)

    return render(request, 'predictions.html', {'plot_div': plot_div, 'stock_names': symbols, 'selected_stock': stock})


def analysis(request):
    symbols = get_symbol_list()
    stock = request.POST.get('stock', 'ADBL')  # ADBL is default

    file_path = os.path.join('static', 'individual', f'{stock}.csv')
    data = pd.read_csv(file_path)

    # Convert the Date column to a datetime format
    data['Date'] = data['Date'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y'))

    # Set the Date column as the index of the DataFrame
    data.set_index('Date', inplace=True)

    # Resample the data to the desired time frame and aggregate the High, Low, and Close values
    #also filtering out the date range because NEPSE was closed due to covid
    resampled_data = data.loc[(data.index < '2020-04-01') | (data.index > '2020-05-12')].resample('D').agg({'High': 'max', 'Low': 'min', 'Close': 'last'})

    # Calculate additional columns such as Moving Average, Bollinger Bands and Relative Strength Index (RSI) for the stock data
    resampled_data['MA'] = resampled_data['Close'].rolling(window=14, min_periods=1).mean()
    resampled_data['Delta'] = resampled_data['Close'].diff()
    resampled_data['Gain'] = resampled_data['Delta'].apply(
        lambda x: x if x > 0 else 0)
    resampled_data['Loss'] = resampled_data['Delta'].apply(
        lambda x: abs(x) if x < 0 else 0)
    resampled_data['AvgGain'] = resampled_data['Gain'].rolling(
        window=14).mean()
    resampled_data['AvgLoss'] = resampled_data['Loss'].rolling(
        window=14).mean()
    resampled_data['RS'] = resampled_data['AvgGain'] / \
        resampled_data['AvgLoss']
    resampled_data['RSI'] = 100 - (100 / (1 + resampled_data['RS']))

    # Calculate Bollinger Bands
    resampled_data['std'] = resampled_data['Close'].rolling(window=14, min_periods=1).std()
    resampled_data['upper_band'] = resampled_data['MA'] + 2 * resampled_data['std']
    resampled_data['lower_band'] = resampled_data['MA'] - 2 * resampled_data['std']

    # Create the candlestick chart with the stock data and technical indicators
    # Moving Average plot with Bollinger Bands
    fig_ma = go.Figure(data=[go.Candlestick(x=resampled_data.index,
                                         high=resampled_data['High'],
                                         low=resampled_data['Low'],
                                         close=resampled_data['Close']),
                          go.Scatter(x=resampled_data.index, y=resampled_data['MA'], name='Moving Average', line_width=3),
                          go.Scatter(x=resampled_data.index, y=resampled_data['upper_band'], name='Upper Band'),
                          go.Scatter(x=resampled_data.index, y=resampled_data['lower_band'], name='Lower Band')])

    fig_ma.update_layout(xaxis_rangeslider_visible=False,
                    title=f'{stock} Trading Graph')

    # RSI plot
    fig_rsi = go.Figure(data=[go.Scatter(x=resampled_data.index, y=resampled_data['RSI'], name='RSI')])

    fig_rsi.update_layout(xaxis_rangeslider_visible=False,
                    title=f'{stock} RSI Graph')

    # Add dotted lines at RSI values of 30 and 70
    fig_rsi.add_shape(type="line",
                  x0=resampled_data.index[0], y0=30, x1=resampled_data.index[-1], y1=30,
                  line=dict(color="grey", width=1, dash="dot"))
    fig_rsi.add_shape(type="line",
                  x0=resampled_data.index[0], y0=70, x1=resampled_data.index[-1], y1=70,
                  line=dict(color="grey", width=1, dash="dot"))

    # Render the chart in the Django template
    context = {'ma_graph': fig_ma.to_html(full_html=False), 'rsi_graph': fig_rsi.to_html(full_html=False), 'stock_names': symbols, 'selected_stock': stock}
    return render(request, 'analysis.html', context)

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


def get_symbol_list():
    symbols = ['ADBL', 'MEGA', 'NABIL', 'NICA']
    return symbols


def profile(request):
    favorite_stocks = Favorite.objects.filter(user=request.user).values_list('stock__company_name', flat=True)
    context = {
        'user': request.user,
        'favorite_stocks': favorite_stocks,
    }
    return render(request, 'profile.html', context)