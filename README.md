# 📊 Crypto Signal Scanner | اسکنر سیگنال کریپتو

A Python script that fetches cryptocurrency prices from CoinGecko, calculates key technical indicators (EMA, RSI, MACD), and generates simple BUY / SELL / HOLD signals.

اسکریپتی در پایتون که قیمت ارزهای دیجیتال را از CoinGecko دریافت می‌کند، اندیکاتورهای کلیدی EMA، RSI و MACD را محاسبه می‌کند و سیگنال‌های ساده خرید / فروش / نگه‌داری ارائه می‌دهد.

---

## 🧠 Technologies Used | تکنولوژی‌های استفاده‌شده

- Python 3.10+  
- requests → برای دریافت داده‌ها از API  
- pandas / NumPy → پردازش و مدیریت داده‌ها  
- CoinGecko API → منبع داده‌های قیمتی  
- EMA, RSI, MACD → اندیکاتورهای تحلیل تکنیکال  

---

## ⚙️ How It Works | نحوه کار

1. Fetch hourly cryptocurrency prices from CoinGecko.  
2. Build a DataFrame with timestamp, close price, and volume.  
3. Calculate technical indicators (**EMA short & long, RSI, MACD**).  
4. Generate simple trading signals (**BUY / SELL / HOLD**) for each hour.  
5. Output results in console or optionally save to CSV.

مراحل کار:  
1. دریافت داده‌های ساعتی از CoinGecko  
2. ساخت DataFrame شامل ستون‌های زمان، قیمت و حجم  
3. محاسبه اندیکاتورهای تکنیکال (**EMA کوتاه و بلند، RSI و MACD**)  
4. تولید سیگنال‌های ساده خرید / فروش / نگه‌داری برای هر ساعت  
5. نمایش نتیجه در کنسول یا ذخیره در فایل CSV

---

## 🧩 Key Code Structure | ساختار اصلی کد

```python

df["EMA_short"] = df["close"].ewm(span=3, adjust=False).mean()
df["EMA_long"]  = df["close"].ewm(span=5, adjust=False).mean()

df["RSI"] = compute_rsi(df["close"], period=3)

df["MACD"], df["MACD_signal"] = compute_macd(df["close"])


def generate_signal(row):
    if row["EMA_short"] > row["EMA_long"] and row["RSI"] < 70 and row["MACD"] > row["MACD_signal"]:
        return "BUY"
    elif row["EMA_short"] < row["EMA_long"] and row["RSI"] > 30 and row["MACD"] < row["MACD_signal"]:
        return "SELL"
    else:
        return "HOLD"

df["Signal"] = df.apply(generate_signal, axis=1)
print(df[["timestamp","close","Signal"]])

