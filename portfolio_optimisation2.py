from lib2to3.pytree import Base
from tkinter import *


class portfolio_optimization:
    def __init__(self, assets, money_to_be_invested):
        import yfinance as yf
        import pandas as pd
        from datetime import datetime
        self.stock_owning_limit = 2000
        self.stocks_and_limits = {'FB': 200, 'AMZN': 50, 'AAPL': 70, 'NFLX': 80, 'GOOG': 120}

        self.dummy_assets = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG']
        print(f"dummy assets:{self.dummy_assets}")
        label = Label(window)
        ###################
        self.assets = assets
        self.money_to_be_invested = money_to_be_invested
        ###################
        # self.assets = input(
        #     "Enter the symbols of the companies you want to invest in:\nYou may choose from list above\n").split()
        # self.money_to_be_invested = int(input("Enter the money to invest\n"))
        stocksStartDate = '2013-01-01'
        today = datetime.today().strftime('%Y-%m-%d')
        self.all_stocks = pd.DataFrame()
        for symbol in self.assets:
            tmp_close = yf.download(symbol,
                                    start=stocksStartDate,
                                    end=today,
                                    progress=False)['Close']
            self.all_stocks = pd.concat([self.all_stocks, tmp_close], axis=1)

        self.all_stocks.columns = self.assets
        self.b=[]

    def full_list_of_companies(self):
        import pandas as pd
        import csv
        dict_from_csv = {}
        with open('Top+2000+Valued+Companies+with+Ticker+Symbols.csv', mode='r') as inp:
             reader = csv.reader(inp)
             dict_from_csv = {rows[0]:rows[1] for rows in reader}
        comprehensive_list_of_companies=[]
        comprehensive_list_of_symbols=[]
        #print(dict_from_csv)

        # assets=[]
        for item, item2 in dict_from_csv.items():
             comprehensive_list_of_companies.append(item)
             comprehensive_list_of_symbols.append(item2)

        company_dict={"companies":comprehensive_list_of_companies,"symbols":comprehensive_list_of_symbols}
        Visual_list_of_companies=pd.DataFrame(company_dict)
        return(Visual_list_of_companies)
        #

    def stock_optimisation_trial_graph(self):
        import matplotlib.pyplot as plt
        title='portfolio Adj. Close Price History'
        for c in self.all_stocks.columns.values:
            plt.plot(self.all_stocks[c],label=c)
        plt.title(title)
        plt.xlabel('Date',fontsize=20)
        plt.ylabel('Adj.price USD ($)',fontsize=20)
        plt.legend(self.all_stocks.columns.values,loc='upper left')
        plt.show()

    def portfolio_optimisation(self):
        from pypfopt.efficient_frontier import EfficientFrontier
        from pypfopt import risk_models
        from pypfopt import expected_returns
        import pandas as pd

        #portfolio optimisation

        #Calculate the expected returns and the annualised covariance matrix of asset returns
        mu=expected_returns.mean_historical_return(self.all_stocks)
        print(mu)
        #s is the annualised covariance matrix
        s=risk_models.sample_cov(self.all_stocks)
        #efficient frontier is the set of optimal portfolios that offer the highest expected return for a defined level of risk
        # or the lowest risk for a given level of expected return
        ef=EfficientFrontier(mu,s)

        weights=ef.max_sharpe()
        #print(weights)

        cleaned_weights=ef.clean_weights()
        ef.portfolio_performance(verbose=True)

        from pypfopt.discrete_allocation import DiscreteAllocation,get_latest_prices
        latest_prices=get_latest_prices(self.all_stocks)

        allocation_of_funds=DiscreteAllocation(cleaned_weights, latest_prices,total_portfolio_value=self.money_to_be_invested)
        allocation, leftover=allocation_of_funds.lp_portfolio()
        companies=[]
        number_of_stocks=[]
        for company,no_of_stocks in allocation.items():
            companies.append(company)
            number_of_stocks.append(no_of_stocks)
        optimized_assets={"company":companies,"number of stocks":number_of_stocks}
        print("Below are is the optimized portfolio")


        return(pd.DataFrame(optimized_assets)), ('Funds remaining: ${:.2f}'.format(leftover))
        

    def knapsgack_implementation(self):
        from pypfopt.efficient_frontier import EfficientFrontier
        from pypfopt import risk_models
        from pypfopt import expected_returns

        from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
        weight_limits=[]
        for item in self.assets:
            if item in self.stocks_and_limits.keys():
                weight_limits.append(self.stocks_and_limits[item])
        latest_prices = get_latest_prices(self.all_stocks)
        mu = expected_returns.mean_historical_return(self.all_stocks)
        s = risk_models.sample_cov(self.all_stocks)
        ef = EfficientFrontier(mu, s)

        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()
        allocation_of_funds = DiscreteAllocation(cleaned_weights, latest_prices,
                                                 total_portfolio_value=self.money_to_be_invested)
        allocation, leftover = allocation_of_funds.lp_portfolio()
        companies = []
        number_of_stocks = []
        for company, no_of_stocks in allocation.items():
            companies.append(company)
            number_of_stocks.append(no_of_stocks)
        optimized_assets = {"company": companies, "number of stocks": number_of_stocks}
        self.knapsack_algorithm(self.stock_owning_limit,weight_limits,latest_prices,len(self.assets))
        return self.b

    def knapsack_algorithm(self,W, wt, val, n):
            K = [[0 for w in range(W + 1)]
                 for i in range(n + 1)]
            for i in range(n + 1):
                for w in range(W + 1):
                    if i == 0 or w == 0:
                        K[i][w] = 0

                    elif wt[i - 1] <= w:
                        K[i][w] = max(val[i - 1]
                                      + K[i - 1][w - wt[i - 1]],
                                      K[i - 1][w])
                    else:
                        K[i][w] = K[i - 1][w]


            max_value = K[n][W]
            print(max_value)
            w = W
            for i in range(n, 0, -1):
                if max_value <= 0:
                    break
                if max_value == K[i - 1][w]:
                    continue
                else:
                    self.b.append(wt[i - 1])
                    max_value = max_value - val[i - 1]
                    w = w - wt[i - 1]

    

