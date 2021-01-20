##------------Importanto bibliotecas-------------------------##
import pandas as pd
import sqlite3

#-------------CRIANDO A CONEXÃO COM O BANCO DE DADOS----------##

# LOCAL DA PASTA ONDE SE ENCONTRA O ARQUIVO SQLITE
path = r'/home/otaviohrg/GestoresDoAmanhaITA/engine'

# NOME DO ARQUIVO SQLITE BAIXADO
db = input('BOLSA ou MOEDA:')
conexao = sqlite3.connect(path + r'/' + db + '.db')
cursor = conexao.cursor()

#PRINTANDO AS TABELAS PRESENTES NO BANCO DE DADOS DO ARQUIVO SELECIONADO:

print('\n\nAs tabelas presentes no banco de dados são:\n')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

tabela = input('\n Digite a tabela que deseja transformar em dataframe pandas:\n')

# TRANSFORMANDO O ARQUIVO SQLITE EM DATAFRAME PANDAS
df = pd.read_sql_query("SELECT * FROM "+tabela , conexao)
print(df.head())
#OBS: PARA EXTRAIR OS DADOS DE CADA TABELA BASTA COPIAR E COLAR NO DIRETÓRIO O NOME DA TABELA DESEJADA

for tag in df[df.columns[0]].unique():
	tagdf = df.loc[df[df.columns[0]] == tag]
	tagdf = tagdf.drop(['SYMB'], axis=1)
	tagdf = tagdf.rename(columns={"DATA_OP": "date", "MKT_OPEN": "open", "HIGH": "high", "LOW": "low", "MKT_CLOSE": "close", "VOLUME": "volume", "DIVIDEND_AMOUNT": "dividend", "SPLIT_COEFICIENT": "split"})
	tagdf.to_csv('/home/otaviohrg/GestoresDoAmanhaITA/engine/data/' + db + '/' + tabela + '/' + tag +'.csv', index=False)
