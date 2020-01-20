import pandas as pd
import us_stock_sina as us
import time
import pdb

class track_ticker:
    def __init__(self):
        self.my_tick_list = ["BILI", "JD", "LK", "MOMO", "NVDA", "TCOM", "WDC", "WUBA", "XNET", "YY"]
        self.df_us = pd.read_csv(r"C:\Users\johnny\PycharmProjects\stock-github\us_stock_list1.csv")
        self.df_selected = pd.DataFrame(columns=['code', 'page'])
        for code in self.my_tick_list:
            self.add_ticker(code)
        print(self.df_selected)

    def add_ticker(self, ticker):
        df = self.df_us[self.df_us["symbol"] == ticker]
        if df.empty:
            print("symbol {} not found!!".format(ticker))
            return
        else:
            print("symbol {} exists".format(ticker))

        self.df_selected = self.df_selected.append({'code': ticker, 'page': df.iloc[0].page},
                                                   ignore_index=True)
        return

    def get_data(self):
        stock_info = []
        for row in self.df_selected.itertuples():
            jason_data = us.get_stock_us_page(row.page)
            for stock in jason_data:
                if stock["symbol"] == row.code:
                    stock_info.append(stock)

        for stock in stock_info:
            print(stock["cname"], stock["symbol"], stock["price"], stock["open"], stock["chg"])
        print("\n\n")

    def print_ticker(self):
        print(self.df_selected)

"""
1. read the stock list file.
2. add the tick and find the page number from stock list
3. if 
"""

if __name__ == "__main__":
    tracker = track_ticker()
    tracker.print_ticker()
    while True:
        tracker.get_data()
        time.sleep(10)
