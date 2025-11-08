import requests
import pandas as pd

# لینک API CoinGecko
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1&interval=hourly"
params = {
    "vs_currency": "usd",
    "days": "1",        # داده‌ی 1 روز گذشته
    "interval": "hourly"
}

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    # دیتای قیمت و زمان
    prices = data["prices"]         # هر آیتم: [timestamp, price]
    volumes = data["total_volumes"] # هر آیتم: [timestamp, volume]

    df = pd.DataFrame(prices, columns=["timestamp", "close"])
    df["volume"] = [v[1] for v in volumes]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')

    print(df)
    
except requests.exceptions.RequestException as e:
    print("خطا در اتصال به CoinGecko:", e)
    df = pd.DataFrame()  # دیتافریم خالی در صورت خطا

try:
    #محاسبه مکدی و آر اس آی و مووینگ اوریج
    df["EMA_short"]=df["close"].ewm(span=3,adjust=False).mean()
    df["EMA_long"]=df["close"].ewm(span=5,adjust=False).mean()

    delta=df["close"].diff()
    gain=delta.clip(lower=0)
    loss=-delta.clip(upper=0)
    avg_gain=gain.rolling(window=3).mean()
    avg_loss=loss.rolling(window=3).mean()
    rs=avg_gain/avg_loss
    df["RSI"]=100-(100/(1+rs))

    ema12=df["close"].ewm(span=12,adjust=False).mean()
    ema26=df["close"].ewm(span=26,adjust=False).mean()
    df["MACD"]=ema12-ema26
    df["MACD_signal"]=df["MACD"].ewm(span=9,adjust=False).mean()

except Exception as e:
    print("error in indicators",e)


#تولید سیگنال    
def generate_signal(row):
    if row["EMA_short"]>row["EMA_long"]and row["RSI"]<70 and row["MACD"]>row["MACD_signal"]:
        return "BUY"
    elif row["EMA_short"]<row["EMA_long"]and row["RSI"]>30 and row["MACD"]<row["MACD_signal"]:
        return "SELL"
    else:
        return "HOLD"

df["Signal"]=df.apply(generate_signal,axis=1)  #تابع روی ردیف ها اعمال میشه یعنی برای هر ساعت بررسی میکنه سیگنال چی باشه
print(df[["timestamp","close","Signal"]])

