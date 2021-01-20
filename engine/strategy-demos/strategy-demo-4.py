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
    context.i = 0
    pass

def handle_data(context, data):
    context.i += 1
    if context.i < 300:
        return
    order(symbol('PETR4'), 10)
    record(PETR4=data.current(symbol('PETR4'), 'price'))
    

perf = zipline.run_algorithm(start = pd.Timestamp('2015-02-02 00:00:00+0000'),
                             end = pd.Timestamp('2020-12-22 00:00:00+0000'),
                             initialize=initialize,
                             capital_base=100000,
                             handle_data = handle_data,
                             bundle = 'custom-csvdir-bundle')

ax1 = plt.subplot(211)
perf.portfolio_value.plot(ax=ax1)
ax1.set_ylabel('Portfolio Value')
ax2 = plt.subplot(212, sharex=ax1)
perf.PETR4.plot(ax=ax2)
ax2.set_ylabel('PETR4 Stock Price')
plt.show()
df = pd.DataFrame(perf)
df.to_csv("output_4.csv")
