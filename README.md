# automated-stock-portfolio
This is my first Python project. Its purpose is to divide companies from the S&P 500 index into two groups: undervalued and overvalued. Next, the program will execute buy/sell actions for stocks. The project maintains records of open positions and closed positions.

S&P500_stocks.py downloads information about each company in the S&P 500 index. The program then filters out companies that pay dividends. This filtering is essential because I use Gordon's model to calculate the rate of return. Next, I calculate Jensen's alpha for each remaining company. If alpha is greater than 0, we buy the stock; if alpha is lower than 0, we sell it. Therefore, S&P500_stocks.py provides information on which companies to buy and sell.

The second code, transactions_record.py, manages three CSV files: open_positions, closed_positions, and guideline for each day. This file is updated by S&P500_stocks.py. The program essentially checks if the guideline matches the open positions. For example, if we have an open long position for Apple stocks and today's guideline states that Apple stock should be sold because its alpha is lower than 0, the program will close the long position for Apple stock, record the open and close prices, and then open a new short position for Apple. It's as simple as that.

In this particulalr case I assumed risk free rate equals 4,626% and equity risk premium equals 4,13%.

If you want to ran this project on your own computer you have to create those 3 csv files and update the path to each of them in python codes.
