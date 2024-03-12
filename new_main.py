# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 09:35:58 2024

@author: thiag
"""
import time
import new_funcoes
import pandas as pd
import numpy as np

start = time.time()

# Chama o arquivo .log onde estão as variáveis que serão utilizadas
nome_do_arquivo = 'exemplo.log'

# Chama a função de extração dos conjuntos de variáveis que estão no .log e combina tudo numa lista de listas
listas_variaveis = new_funcoes.log_para_variaveis(nome_do_arquivo)


# Inicializa a variável que vai armazenar os valores formatados no modelo que o ATP aceita (no máximo 10 caracteres por número)
valores_formatados = []
# Chama a função de formatar os valores no modelo que o ATP aceita (no máximo 10 caracteres por número)
for i in listas_variaveis:
    
    valores_formatados.append(new_funcoes.formatar_valores(i))

# # Printar os valores formatados para conferir
# for j, conjunto in enumerate(valores_formatados, start=0):
#     print(f'Conjunto {j+1}: {conjunto}')

# Prefiro para achar a linha que contém as informações da fonte de corrente
prefixo_a_procurar = '13RAIO__-1'

# Caminho completo do arquivo atp que será executado
working_dir = 'C:\\ATP\\atpdraw\\work\\VAO_01_estocastico.atp'

# Caminho completo do .lis

lis_working_dir = 'C:\\ATP\\atpdraw\\work\\'

# Inicializa a variável que vai guardar a lista de resultados após a primeira execucao

listao =[]

# Inicializa a variável que vai receber os resultados do .lis

df = []

# Lista do cabeçalho
cabecalho = ['variaveis'] + list(np.arange(len(valores_formatados)))

# Fazer o primeiro caso na tentativa de agilizar o processo
amplitude = valores_formatados[0][0] #valor da magnitude da fonte de corrente
A1 = valores_formatados[0][1]    #valor da magnitude/2 da fonte de corrente
T_frente = valores_formatados[0][3] #valor do tempo de frente da fonte de corrente
T1 = '   75.0E-6'   #valor do tempo em que atinge A1
TSTOP = valores_formatados[0][4]  #valor do tempo em que a magnitude da fonte de corrente vai a 0
nova_linha_completa = f"13RAIO__-1{amplitude}          {T_frente}{A1}{T1}          {TSTOP}"
new_funcoes.alterar_linha_em_arquivo(working_dir, prefixo_a_procurar, nova_linha_completa)
new_funcoes.rodar_atp(working_dir, 1)
#df = pd.DataFrame(new_funcoes.ler_lis(lis_working_dir, 1))

listao.append(new_funcoes.ler_lis(lis_working_dir, 1))




# Começa o laço de repetição para rodar todas as instâncias disponíveis no arquivo .log

for i in range(1,len(valores_formatados)):
    # Chama a função para alterar os valores da fonte de corrente formatados no arquivo .atp
    amplitude = valores_formatados[i][0] #valor da magnitude da fonte de corrente
    A1 = valores_formatados[i][1]    #valor da magnitude/2 da fonte de corrente
    T_frente = valores_formatados[i][3] #valor do tempo de frente da fonte de corrente
    T1 = '   75.0E-6'   #valor do tempo em que atinge A1
    TSTOP = valores_formatados[i][4]  #valor do tempo em que a magnitude da fonte de corrente vai a 0
    nova_linha_completa = f"13RAIO__-1{amplitude}          {T_frente}{A1}{T1}          {TSTOP}"
    new_funcoes.alterar_linha_em_arquivo(working_dir, prefixo_a_procurar, nova_linha_completa)
    new_funcoes.rodar_atp(working_dir, i+1)
    listao.append(new_funcoes.ler_lis(lis_working_dir, i+1))
    #print(f'Simulação {i+1} efetuada com sucesso. ')
    #df.insert(i+1, i+1, new_funcoes.ler_lis(lis_working_dir, i+1), allow_duplicates=False)

df = pd.DataFrame(listao)
df = df.T
    
print(f'{len(valores_formatados)} simulações foram realizadas.\n\n')

#df.to_excel('Resultados_.xlsx')

end = time.time()

print(f"O tempo de execução total foi de: {end - start:.2f} segundos ou {(end - start)/60:.2f} minutos.\n\n\n\n")