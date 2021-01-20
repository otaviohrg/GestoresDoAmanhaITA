#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 13:43:33 2021

@author: otaviohrg
"""

from zipline.api import order_target, record, symbol, symbols
import matplotlib.pyplot as plt
import pandas as pd

def initialize(context):
    context.i = 0
    context.assets = symbols('PETR4', 'MGLU3', 'ABEV3', 'GGBR4', 'ITUB4')


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return

    # Compute averages
    # data.history() has to be called with the same params
    # from above and returns a pandas dataframe.
    for asset in context.assets:
        short_mavg = data.history(asset, 'price', bar_count=100, frequency="1d").mean()
        long_mavg = data.history(asset, 'price', bar_count=300, frequency="1d").mean()

        # Trading logic
        if short_mavg > long_mavg:
            # order_target orders as many shares as needed to
            # achieve the desired number of shares.
            order_target(asset, 100)
        elif short_mavg < long_mavg:
            order_target(asset, 0)

        # Save values for later inspection
        record(**{
            asset.symbol: data.current(asset, 'price'),
            asset.symbol + "short_mavg": short_mavg,
            asset.symbol + "long_mavg": long_mavg
        })


def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')

    ax2 = fig.add_subplot(212)
    perf['PETR4'].plot(ax=ax2)
    perf[['PETR4short_mavg', 'PETR4long_mavg']].plot(ax=ax2)

    perf_trans = perf.ix[[t != [] for t in perf.transactions]]
    buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.ix[
        [t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax2.plot(buys.index, perf.PETR4short_mavg.ix[buys.index],
             '^', markersize=10, color='m')
    ax2.plot(sells.index, perf.PETR4short_mavg.ix[sells.index],
             'v', markersize=10, color='k')
    ax2.set_ylabel('price in $')
    plt.legend(loc=0)
    plt.show()
    df = pd.DataFrame(perf)
    df.to_csv("output-3.csv")
