import yfinance as yf
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.models import Span
from bokeh.io import output_notebook


def get_stock_data(ticker, period='1y'):
    stock_data = yf.download(ticker, period=period)
    return stock_data

# Function to calculate RSI
def calculate_rsi(stock_data, period=14):
    delta = stock_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))
    return stock_data

#MACD
def calculate_macd(stock_data, fast_period=12, slow_period=26, signal_period=9):
    exp1 = stock_data['Close'].ewm(span=fast_period, adjust=False).mean()
    exp2 = stock_data['Close'].ewm(span=slow_period, adjust=False).mean()
    stock_data['MACD'] = exp1 - exp2
    stock_data['MACD_signal'] = stock_data['MACD'].ewm(span=signal_period, adjust=False).mean()
    return stock_data


def plot_indicators_bokeh(stock_data, ticker):

    price_fig = figure(x_axis_type='datetime', title=f"{ticker} Closing Price", height=300, width=800)
    price_fig.line(stock_data.index, stock_data['Close'], color='blue', legend_label='Closing Price')


    rsi_fig = figure(x_axis_type='datetime', title=f"{ticker} RSI", height=300, width=800)
    rsi_fig.line(stock_data.index, stock_data['RSI'], color='purple', legend_label='RSI')


    overbought = Span(location=70, dimension='width', line_color='red', line_dash='dashed', line_width=2)
    oversold = Span(location=30, dimension='width', line_color='green', line_dash='dashed', line_width=2)
    rsi_fig.add_layout(overbought)
    rsi_fig.add_layout(oversold)


    macd_fig = figure(x_axis_type='datetime', title=f"{ticker} MACD", height=300, width=800)
    macd_fig.line(stock_data.index, stock_data['MACD'], color='blue', legend_label='MACD')
    macd_fig.line(stock_data.index, stock_data['MACD_signal'], color='orange', legend_label='Signal Line')


    output_file("stock_chart.html")
    

    show(column(price_fig, rsi_fig, macd_fig))

if __name__ == "__main__":
    ticker = input("Enter stock ticker symbol: ")
    stock_data = get_stock_data(ticker)
    stock_data = calculate_rsi(stock_data)
    stock_data = calculate_macd(stock_data)
    plot_indicators_bokeh(stock_data, ticker)
