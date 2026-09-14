#deploy da aplicação

import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

#funcao para carregar o dataset
#@st.cache
def get_data():
    data = pd.read_csv('data.csv')
    return data

#funcao para treinar o modelo
def train_model(data):
    #separando as features e o target
    X = data.drop('MEDV', axis=1)
    y = data['MEDV']

    #criando o modelo
    model = RandomForestRegressor()
    model.fit(X, y)

    return model

#criando o dataframe
data = get_data()

model = train_model(data)

#titulo da aplicação
st.title('DATA APP - Aplicação de Previsão de Preços de Imóveis da cidade de Boston')

#descricao
st.markdown("Este é um dashboard interativo que permite explorar os dados de preços de imóveis da cidade de Boston e fazer previsões com base em um modelo de aprendizado de máquina.")

#veriif ando o dataset
st.subheader('Selecionando apenas um pequeno conjunto de atribuos')

#atributos a serem exibidos
default_features = ['RM', 'PTRATIO', 'CRIM',  'MEDV']

#definindo atributos a partir de um multiselect
cols = st.multiselect('Selecione os atributos que deseja visualizar', data.columns.tolist(), default=default_features)

#mostrando os top10 registros
st.dataframe(data[cols].head(10))

#subtitulo
st.subheader('Distribuição de imóveis por preço')

#definindo a faixa de valores

faixa_preco = st.slider('Selecione a faixa de preço', float(data['MEDV'].min()), float(data['MEDV'].max()), (float(data['MEDV'].min()), float(data['MEDV'].max())))

#filtrando os dados

data_filtrada = data[(data['MEDV'].between(left=faixa_preco[0], right=faixa_preco[1]))]

#plotar a distribuição de preços
fig = px.histogram(data_filtrada, x='MEDV', nbins=100, title='Distribuição de preços de imóveis filtrados')
fig.update_layout(xaxis_title='Preço do imóvel (MEDV)', yaxis_title='Contagem', bargap=0.1)
fig.update_traces(marker_color='blue', opacity=0.7)
st.plotly_chart(fig)

#criando nossa barra lateral

st.sidebar.subheader('Faça sua previsão de preço de imóvel')

#mapeando os atributos do dataset para a barra lateral
RM = st.sidebar.slider('Número médio de quartos por habitação (RM)', float(data['RM'].min()), float(data['RM'].max()), float(data['RM'].mean()))
PTRATIO = st.sidebar.slider('Relação aluno-professor por cidade (PTRATIO)', float(data['PTRATIO'].min()), float(data['PTRATIO'].max()), float(data['PTRATIO'].mean()))
CRIM = st.sidebar.slider('Taxa de criminalidade per capita por cidade (CRIM)', float(data['CRIM'].min()), float(data['CRIM'].max()), float(data['CRIM'].mean()))
NOX = st.sidebar.slider('Concentração de óxidos nítricos (NOX)', float(data['NOX'].min()), float(data['NOX'].max()), float(data['NOX'].mean()))
INDUS = st.sidebar.slider('Proporção de acres de negócios não varejistas por cidade (INDUS)', float(data['INDUS'].min()), float(data['INDUS'].max()), float(data['INDUS'].mean()))
CHAS = st.sidebar.selectbox('Proximidade do rio Charles (CHAS)', [0, 1], index=0)

#botao de predicao
btn_predict = st.sidebar.button('Prever preço do imóvel')

if btn_predict:
    #criando um dataframe com os valores selecionados
    input_data = pd.DataFrame({'CRIM': [CRIM], 'INDUS': [INDUS], 'CHAS': [CHAS], 'NOX': [NOX], 'RM': [RM], 'PTRATIO': [PTRATIO]})
    
    #fazendo a previsão
    prediction = model.predict(input_data)
    
    #mostrando o resultado
    st.subheader(f'O preço previsto do imóvel é: ${prediction[0]*10000:,.2f}')