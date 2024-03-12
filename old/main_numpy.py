# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 09:35:58 2024

@author: thiag
"""
import time
import funcoes
import pandas as pd
import numpy as np

start = time.time()

# Chama o arquivo .log onde estão as variáveis que serão utilizadas
nome_do_arquivo = 'exemplo.log'

# Chama a função de extração dos conjuntos de variáveis que estão no .log e combina tudo numa lista de listas
listas_variaveis = funcoes.log_para_variaveis(nome_do_arquivo)


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

# Caminho completo do arquivo atp que será executado
working_dir = 'C:\\ATP\\atpdraw\\work\\VAO_01_estocastico.atp'

# Caminho completo do .lis

lis_working_dir = 'C:\\ATP\\atpdraw\\work\\'

# Inicializa a variável que vai receber os resultados do .lis

df = []



def process_data(valores_formatados, funcoes, working_dir, prefixo_a_procurar, lis_working_dir):
    data_list = []

    for i, val in enumerate(valores_formatados):
        amplitude, A1, _, T_frente, TSTOP = val
        T1 = '   75.0E-6'

        nova_linha_completa = f"13RAIO__-1{amplitude}          {T_frente}{A1}{T1}          {TSTOP}"
        funcoes.alterar_linha_em_arquivo(working_dir, prefixo_a_procurar, nova_linha_completa)
        funcoes.rodar_atp(working_dir, i + 1)

        # Append the new data to the list
        data_list.append(funcoes.ler_lis(lis_working_dir, i + 1))

    # Convert list of arrays into a NumPy array
    data_array = np.array(data_list,dtype="object").T  # Transpose if necessary

    # Create a DataFrame from the NumPy array
    df = pd.DataFrame(data_array)

    return df

# Usage
df = process_data(valores_formatados, funcoes, working_dir, prefixo_a_procurar, lis_working_dir)









# # Começa o laço de repetição para rodar todas as instâncias disponíveis no arquivo .log

# for i in range(len(valores_formatados)):
#     # Chama a função para alterar os valores da fonte de corrente formatados no arquivo .atp
#     amplitude = valores_formatados[i][0] #valor da magnitude da fonte de corrente
#     A1 = valores_formatados[i][1]    #valor da magnitude/2 da fonte de corrente
#     T_frente = valores_formatados[i][3] #valor do tempo de frente da fonte de corrente
#     T1 = '   75.0E-6'   #valor do tempo em que atinge A1
#     TSTOP = valores_formatados[i][4]  #valor do tempo em que a magnitude da fonte de corrente vai a 0
#     nova_linha_completa = f"13RAIO__-1{amplitude}          {T_frente}{A1}{T1}          {TSTOP}"
#     funcoes.alterar_linha_em_arquivo(working_dir, prefixo_a_procurar, nova_linha_completa)
#     funcoes.rodar_atp(working_dir, i+1)
#     #print(f'Simulação {i+1} efetuada com sucesso. ')
#     if i == 0:
#         df = pd.DataFrame(funcoes.ler_lis(lis_working_dir, i+1))
#     else:
#         df.insert(i+1, i+1, funcoes.ler_lis(lis_working_dir, i+1), allow_duplicates=False)
    

print(f'{len(valores_formatados)} simulações foram realizadas.')

#df.to_excel('Resultados_.xlsx')

end = time.time()

print(f"O tempo de execução total foi de: {end - start:.2f} segundos ou {(end - start)/60:.2f} minutos.")