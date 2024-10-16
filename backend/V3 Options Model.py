from datetime import datetime, time
import yfinance as yf
import numpy as np
from scipy.stats import norm
import math
import pytz
import scipy.stats as si







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








def is_market_open():
    local_tz = pytz.timezone(pytz.country_timezones['US'][0])  
    now = datetime.now(local_tz)

    est_tz = pytz.timezone('US/Eastern')
    now_est = now.astimezone(est_tz)

    market_open_time = time(9, 30)
    market_close_time = time(16, 0)

    if (now_est.month, now_est.day) in US_MARKET_HOLIDAYS:
        return "Market closed for holiday."

    if now_est.weekday() >= 5:  
        return "Market closed for weekend."

    current_time = now_est.time()
    if current_time < market_open_time:
        return "Pre-market."
    elif current_time > market_close_time:
        return "Post-market."
    else:
        return "Market open."








def get_market_status():
    # Get the local timezone
    local_tz = pytz.timezone(pytz.country_timezones['US'][0])  # Assuming user is in the US
    now = datetime.now(local_tz)

    # Convert local time to EST
    est_tz = pytz.timezone('US/Eastern')
    now_est = now.astimezone(est_tz)

    market_open_time = datetime.combine(now_est.date(), time(9, 30), est_tz)
    market_close_time = datetime.combine(now_est.date(), time(16, 0), est_tz)

    status_message = is_market_open()

    if "closed" in status_message:
        return f"{status_message} Current time: {now_est.strftime('%I:%M %p')}"
    elif "Pre-market" in status_message:
        return f"Pre-market. Time until market opens: {market_open_time - now_est}"
    elif "Market open" in status_message:
        time_until_close = market_close_time - now_est
        hours, remainder = divmod(time_until_close.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"Market open. Time until market closes: {hours} hours, {minutes} minutes, {seconds} seconds"
    else:
        return f"Post-market. Current time: {now_est.strftime('%I:%M %p')}"








def initiate_check(ticker, strike_price, expiration_date, option_type):
    if not isinstance(ticker, str) or len(ticker) > 9 or not ticker or any(char.isdigit() for char in ticker):
        ticker_check = "Invalid ticker. Must be a non-empty string with a maximum length of 9 characters and cannot contain integers."
    else:
        ticker_check = "Valid"

    if not isinstance(strike_price, (int, float)) or strike_price < 0:
        strike_check = "Invalid strike price. Must be a positive number."
    else:
        strike_check = "Valid"

    if not isinstance(expiration_date, str):
        expiration_check = "Invalid expiration date. Must be a string in 'YYYY-MM-DD' format."
    else:
        try:
            expiration = datetime.strptime(expiration_date, '%Y-%m-%d')
            if expiration <= datetime.now():
                expiration_check = "Invalid expiration date. Must be a future date."
            else:
                expiration_check = "Valid"
        except ValueError:
            expiration_check = "Invalid expiration date format. Must be in 'YYYY-MM-DD' format."

    if option_type not in ["call", "put"]:
        type_check = "Invalid option type. Please enter 'call' or 'put'."
    else:
        type_check = "Valid"

    return ticker_check, strike_check, expiration_check, type_check













def black_scholes_call(S, K, T, r, sigma):
    """Calculate the Black-Scholes call option price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    return call_price

def black_scholes_put(S, K, T, r, sigma):
    """Calculate the Black-Scholes put option price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0))
    return put_price

def pull_data(ticker, strike_price, expiration_date, option_type):
    stock = yf.Ticker(ticker)

    results = {
        "Underlying Price": 0.0,
        "Bid": 0.0,
        "Ask": 0.0,
        "Spread": 0.0,
        "Volume": 0,
        "Open Interest": 0,
        "Implied Volatility (%)": 0.0,
        "Days Until Expiration": 0,
        "Black-Scholes Price": 0.0,
        "Valuation": "",
        "Price Discrepancy (%)": 0.0,
        "Opportunity Level": 0
    }

    if stock.options and expiration_date in stock.options:
        options = stock.option_chain(expiration_date)
        option_data = options.calls if option_type == "call" else options.puts
        strike_data = option_data[option_data['strike'] == float(strike_price)]

        if not strike_data.empty:
            results["Underlying Price"] = round(stock.history(period='1d')['Close'].iloc[-1], 2)
            bid = strike_data.iloc[0]['bid']
            ask = strike_data.iloc[0]['ask']
            results["Bid"] = round(bid, 2)
            results["Ask"] = round(ask, 2)
            results["Spread"] = round(ask - bid, 2)
            results["Volume"] = int(strike_data.iloc[0]['volume'])
            results["Open Interest"] = int(strike_data.iloc[0]['openInterest'])

            implied_volatility = strike_data.iloc[0]['impliedVolatility']
            results["Implied Volatility (%)"] = round(implied_volatility * 100, 2) if implied_volatility is not None else 0.0
            
            expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%d')
            current_date = datetime.now()
            days_until_expiration = (expiration_date_obj - current_date).days
            results["Days Until Expiration"] = days_until_expiration

            S = results["Underlying Price"]
            K = float(strike_price)
            T = days_until_expiration / 365
            r = 0.01  # Assumed risk-free rate
            sigma = implied_volatility

            bs_price = black_scholes_call(S, K, T, r, sigma) if option_type == "call" else black_scholes_put(S, K, T, r, sigma)
            results["Black-Scholes Price"] = round(bs_price, 2)

            if bid > bs_price:
                results["Valuation"] = "Overvalued"
                # Calculate price discrepancy as a percentage
                price_diff = (bid - bs_price) / bs_price * 100
                results["Price Discrepancy (%)"] = round(price_diff, 2)
            elif ask < bs_price:
                results["Valuation"] = "Undervalued"
                # Calculate price discrepancy as a percentage
                price_diff = (bs_price - ask) / bs_price * 100
                results["Price Discrepancy (%)"] = round(price_diff, 2)
            else:
                results["Valuation"] = "Fairly valued"
                results["Price Discrepancy (%)"] = 0.0  # No discrepancy if fairly valued

            # Determine opportunity level
            price_discrepancy = results["Price Discrepancy (%)"]
            if results["Valuation"] == "Undervalued":
                if price_discrepancy >= 50:
                    results["Opportunity Level"] = 3
                elif price_discrepancy >= 25:
                    results["Opportunity Level"] = 2
                elif price_discrepancy >= 10:
                    results["Opportunity Level"] = 1
                else:
                    results["Opportunity Level"] = 0  # Fairly valued
            elif results["Valuation"] == "Overvalued":
                if price_discrepancy >= 50:
                    results["Opportunity Level"] = 1
                elif price_discrepancy >= 25:
                    results["Opportunity Level"] = 2
                elif price_discrepancy >= 10:
                    results["Opportunity Level"] = 3
                else:
                    results["Opportunity Level"] = 0  # Fairly valued
            else:
                results["Opportunity Level"] = 0  # Fairly valued

    for key, value in results.items():
        if key == "Implied Volatility (%)":
            print(f"{key}: {value:.2f}%")
        elif key == "Black-Scholes Price":
            print(f"{key}: ${value:.2f}")
        else:
            print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")





















