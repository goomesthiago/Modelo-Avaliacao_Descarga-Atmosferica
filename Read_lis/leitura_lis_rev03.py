# REV_01 - GUARDA EM UM VETOR TODAS AS VARIAVEIS
# REV_02 - ARMAZENA OS VALORES EXTREMOS DAS VARIAVEIS SOLICITADAS

import os
import numpy as np
import pandas as pd

diretorio = os. getcwd()
arquivos = os.listdir(diretorio)

resultados = open(diretorio + '\\resultados.txt','w')

# Vetor para armazenar nome das variáveis
variaveis = []
#max = []
#min = []
casos = []
n_var = 0
# Variável para identificar o número de linhas com resultados de saída
linhas_var = 0
# Variável para identificar o número de colunas da última linha
colunas_var = 0
# Maximo absoluto
#maximo = []


for arquivo in arquivos:

    if arquivo.endswith('.lis'):

        # Vetor para armazenar nome das variáveis
#        variaveis = []
        max = []
        min = []
#        casos = []
#        n_var = 0
        # Variável para identificar o número de linhas com resultados de saída
#        linhas_var = 0
        # Variável para identificar o número de colunas da última linha
#        colunas_var = 0
        # Maximo absoluto
        maximo = []

        casos.append(arquivo)
        file_ = open(diretorio + '\\' + arquivo, 'r')
        texto = file_.readlines()
        for linha in texto:

            # Detecta as variáveis monitoradas

            if 'Column headings for the' in linha and len(casos) == 1:

                n_var = int(texto[texto.index(linha)][23:29])
                linhas_var = int(n_var / 10) + 1
                colunas_var = n_var % 10


                i = 1

                while texto[texto.index(linha) + i][0:4] != ' ***':

                    if texto[texto.index(linha) + i][0:7] == '   Step':

                        flag = 1

                        while flag == 1:

                            for linhas in range(linhas_var):

                                if linhas == linhas_var - 1:

                                    for j in range(colunas_var):

                                        variaveis.append(texto[texto.index(linha) + i][23 + j * 11:29 + j * 11] +
                                                         '-' + texto[texto.index(linha) + i + 1][23 + j * 11:29 + j * 11])

                                    flag = 0
                                    i = i + 2

                                else:

                                    for j in range(10):

                                        variaveis.append(texto[texto.index(linha) + i][23 + j * 11:29 + j * 11] +
                                                         '-' + texto[texto.index(linha) + i + 1][23 + j * 11: 29 + j * 11])

                                    i = i + 3
                                    linhas = linhas + 1

                    else:

                        i = i + 1

            if 'Variable maxima :' in linha:

                i = 0

                for linhas in range(linhas_var):

                    if linhas == linhas_var - 1:

                        for j in range(colunas_var):

                            max.append(float(texto[texto.index(linha) + i][19 + j * 11:29 + j * 11]))

                    else:

                        for j in range(10):

                            max.append(float(texto[texto.index(linha) + i][19 + j * 11:29 + j * 11]))

                        i = i + 1

            elif 'Variable minima :' in linha:

                i = 0

                for linhas in range(linhas_var):

                    if linhas == linhas_var - 1:

                        for j in range(colunas_var):

                            min.append(float(texto[texto.index(linha) + i][19 + j * 11:29 + j * 11]))

                    else:

                        for j in range(10):

                            min.append(float(texto[texto.index(linha) + i][19 + j * 11:29 + j * 11]))

                        i = i + 1

        # Pega valor absoluto
        for i in range(len(max)):
            maximo.append(np.max([max[i], np.abs(min[i])]))

        # Criando DataFrames
        if len(casos) == 1:
            resultados = [variaveis,maximo]
            #resultados = pd.DataFrame(resultados)
#            resultados = resultados.set_index('variaveis')
#            resultados = resultados.T
#            print(resultados)

        else:
#            resultados_new = pd.Series(maximo)
#            resultados_new = pd.DataFrame(resultados_new)
#            resultados_new = resultados_new.set_index('variaveis')
            #resultados.insert(len(casos), str(arquivo), maximo, allow_duplicates=False)
            resultados.append(maximo)
            print(resultados)

        file_.close()

#resultados.to_excel('Resultados_.xlsx')

## mandar pra função o número de caasos através de len(valores_formatados)