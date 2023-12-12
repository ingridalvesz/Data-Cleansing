import pandas as pd
import json

dados_churn = pd.read_json('dataset-telecon.json')
dados_churn.head()
# ler os dados .read_json('') e observar as 5 primeiras linhas dos dados com o .head()


dados_churn['conta'][0]

pd.json_normalize(dados_churn['conta']).head()
# para normalizar a visualização dos dados usomos o .json_normalize

pd.json_normalize(dados_churn['telefone']).head()

with open('dataset-telecon.json') as f:
    json_bruto = json.load(f)
json_bruto
# utilizando o método with open(''), passando o nome do arquivo dataset-telecon.json, e, em seguida, criamos uma variável nomeada como f.
# Com uma uma variável chamada json_bruto para armazenar nosso JSON original, utilizando o método json.load(f) e passando f, que é o arquivo que está sendo aberto com o método open()


dados_normalizados = pd.json_normalize(json_bruto)
dados_normalizados.head()
# aqui normalizamos todos os dados de uma só vez

dados_normalizados.info()

dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '].head()
# aqui observamos que a coluna 'conta.cobranca.Total' se encontra vazia nas linhas retornadas. Isso torna inviável a conversão de tipo da coluna.

dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '][
    ['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
]
# filtrado as colunas e as relacionando com a coluna 'conta.cobranca.Total' podemos inferir os valores das que estão zeradas

idx = dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '].index
# podemos ver agora todos os índices dos dados retornados acima

dados_normalizados.loc[idx, 'conta.cobranca.Total'] = dados_normalizados.loc[idx, 'conta.cobranca.mensal'] * 24
# para percorrer as linhas e colunas do dataframe utilizamos o .loc[]. Por ser um caso mensal e a coluna 'conta.contrato está por 2 anos multipicamos por 24 meses 

dados_normalizados.loc[idx, 'cliente.tempo_servico'] = 24
# aqui está o valor recebido pela coluna = 24

dados_normalizados.loc[idx] [
    ['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
]
# observação dos dados alterados e inclusos na tabela

dados_normalizados['conta.cobranca.Total'] = dados_normalizados['conta.cobranca.Total'].astype(float)
# podendo agora ser alterado o tipo com o .astype()

dados_normalizados.info()

for col in dados_normalizados.columns:
    print(f"Coluna: {col}")
    print(dados_normalizados[col].unique())
    print("-" * 30)
# aqui podemos observar no retorno o conteúdo único presente em cada coluna

dados_normalizados.query("Churn == ''")
# para informar quais e quantas são as amostras que não apresentam valores na coluna Churn. No total, temos 226 amostras com este problema

dados_sem_vazio = dados_normalizados[dados_normalizados['Churn'] != ''].copy()
# o != estamos dizendo que o '' vazio é diferente da coluna 'Churn'
#.copy() para cria uma cópia 

dados_sem_vazio.reset_index(drop=True, inplace=True)
# o .reset_index() serve para não ter índeces antigos 
# o drop=True que retirará a coluna Index
# o inplace=True que alterará diretamente o dados_sem_vazio

dados_sem_vazio.info()

dados_sem_vazio.duplicated().sum()
#para saber se existe celulas duplicadas .duplicated() e para saber quantas .sum() para somar todas elas

filtro_duplicadas = dados_sem_vazio.duplicated()
# criando uma definição

dados_sem_vazio[filtro_duplicadas]
# para identificar quais são as amostras são duplicadas

dados_sem_vazio.drop_duplicates(inplace=True)
# drop_duplicates() para retirar amostras duplicadas
# e para que faça a remoção (inplace=True)

dados_sem_vazio
# vizualiçao da tabela

dados_sem_vazio.duplicated().sum
# vizualição do somatório das duplicadas, tendo agora um total de 0

dados_sem_vazio.isna()
# para verificar se existem dados vazios .isna() ou seja (is N/A) que significa "é nulo" ou "não está disponível".

dados_sem_vazio.isna().sum()
# contando os vazios da tabela .sum()

dados_sem_vazio.isna().sum().sum()
# contando os vazios totais da tabela .sum().sum()

dados_sem_vazio[dados_sem_vazio.isna().any(axis=1)]
# para saber quantas amostras diferentes possuem dados nulos .isna().any(), passando axis igual à 1 para fazer referência a coluna

filtro = dados_sem_vazio['cliente.tempo_servico'].isna()
# foi criado uma definição para verificar quais amostras tem nulos na coluna "cliente.tempo_servico"

dados_sem_vazio[filtro][['cliente.tempo_servico','conta.cobranca.mensal','conta.cobranca.Total']]
# selecionando as três colunas que se interligam

import numpy as np 
np.ceil(5957.90/90.45)
#usando o método np.ceil() para realizar a divisão

dados_sem_vazio['cliente.tempo_servico'].fillna(
    np.ceil
        (dados_sem_vazio['conta.cobranca.Total'] / dados_sem_vazio['conta.cobranca.mensal']
    ), inplace=True
)
# para aplicar em toda a coluna a divisão feita com np.ceil usamos o inplace=True depois de ter selecionados as colunas desejadas

dados_sem_vazio[filtro][['cliente.tempo_servico','conta.cobranca.mensal','conta.cobranca.Total']]
# vizualizar tabela

dados_sem_vazio.isna().sum()
# somar vazios 

dados_sem_vazio['conta.contrato'].value_counts()

colunas_dropar = ['conta.contrato', 'conta.faturamente_eletronico', 'conta.metodo_pagamento']

dados_sem_vazio[colunas_dropar].isna().any(axis=1).sum()

df_sem_nulos = dados_sem_vazio.dropna(subset=colunas_dropar).copy()
df_sem_nulos.head()

df_sem_nulos.reset_index(drop=True, inplace=True)

df_sem_nulos.isna().sum()



# %%