#carregando a base

import pandas as pd

link = 'https://ocw.mit.edu/courses/15-071-the-analytics-edge-spring-2017/d4332a3056f44e1a1dec9600a31f21c8_boston.csv'

data = pd.read_csv(link)

#converterndo type da coluna RM

data['RM'] = data['RM'].astype(int)

#removendo as colunas irrelevants

data = data.drop(columns=['TOWN','TRACT', 'LAT', 'LON', 'RAD', 'TAX', 'DIS', 'AGE', 'ZN'])

data.to_csv('data.csv', index=False)