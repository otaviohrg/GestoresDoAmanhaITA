#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 13:43:33 2021

@author: otaviohrg
"""

from zipline.api import order_target, record, symbol
import matplotlib.pyplot as plt
import pandas as pd
import zipline

def initialize(context):
    context.i = 0
    context.asset = symbol('MMM')


def handle_data(context, data):
    print(context.asset)
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 30:
        return

    # Compute averages
    # data.history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_mavg = data.history(context.asset, 'price', bar_count=10, frequency="1d").mean()
    long_mavg = data.history(context.asset, 'price', bar_count=30, frequency="1d").mean()

    # Trading logic
    if short_mavg > long_mavg:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target(context.asset, 100)
    elif short_mavg < long_mavg:
        order_target(context.asset, 0)

    # Save values for later inspection
    record(MMM=data.current(context.asset, 'price'),
           short_mavg=short_mavg,
           long_mavg=long_mavg)
           
           
def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')

    ax2 = fig.add_subplot(212)
    perf['MMM'].plot(ax=ax2)
    perf[['short_mavg', 'long_mavg']].plot(ax=ax2)

    perf_trans = perf.ix[[t != [] for t in perf.transactions]]
    buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.ix[
        [t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax2.plot(buys.index, perf.short_mavg.ix[buys.index],
             '^', markersize=10, color='m')
    ax2.plot(sells.index, perf.short_mavg.ix[sells.index],
             'v', markersize=10, color='k')
    ax2.set_ylabel('price in $')
    plt.legend(loc=0)
    plt.show()
    df = pd.DataFrame(perf)
    df.to_csv("output-new.csv")
    
perf = zipline.run_algorithm(start = pd.Timestamp('2020-06-16 00:00:00+0000'),
                             end = pd.Timestamp('2020-11-04 00:00:00+0000'),
                             initialize=initialize,
                             analyze=analyze,
                             capital_base=100000,
                             handle_data = handle_data,
                             bundle = 'DAILY_ADJUSTED_TIME_SERIES')
