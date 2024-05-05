import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date

sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
data_table = pd.read_html(sp500url)
correct_data_table = data_table[0]

sp500ticker = correct_data_table["Symbol"].tolist()


sp500_dividend_yield = []
sp500_beta = []
sp500_payoutratio = []
sp500_ROE = []
sp500_price = []
sp500_forwardeps = []
sp500_dividends = []
sp500_Adj_Close = []
sp500_number_of_shares = []
#todays_date = str(date.today())
todays_date = "2024-04-30"



for ticker in sp500ticker:
    x = yf.Ticker(ticker)
    data = x.info
    data_dt = pd.DataFrame([data])
    
    if "dividendYield" in data_dt.columns:
        sp500_dividend_yield.append(data_dt["dividendYield"].values[0])
    else:
        sp500_dividend_yield.append(None)
    
    if "beta" in data_dt.columns:
        sp500_beta.append(data_dt["beta"].values[0])
    else:
        sp500_beta.append(None)
    
    if "payoutRatio" in data_dt.columns:
        sp500_payoutratio.append(data_dt["payoutRatio"].values[0])
    else:
        sp500_payoutratio.append(None)
    
    if "returnOnEquity" in data_dt.columns:
        sp500_ROE.append(data_dt["returnOnEquity"].values[0])
    else:
        sp500_ROE.append(None)
    
    if "currentPrice" in data_dt.columns:
        sp500_price.append(data_dt["currentPrice"].values[0])
    else:
        sp500_price.append(None)
    if "forwardEps" in data_dt.columns:
        sp500_forwardeps.append(data_dt["forwardEps"].values[0])
    else:
        sp500_forwardeps.append(None)

for ticker in sp500ticker:
    price = yf.download(ticker, period="1d")

    if "Adj Close" in price.columns and not price.empty:
        # Append only the last adjusted close value as a float
        sp500_Adj_Close.append(price["Adj Close"].iloc[-1])
    else:
        sp500_Adj_Close.append(None)





list_of_tickers = []
for ticker in sp500ticker:
    list_of_tickers.append(ticker)


sp500_df = pd.DataFrame({'ticker': list_of_tickers, "price": sp500_Adj_Close, "forwardEps": sp500_forwardeps,  'DividentYield': sp500_dividend_yield, 'beta': sp500_beta, 'payoutRatio': sp500_payoutratio, 'returnOnEquity': sp500_payoutratio, "ones": 1, "ERP": 0.0413, "RF": 0.04626, "thousands": 1000})
sp500_df_clean = sp500_df.dropna()

pd.set_option('display.max_columns', None)


sp500_df_clean["f"] = sp500_df_clean["ones"] - sp500_df_clean["payoutRatio"]
sp500_df_clean["g"] = sp500_df_clean["f"] * sp500_df_clean["returnOnEquity"]
sp500_df_clean["dividend"] = sp500_df_clean["forwardEps"] * sp500_df_clean["payoutRatio"]
sp500_df_clean["investors_r"] = ((sp500_df_clean["dividend"])/ sp500_df_clean["price"]) + sp500_df_clean["g"]
sp500_df_clean["alfa"] = sp500_df_clean["investors_r"] - (sp500_df_clean["RF"] + (sp500_df_clean["beta"] * sp500_df_clean["ERP"]))
sp500_df_clean["number_of_shares"] = sp500_df_clean["thousands"] * sp500_df_clean["alfa"]

sp500_df_clean['buy/sell'] = np.where(sp500_df_clean['alfa'] > 0, 'buy', 'sell')
sp500_df_clean = sp500_df_clean[sp500_df_clean["alfa"] <0.5]
sp500_df_clean = sp500_df_clean[sp500_df_clean["alfa"] >-0.5]

buy = sp500_df_clean['buy/sell'].value_counts()

print(buy)

beta_values = np.linspace(0,4,1000)
risk_free_rate = 0.04626
equity_risk_premium = 0.0413
companies_beta = np.array(sp500_df_clean["beta"])
investors_r = np.array(sp500_df_clean["investors_r"])

expected_return = risk_free_rate + beta_values * equity_risk_premium

plt.plot(beta_values, expected_return, label="SML")
plt.title('Security Market Line (SML)')
plt.xlabel('Beta (Systematic Risk)')
plt.ylabel('Expected Return')

plt.scatter(companies_beta, sp500_df_clean["RF"] + sp500_df_clean["beta"] * sp500_df_clean["ERP"] + sp500_df_clean["alfa"], label="companies", s =3.5)

plt.legend()

plt.show()

pd.set_option('display.max_rows', None)

data_to_export = sp500_df_clean[["ticker", "price", "buy/sell", "number_of_shares"]]


data_to_export.to_csv("wytyczne_do_transakcji.csv", index=False)

