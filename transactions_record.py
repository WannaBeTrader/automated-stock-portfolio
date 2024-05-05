import numpy as np
import pandas as pd


odczyt=pd.read_csv("/Users/michal2/Desktop/wytyczne_do_transakcji.csv")
otwarte_pozycje=pd.read_csv("/Users/michal2/Desktop/otwarte_pozycje.csv")
closed_transactions=pd.read_csv("/Users/michal2/Desktop/closed_positions.csv")

otwarte_pozycje["rate_of_return_in_percentages"] = (odczyt["price"]/otwarte_pozycje["opening_price"]-1)/100
merged_df = pd.merge(otwarte_pozycje, odczyt, on='ticker', how='outer', suffixes=('_open', '_daily'))


for index, row in merged_df.iterrows():
    ticker = row['ticker']
    opening_price = row['opening_price']
    long_short = row['long_short'] if row['long_short'] else "None"
    current_price = row['price']
    buy_sell = row['buy/sell']
    number_of_shares = row['number_of_shares_open'] if row['number_of_shares_open'] else "None"
    number_of_shares_daily= row['number_of_shares_daily'] if row['number_of_shares_daily'] else "None"

    if pd.isnull(long_short):  # Check if position doesn't exist
        # Add new position
        long_short = 'Long' if buy_sell == 'buy' else 'short'
        new_position = pd.DataFrame({
            'ticker': [ticker],
            'opening_price': [current_price],
            'long_short': [long_short],
            'number_of_shares': [number_of_shares_daily]
        })
        otwarte_pozycje = pd.concat([otwarte_pozycje, new_position], ignore_index=True)

    if long_short == 'long' and buy_sell == 'sell':
        new_long_short = 'short'
        closed_transaction = pd.DataFrame({
            'ticker': [ticker],
            'opening_price': [opening_price],
            'closing_price': [current_price],
            'long_short': [long_short],
            'number_of_shares': [number_of_shares]
        })
        closed_transactions = pd.concat([closed_transactions, closed_transaction], ignore_index=True)
        otwarte_pozycje.loc[otwarte_pozycje['ticker'] == ticker, ['long_short', 'opening_price']] = [new_long_short, current_price]

    if long_short == 'short' and buy_sell == 'buy':
        new_long_short = 'long'
        closed_transaction = pd.DataFrame({
            'ticker': [ticker],
            'opening_price': [opening_price],
            'closing_price': [current_price],
            'long_short': [long_short],
            'number_of_shares': [number_of_shares]
        })
        closed_transactions = pd.concat([closed_transactions, closed_transaction], ignore_index=True)
        otwarte_pozycje.loc[otwarte_pozycje['ticker'] == ticker, ['long_short', 'opening_price']] = [new_long_short, current_price]

closed_transactions["rate_of_return_in_percentages"]=(closed_transactions["closing_price"]/closed_transactions["opening_price"]-1) * 100

print("Aktualne pozycje po zmianach:")
print(otwarte_pozycje)
print("\nZamknięte transakcje:")
print(closed_transactions)

otwarte_pozycje.to_csv('otwarte_pozycje.csv', index=False)
closed_transactions.to_csv('closed_positions.csv', index=False)


