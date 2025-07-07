def generate_signal(trend):
    if trend == "uptrend":
        return "BUY"
    elif trend == "downtrend":
        return "SELL"
    return "HOLD"