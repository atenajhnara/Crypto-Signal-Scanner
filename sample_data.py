import pandas as pd

# ------------------------------
# 1️⃣ دیتای نمونه (در صورت عدم دسترسی به API)
# ------------------------------
data = [
    ["2025-09-23 12:00", 64000, 64500, 63800, 64200, 100],
    ["2025-09-23 13:00", 64200, 64600, 64100, 64400, 120],
    ["2025-09-23 14:00", 64400, 64800, 64300, 64700, 110],
    ["2025-09-23 15:00", 64700, 65000, 64600, 64900, 130],
    ["2025-09-23 16:00", 64900, 65200, 64800, 65100, 125],
]

df = pd.DataFrame(data, columns=["timestamp","open","high","low","close","volume"])

# اضافه کردن ستون نام ارز
df["Symbol"] = "BTC"

# ------------------------------
# 2️⃣ محاسبه اندیکاتورها با try/except
# ------------------------------
try:
    # EMA کوتاه و بلند
    df["EMA_short"] = df["close"].ewm(span=3, adjust=False).mean()
    df["EMA_long"] = df["close"].ewm(span=5, adjust=False).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=3).mean()
    avg_loss = loss.rolling(window=3).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

except Exception as e:
    print("خطا در محاسبه اندیکاتورها:", e)

# ------------------------------
# 3️⃣ تابع تولید سیگنال ساده
# ------------------------------
def generate_signal(row):
    try:
        if row["EMA_short"] > row["EMA_long"] and row["RSI"] < 70 and row["MACD"] > row["MACD_signal"]:
            return "BUY"
        elif row["EMA_short"] < row["EMA_long"] and row["RSI"] > 30 and row["MACD"] < row["MACD_signal"]:
            return "SELL"
        else:
            return "HOLD"
    except:
        return "ERROR"

df["Signal"] = df.apply(generate_signal, axis=1)

# ------------------------------
# 4️⃣ نمایش خروجی نهایی
# ------------------------------
print(df[["timestamp","Symbol","close","EMA_short","EMA_long","RSI","MACD","MACD_signal","Signal"]])