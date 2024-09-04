# -----------------------------------------------

#V1 comparative options valuation model ...
#all comments are added under relevant lines
#all financial data is fetched from yahoo finance
#possible Alpha Vantage API usage for partial usage
#VS and ChatGPT used for debugging
                     
#-----------------------------------------------

#from flask import Flask, request, jsonify, session
#app = Flask(__OptionsPricingModel__)
#app.secret_key = 'your_secret_key'  # Required for session management
#for later?^

# IMPORTS AND SETUP -----------------------------------------------

from datetime import datetime, time
import yfinance as yf
import numpy as np
from scipy.stats import norm
import math

def BlackScholes(S, K, T, r, sigma, OptionType="call"):
    # S: Current underlying stock price
    # K: Strike price
    # T: Time to expiration (years)
    # r: Risk free interest rate
    # sigma: Volatility of the underlying asset (implied volatility)
    # OptionType: Call or Put

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if OptionType == "call":
        return (S * norm.cdf(d1)) - (K * math.exp(-r * T) * norm.cdf(d2))
    elif OptionType == "put":
        return (K * math.exp(-r * T) * norm.cdf(-d2)) - (S * norm.cdf(-d1))


# US market holidays for 2024 (update as needed for future years)

US_MARKET_HOLIDAYS = {
    (1, 1),   # New Year's Day
    (1, 15),  # Martin Luther King Jr. Day
    (2, 19),  # Presidents' Day
    (4, 1),   # Good Friday
    (5, 27),  # Memorial Day
    (6, 19),  # Juneteenth National Independence Day
    (7, 4),   # Independence Day
    (9, 2),   # Labor Day
    (11, 28), # Thanksgiving Day
    (12, 25)  # Christmas Day
}

# VERIFY IF DURING MARKET HOURS AND NOT ON A HOLIDAY -----------------------------------------------

def is_market_open():
    # Market hours for the US stock market: 9:30 AM to 4:00 PM EST
    now = datetime.now()  # Get the current date and time
    if now.weekday() >= 5:  # Check if it's a weekend (Saturday or Sunday)
        return False, "Market closed for the weekend."
    if (now.month, now.day) in US_MARKET_HOLIDAYS:  # Check if it's a holiday
        return False, "Market closed for a holiday."
    return time(9, 30) <= now.time() <= time(16, 0), "Market open."  # Check if within market hours

# GET MARKET STATUS (PRE-MARKET, OPEN, AFTER-MARKET, OR CLOSED) -------------------------------------

def get_market_status():
    now = datetime.now()  # Get the current date and time
    market_open_time = datetime.combine(now.date(), time(9, 30))  # Market open time
    market_close_time = datetime.combine(now.date(), time(16, 0))  # Market close time
    
    is_open, status_message = is_market_open()  # Check if market is open
    
    if not is_open:  # If market is not open, return the status message
        return f"{status_message} Current time: {now.strftime('%I:%M %p')}", False
    elif now < market_open_time:  # If it's pre-market, calculate time until market opens
        return f"Pre-market. Time until market opens: {market_open_time - now}", False
    elif market_open_time <= now <= market_close_time:  # If market is open, calculate time until it closes
        return f"Market open. Time until market closes: {market_close_time - now}", True
    else:  # If it's after-market, return the current time
        return f"After-market. Current time: {now.strftime('%I:%M %p')}", False

# FETCH AND PREPARE OPTION DATA -----------------------------------------------

def fetch_option_data(ticker, strike_price, expiration_date, option_type):
    stock = yf.Ticker(ticker)  # Fetch the stock data using yfinance
    if not stock.options or expiration_date not in stock.options:  # Check if options are available for the ticker
        return f"No options available for {ticker} with expiration date {expiration_date}.", None
    
    # Get the option chain for the given expiration date
    options = stock.option_chain(expiration_date)
    
    # Select the option type (call or put) and filter by strike price
    option_data = options.calls if option_type == "call" else options.puts
    option_data = option_data[option_data['strike'] == float(strike_price)]
    if option_data.empty:  # Check if the strike price exists in the option chain
        return f"No {option_type} options available for the given strike price: {strike_price}.", None

    # Determine if the market is open or closed
    _, market_open = get_market_status()

    if market_open:  # If the market is open, fetch the current bid/ask and sizes
        bid = option_data.iloc[0]['bid']
        ask = option_data.iloc[0]['ask']
        bid_size = option_data.iloc[0]['bidSize']
        ask_size = option_data.iloc[0]['askSize']
        current_price = None  # Current price is not needed if market is open
    else:  # If the market is closed, fetch the last traded price
        bid, ask, bid_size, ask_size = None, None, None, None
        current_price = stock.history(period="1d")['Close'][0]

    # Extract implied volatility from the option data
    implied_volatility = option_data.iloc[0]['impliedVolatility']
    
    # Calculate the time to expiration in years
    expiration = datetime.strptime(expiration_date, '%Y-%m-%d')
    time_to_expiration = (expiration - datetime.now()).days / 365.0

    # Compile all the relevant option data into a dictionary
    return None, {
        "current_price": current_price,
        "strike_price": strike_price,
        "time_to_expiration": time_to_expiration,
        "implied_volatility": implied_volatility,
        "option_type": option_type,
        "bid": bid,
        "ask": ask,
        "bid_size": bid_size,
        "ask_size": ask_size
    }

# MAIN FUNCTION TO CALCULATE FAIR VALUE USING BLACK-SCHOLES MODEL -----------------------------------------------

def calculate_fair_value(ticker, strike_price, expiration_date, option_type, risk_free_rate):
    error, option_info = fetch_option_data(ticker, strike_price, expiration_date, option_type)
    if error:
        return error
    
    # Determine the price to use in the Black-Scholes model (current price if market is closed, or mid-price if open)
    S = option_info['current_price'] if option_info['current_price'] else (option_info['bid'] + option_info['ask']) / 2
    K = option_info['strike_price']
    T = option_info['time_to_expiration']
    sigma = option_info['implied_volatility']
    OptionType = option_info['option_type']
    
    # Calculate the fair value using the Black-Scholes model
    fair_value = BlackScholes(S, K, T, risk_free_rate, sigma, OptionType)
    
    # Return the calculated fair value along with other market details
    return {
        "fair_value": fair_value,
        "bid": option_info['bid'],
        "ask": option_info['ask'],
        "bid_size": option_info['bid_size'],
        "ask_size": option_info['ask_size'],
        "market_status": get_market_status()[0]
    }

# Calculate the fair value and print the results
option_data = calculate_fair_value(ticker, strike_price, expiration_date, option_type, risk_free_rate)
print(f"The fair value of the {option_type} option for {ticker} with strike price {strike_price} and expiration date {expiration_date} is: {option_data['fair_value']:.2f}")
if option_data['bid'] and option_data['ask']:
    print(f"Bid: {option_data['bid']}, Ask: {option_data['ask']}, Bid Size: {option_data['bid_size']}, Ask Size: {option_data['ask_size']}")
else:
    print(f"Last traded price: {option_data['fair_value']}")
print(f"Market Status: {option_data['market_status']}")

