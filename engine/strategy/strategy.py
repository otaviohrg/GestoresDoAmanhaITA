#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 18:26:54 2020

@author: otaviohrg
"""

from zipline.api import order, record, symbol, set_benchmark
import zipline
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


def initialize(context):
    pass

def handle_data(context, data):
    order(symbol('ABBV'), 10)
    order(symbol('ABMD'), 10)
    order(symbol('ABT'), 10)
    order(symbol('ACN'), 10)
    order(symbol('MMM'), 10)
    record(ABBV=data.current(symbol('ABBV'), 'price'),
            ABMD=data.current(symbol('ABMD'), 'price'),
            ABT=data.current(symbol('ABT'), 'price'),
            ACN=data.current(symbol('ACN'), 'price'),
            MMM=data.current(symbol('MMM'), 'price'))
    

perf = zipline.run_algorithm(start = pd.Timestamp('2020-06-16 00:00:00+0000'),
                             end = pd.Timestamp('2020-11-04 00:00:00+0000'),
                             initialize=initialize,
                             capital_base=100000,
                             handle_data = handle_data,
                             bundle = 'DAILY_ADJUSTED_TIME_SERIES')

ax1 = plt.subplot(211)
perf.portfolio_value.plot(ax=ax1)
ax1.set_ylabel('Portfolio Value')
ax2 = plt.subplot(212, sharex=ax1)
perf.ABBV.plot(ax=ax2)
ax2.set_ylabel('ABBV Stock Price')
plt.show()