# if '__main__'==__name__:
#     sample_optimisation=portfolio_optimization()
    # sample_optimisation.full_list_of_companies()
    # sample_optimisation.stock_optimisation_trial_graph()
    # sample_optimisation.portfolio_optimisation()
    # sample_optimisation.gui()
    #sample_optimisation.knapsack_implementation()


def gui():

    def implement():
        input1Value=input1.get("1.0","end-1c")
        input2Value=int(input2.get("1.0","end-1c"))
        sample_optimisation=portfolio_optimization(input1Value, input2Value)
        result1 = sample_optimisation.full_list_of_companies()
        sample_optimisation.stock_optimisation_trial_graph()
        result2 = sample_optimisation.portfolio_optimisation()        
        try:
            text.insert(INSERT, result2)
        except BaseException as error:
            print(error)
            print (result2)

    window = Tk()
    window.geometry('700x500')
    window.maxsize(700, 500)
    window.title('Portofolio Optimization')
    labelmain = Label(window, text= 'Welcome to our portofolio optimization programme')
    labelmain.pack()
    labelinf = Label(window, text = 'Examples of the assests are : test test test test')
    labelinf.place(relx = .3333, rely=.1)
    input1=Text(window, height=1, width=40)
    input1.place(relx = .5, rely=.2)
    label01 = Label(window, text = 'Please Enter the first input - assets:')
    label01.place(relx = .1, rely=.2)
    labelinf2 = Label(window, text = 'Examples of the money_to_be_invested are : test test test test')
    labelinf2.place(relx = .3333, rely=.3)
    input2=Text(window, height=1, width=40)
    input2.place(relx = .5, rely=.4)
    label02 = Label(window, text = 'Please Enter the seocnd input - money_to_be_invested:')
    label02.place(relx = .08, rely=.4)
    #If it gave error try to put prackects after implement like this --> implement()
    but = Button(window, text="Start", command= implement)
    but.place(x=0, y=0)
    text = Text(window)
    text.place(rely = .5, relx=.05)
    # sample_optimisation.knapsack_implementation()
    window.mainloop()

gui()