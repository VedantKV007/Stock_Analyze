import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_stock_data(ticker, period='1y'):
    try:
        stock_data = yf.download(ticker, period=period)
        if stock_data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        return stock_data
    except Exception as e:
        print(f"Error getting data: {e}")
        return None


def calculate_macd(stock_data, fast_period=12, slow_period=26):
    exp1 = stock_data['Close'].ewm(span=fast_period, adjust=False).mean()
    exp2 = stock_data['Close'].ewm(span=slow_period, adjust=False).mean()
    stock_data['MACD'] = exp1 - exp2
    return stock_data


def plot_indicators(stock_data, ticker):
    fig = make_subplots(rows=2, cols=1,
                         subplot_titles=(f'{ticker} Closing Price', f'{ticker} MACD'),
                         vertical_spacing=0.15)

    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'],
                             mode='markers', name='Closing Price',
                             marker=dict(size=5, color='blue'),
                             line=dict(color='blue', width=1)), row=1, col=1)

 
    stock_data['MACD_color'] = ['green' if macd >= 0 else 'red' for macd in stock_data['MACD']]

 
    fig.add_trace(go.Scatter(
        x=stock_data.index, 
        y=stock_data['MACD'],
        mode='lines',
        line=dict(color='rgba(0,255,255,0.5)', width=3),
        marker=dict(color=stock_data['MACD_color']),
        name="MACD",
    ), row=2, col=1)

 
    fig.add_shape(type="rect",
                  x0=stock_data.index[0], x1=stock_data.index[-1],
                  y0=10, y1=11,
                  fillcolor="rgba(255,0,0,0.2)",
                  line=dict(color="rgba(0, 0, 0, 0.2)", width=1),
                  row=2, col=1,
                  opacity=0.5,
                  xref='x2', yref='y2',
                  layer='below')

    fig.add_shape(type="rect",
                  x0=stock_data.index[0], x1=stock_data.index[-1],
                  y0=-11, y1=-10,
                  fillcolor="rgba(0,255,0,0.2)",
                  line=dict(color="rgba(0, 0, 0, 0.2)", width=1),
                  row=2, col=1,
                  opacity=0.5,
                  xref='x2', yref='y2',
                  layer='below')


    fig.update_layout(
        title=dict(
            text=f'{ticker} Stock Price and MACD',
            font=dict(size=28, color='white'),
            x=0.5, xanchor='center',
            y=0.98, yanchor='top'
        ),
        height=800,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(18, 20, 59, 0.96)',
        font=dict(color='white'),
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        hovermode='x unified',
        showlegend=False,
    )

    fig.show()

if __name__ == "__main__":
    ticker = input("Enter stock ticker symbol: ")
    stock_data = get_stock_data(ticker)
    if stock_data is not None:
        stock_data = calculate_macd(stock_data)
        plot_indicators(stock_data, ticker)
