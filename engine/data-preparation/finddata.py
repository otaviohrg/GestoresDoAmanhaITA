# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a GGtemporary script file.
"""
import pandas as pd
import investpy

stockname = input()
df = investpy.get_stock_historical_data(stock=stockname,
                                        country='Brazil',
                                        from_date='01/02/2015',
                                        to_date='22/12/2020')
df = df.drop(["Currency"], axis=1)
df = df.rename({"Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"}, axis=1)
line = df.loc(pd.Timestamp("2020-11-20"))
print(line)
df.to_csv("data/daily/" + stockname + ".csv")