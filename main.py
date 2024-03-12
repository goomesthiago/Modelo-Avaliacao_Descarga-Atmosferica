# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 09:35:58 2024

@author: thiag
"""
import time
import funcoes
import pandas as pd
import numpy as np
import os

start = time.time()

# Chama o arquivo .log onde estão as variáveis que serão utilizadas
nome_do_log = input('Digite o nome do arquivo .log contendo as variáveis da fonte de corrente:\n')

# Chama a função de extração dos conjuntos de variáveis que estão no .log e combina tudo numa lista de listas
listas_variaveis = funcoes.log_para_variaveis(nome_do_log)

nome_excel = input('Digite a seguir o nome do arquivo que será gerado ao fim da execução desse programa:\n')

# Inicializa a variável que vai armazenar os valores formatados no modelo que o ATP aceita (no máximo 10 caracteres por número)
valores_formatados = []
# Chama a função de formatar os valores no modelo que o ATP aceita (no máximo 10 caracteres por número)
for i in listas_variaveis:
    
    valores_formatados.append(funcoes.formatar_valores(i))

# # Printar os valores formatados para conferir
# for j, conjunto in enumerate(valores_formatados, start=0):
#     print(f'Conjunto {j+1}: {conjunto}')

# Prefiro para achar a linha que contém as informações da fonte de corrente
prefixo_a_procurar = '13RAIO__-1'


# Caminho completo do .lis

lis_working_dir = 'C:\\ATP\\atpdraw\\work\\'

# Caminho completo do arquivo atp que será executado

nome_ATP = 'Caso_09_estocastico.atp'
working_dir = lis_working_dir + nome_ATP



# Inicializa a variável que vai guardar a lista de resultados após a primeira execucao

listao =[]

# Inicializa a variável que vai receber os resultados do .lis

df = []

# Fazer o primeiro caso na tentativa de agilizar o processo
amplitude = valores_formatados[0][0] #valor da magnitude da fonte de corrente
A1 = valores_formatados[0][1]    #valor da magnitude/2 da fonte de corrente
T_frente = valores_formatados[0][3] #valor do tempo de frente da fonte de corrente
T1 = '   75.0E-6'   #valor do tempo em que atinge A1
TSTOP = valores_formatados[0][4]  #valor do tempo em que a magnitude da fonte de corrente vai a 0
nova_linha_completa = f"13RAIO__-1{amplitude}          {T_frente}{A1}{T1}          {TSTOP}"
funcoes.alterar_linha_em_arquivo(working_dir, prefixo_a_procurar, nova_linha_completa)
funcoes.rodar_atp(working_dir, 1)

caso1 = funcoes.ler_lis(lis_working_dir, 1, nome_ATP)
df = pd.DataFrame(np.array(caso1[1]).reshape(1,-1), columns = caso1['variaveis'] )





# Começa o laço de repetição para rodar todas as instâncias disponíveis no arquivo .log

for i in range(1,len(valores_formatados)):
    # Chama a função para alterar os valores da fonte de corrente formatados no arquivo .atp
    amplitude = valores_formatados[i][0] #valor da magnitude da fonte de corrente
    A1 = valores_formatados[i][1]    #valor da magnitude/2 da fonte de corrente
    T_frente = valores_formatados[i][3] #valor do tempo de frente da fonte de corrente
    T1 = '   75.0E-6'   #valor do tempo em que atinge A1
    TSTOP = valores_formatados[i][4]  #valor do tempo em que a magnitude da fonte de corrente vai a 0
    nova_linha_completa = f"13RAIO__-1{amplitude}          {T_frente}{A1}{T1}          {TSTOP}"
    funcoes.alterar_linha_em_arquivo(working_dir, prefixo_a_procurar, nova_linha_completa)
    funcoes.rodar_atp(working_dir, i+1)
    listao.append(funcoes.ler_lis(lis_working_dir, i+1, nome_ATP))
    #print(f'Simulação {i+1} efetuada com sucesso. ')
    #df.insert(i+1, i+1, funcoes.ler_lis(lis_working_dir, i+1), allow_duplicates=False)

#df.insert(2, 2, listao, allow_duplicates=False)
tmp = pd.DataFrame(listao,columns = df.columns)
final = pd.concat([df,tmp], ignore_index=True)
print(f'{len(valores_formatados)} simulações foram realizadas.\n\n')

final.to_excel(nome_excel + '.xlsx')

end = time.time()

print(f"O tempo de execução total foi de: {end - start:.2f} segundos ou {(end - start)/60:.2f} minutos.\n\n\n\n")


pasta_destino = 'FIGURAS_' + nome_ATP
if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)


analises = funcoes.le_resultados(nome_do_log, nome_excel + '.xlsx',pasta_destino)

funcoes.plota_individual(analises, pasta_destino)



