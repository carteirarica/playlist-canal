import streamlit as st
import numpy as np
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt


import os
files = [f for f in os.listdir('.')]
for f in files:
    st.write(f)


# Importação de dados
simbolos = pd.read_pickle('data/simbolos')
brasil = pd.read_pickle('data/brasil')
nas = pd.read_pickle('data/nasdaq')
sp = pd.read_pickle('data/spx')


# Funções
def get_gain(frame, delta=pd.DateOffset(days=30)):
    retornos = []
    for col in frame.columns:
        init_val = frame[col].dropna().iloc[0]
        day_fut = pd.to_datetime(frame[col].dropna().index[0]) + delta
        dfut_idx = frame.index.get_loc(day_fut, method='nearest')
        dfut_val = frame[col].iloc[dfut_idx]
        gain = (dfut_val/init_val-1)*100
        # print(init_val)
        # print(d30_idx)
        # print(gain)
        # print(d30_val)
        if day_fut > date.today():  # se o IPO é recente, pula para a próxim execução e não add o ganho
            continue
        retornos.append((col, round(gain, 2)))
    return retornos


mes = pd.DateOffset(days=30)
ano = pd.DateOffset(days=364)

retornos = get_gain(brasil, delta=mes)
ret_30 = pd.DataFrame(retornos, columns=["ativo", "retorno"])
anual = get_gain(brasil, delta=ano)
ret_ano = pd.DataFrame(anual, columns=["ativo", "retorno"])

# Visual

st.title('IPO - Estudos')
'---'
st.header('IPOs brasileiros desde 2016')
brasil
'---'

col1, col2 = st.beta_columns(2)

with col1:
    st.header('Estatísticas em 30 dias pós IPO:')
    ret_30
    st.markdown(f'''
    **{'{:,.2f}'.format(ret_30.retorno.mean())}** Retorno médio nos 1ºs 30d
    **{'{:,.2f}'.format(ret_30.retorno.median())}** Retorno mediano
    **{'{:,.2f}'.format(ret_30.retorno.std())}** Desvio padrão em 30d médio
    ''')

    st.header('Boxplot de retornos')
    fig, ax = plt.subplots()
    ax.boxplot(ret_30.retorno)
    st.pyplot(fig)

    st.header('Histograma de retornos')
    fig1, ax1 = plt.subplots()
    ax1.hist(ret_30.retorno)
    st.pyplot(fig1)
    '---'

with col2:
    st.header('Estatísticas em 1 ano pós IPO:')
    ret_ano
    st.markdown(f'''
    **{'{:,.2f}'.format(ret_ano.retorno.mean())}** Retorno médio no 1º ano
    **{'{:,.2f}'.format(ret_ano.retorno.median())}** Retorno mediano
    **{'{:,.2f}'.format(ret_ano.retorno.std())}** Desvio padrão 1º ano médio
    ''')

    st.header('Boxplot de retornos')
    fig2, ax2 = plt.subplots()
    ax2.boxplot(ret_ano.retorno)
    st.pyplot(fig2)

    st.header('Histograma de retornos')
    fig3, ax3 = plt.subplots()
    ax3.hist(ret_ano.retorno)
    st.pyplot(fig3)

'---'
st.title('EUA')
st.header('Tabela IPOs Nasdaq')
nas
st.header('SP500')
st.write('Retorno SP500 no período similar: {:,.2f}'.format(
    (sp.iloc[-1]['adj close']/sp.iloc[0]['adj close']-1)*100))
st.line_chart(sp.close)
'---'

'## Nasdaq'
nas30 = nas.day30.dropna()
'Média de ganho em 30 dias'
st.write(nas30.mean())
'Mediana de ganho em 30 dias'
st.write(nas30.median())

st.header('Boxplot de retornos 30d')
fig4, ax4 = plt.subplots()
ax4.boxplot(nas30)
st.pyplot(fig4)

st.header('Histograma de retornos 30d')
fig1, ax1 = plt.subplots()
ax1.hist(nas30)
st.pyplot(fig1)
'---'
