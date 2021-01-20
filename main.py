from zipline.api import order, record, symbol, set_benchmark
from zipline.data.bundles.csvdir import csvdir_equities
from zipline.data.bundles import register
import zipline
import pandas as pd
from datetime import datetime
import argparse
from collections import OrderedDict
import pytz
import numpy as np
import sqlite3

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-i', '--ifile', type=str, required=True)
parser.add_argument('-l', '--label', type=str, required=True)
args = parser.parse_args()
args = vars(args)

path = args['ifile']
conexao = sqlite3.connect(path)
cursor = conexao.cursor()
tabela = args['label']
df = pd.read_sql_query("SELECT * FROM "+tabela, conexao)
print(df[df.columns[0]].unique())
tag = input("Choose symbol:")
df = df.loc[df[df.columns[0]] == tag]
df["DATA_OP"] = pd.to_datetime(df["DATA_OP"]+' '+df['HORA_OP']).dt.tz_localize('UTC')
df = df.drop(['SYMB', 'HORA_OP'], axis=1)
df = df.rename(columns={"DATA_OP": "date",
                        "MKT_OPEN": "open",
                        "HIGH": "high",
                        "LOW": "low",
                        "MKT_CLOSE": "close",
                        "VOLUME": "volume"})
df.to_csv('customcsv/minute/custom_try.csv', index=False)
