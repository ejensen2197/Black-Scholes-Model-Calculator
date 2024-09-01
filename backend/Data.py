#V1 comparitive options valuation model ...
#all comments are added under relevant lines
#all financial data is fetched from yahoo finance
#possible Alpha Vantage API usage for partial usage 

                               
# -----------------------------------------------

#from flask import Flask, request, jsonify, session
#app = Flask(__OptionsPricingModel__)
#app.secret_key = 'your_secret_key'  # Required for session management
#for later?^

import yfinance as yf
#market data provider
import numpy as np
from scipy.stats import norm
#cumulative distrobution function ('norm.cdf') for Black-Scholes formula
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
#data visualization

def BlackScholes(S,K,T,r, sigma, OptionType="call"):
    #S: Current underlying stock price
    #K: Strike price
    #T: Time to expiration (years)
    #r: Risk free interst rate
    #Sigma: Volatility of the underlying asset
    #OptionType: Call or Put

    
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    
    if option_type == "call":
        return (S * norm_cdf(d1)) - (K * math.exp(-r * T) * norm_cdf(d2))
    elif option_type == "put":
        return (K * math.exp(-r * T) * norm_cdf(-d2)) - (S * norm_cdf(-d1))

def norm_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
    #Cumulative distribution function for the standard normal distribution

def fetch_option_data(ticker, strike_price, expiration_date, option_type):
    #User enters Ticker, Strike, Exporation, option type
    #Fetch option data from Yahoo Finance based on the option type (call/put).

    stock = yf.Ticker(ticker)
    
    if not stock.options:
        return "No options available for this ticker.", None
    # Check if the ticker has options available at all

    
    if expiration_date not in stock.options:
        return f"Invalid expiration date: {expiration_date}. Available dates: {stock.options}", None
    # Validate the expiration date

    try:
        options = stock.option_chain(expiration_date)
    except Exception as e:
        return f"Error retrieving options chain: {str(e)}", None
    
    if option_type == "call":
        option_data = options.calls[options.calls['strike'] == float(strike_price)]

    if option_data.empty:
        return f"No {option_type} options available for the given strike price: {strike_price}.", None
    # Check if the strike price exists in the option chain


    elif option_type == "put":
        option_data = options.puts[options.puts['strike'] == float(strike_price)]
    # Filter the options based on the strike price and option type

    

    
    option_bid_ask = {
        "bid": option_data.iloc[0]['bid'],
        "ask": option_data.iloc[0]['ask'],
        "bid_size": option_data.iloc[0]['bidSize'],
        "ask_size": option_data.iloc[0]['askSize']
    }
    #creates a dictionary called option_info containing the Bid/Ask data of the specified option 
    #It is assumed that ther eis only one row in option_data because the strike price is unique. .iloc[0] directly accesses this row 
    
    return None, option_bid_ask
    

    
    
    






