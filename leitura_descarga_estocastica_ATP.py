# Arquivo para ler saídas das simulações paramétricas no ATP
# Arquivo adequado para as simulações de ferroressonância

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def le_resultados():

    diretorio = 0

    variaveis = {'KNT': [], 'RAIO': [], 'TFRENT': []}
    #variaveis = {'KNT': [], 'RAIO': []}

    while diretorio == 0:
        try:
            leitura = input('Digite o diretório do arquivo .log contendo os valores dos parâmetros adotados em cada'
                            'simulação, com seu nome e sua extensão \n'
                            'por exemplo: C:/Users/Matheus/Desktop/meuarquivo.log: \n')
            arquivo = open(leitura, 'r', encoding='utf8')
        except:
            print('Há algo errado com o diretorio ou arquivo informados, verifique.')
        else:
            arquivo.close
            diretorio = 1

    with open(leitura, 'r', encoding='ISO-8859-2') as arquivo:
        texto = arquivo.readlines()

        for linha in texto:

            if 'KNT' in linha:
                variaveis['KNT'].append(float(linha.replace('Variables KNT=', '').replace(':', '')))

            elif 'RAIO' in linha:
                variaveis['RAIO'].append(float(linha.replace('RAIO=', '')))

            elif 'TFRENT' in linha:
                variaveis['TFRENT'].append(float(linha.replace('TFRENT=', '')))

#    return variaveis

    #variaveis = le_resultados()

    plt.subplot(1,3,1)
    plt.title('Amplitudes')
    plt.xlabel('Corrente (A)')
    plt.ylabel('Frequência')
    plt.hist(variaveis['RAIO'], rwidth=0.9)
    plt.subplot(1,3,2)
    plt.title('Tempos de frente')
    plt.xlabel('Tempo de frente (s)')
    plt.ylabel('Frequência')
    plt.hist(variaveis['TFRENT'], rwidth=0.9)
    plt.subplot(1,3,3)
    plt.title('Correntes versus tempo de frente')
    plt.xlabel('Tempo de frente (s)')
    plt.ylabel('Amplitude (A)')
    plt.scatter(variaveis['TFRENT'], variaveis['RAIO'])

    plt.show()


    # Leitura das saídas do ATP, coladas em uma planilha excel
    diretorio = 0

    while diretorio == 0:
        try:
            leitura = input(
                 'Digite o diretório do arquivo excel contendo as saídas do ATP com seu nome e sua extensão \n'
                 'por exemplo: C:/Users/Matheus/Desktop/meuarquivo.xlsx: \n')
            resultados = pd.read_excel(leitura, engine='openpyxl')

        except:
            print('Há algo errado com o diretorio ou arquivo informados, verifique.')
        else:
            diretorio = 1

    var = pd.DataFrame(variaveis)

    analises = pd.concat([var, resultados], axis=1)

    return analises

#variaveis = le_resultados()

#print(variaveis)

analises = le_resultados()

#print(analises)

def plota_individual(analise):

    plt.figure()
    #plt.subplot(1, 2, 1)
    count, bins_count = np.histogram(analise['Transição (Vão 1) (kV)'], bins=1000)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 1 (kV)')
    count, bins_count = np.histogram(analise['Transição (Vão 2) (kV)'], bins=1000)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 2 (kV)')
    count, bins_count = np.histogram(analise['Transição (Vão 3) (kV)'], bins=1000)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 3 (kV)')
    plt.ylabel('Prob. (%)')
    plt.yticks([0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel('V (kV)')
    plt.xticks([0, 50, 100, 150, 200])
    plt.xlim([0, 200])
    plt.grid(True)
    plt.title(f"Probabilidade de determinada tensão ser excedida ({len(analise['KNT'])} simulações)")
    plt.legend()

    plt.figure()
    plt.subplot(1, 2)
    plt.hist(analises['Transição (Vão 1) (kV)'], rwidth=0.9, bins=20)
    plt.title('Vão 1 - Transição (Cobertura)')
    plt.xlabel('Amplitudes (kV)')
    plt.ylabel('Frequência')
    plt.subplot(1, 3, 2)
    plt.hist(analises['Transição (Vão 2) (kV)'], rwidth=0.9, bins=20)
    plt.title('Vão 2 - Transição (Cobertura)')
    plt.xlabel('Amplitudes (kV)')
    plt.ylabel('Frequência')
    plt.subplot(1, 3, 3)
    plt.hist(analises['Transição (Vão 3) (kV)'], rwidth=0.9, bins=20)
    plt.title('Vão 3 - Transição (Cobertura)')
    plt.xlabel('Amplitudes (kV)')
    plt.ylabel('Frequência')
    plt.show()

    plt.figure()
    # plt.subplot(1, 2, 1)
    count, bins_count = np.histogram(analise['B11 (Vão 1) (kV)'], bins=1000)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 1 (kV)')
    count, bins_count = np.histogram(analise['B11 (Vão 2) (kV)'], bins=1000)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 2 (kV)')
    count, bins_count = np.histogram(analise['B11 (Vão 3) (kV)'], bins=1000)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 3 (kV)')
    plt.ylabel('Prob. (%)')
    plt.yticks([0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel('V (kV)')
    plt.xticks([0, 50, 100, 150, 200])
    plt.xlim([0, 200])
    plt.grid(True)
    plt.title(f"Probabilidade de determinada tensão ser excedida ({len(analise['KNT'])} simulações)")
    plt.legend()

    plt.figure()
    plt.subplot(1, 3, 1)
    plt.hist(analises['B11 (Vão 1) (kV)'], rwidth=0.9, bins=20)
    plt.title('Vão 1 - B11')
    plt.xlabel('Amplitudes (kV)')
    plt.ylabel('Frequência')
    plt.subplot(1, 3, 2)
    plt.hist(analises['B11 (Vão 2) (kV)'], rwidth=0.9, bins=20)
    plt.title('Vão 2 - B11')
    plt.xlabel('Amplitudes (kV)')
    plt.ylabel('Frequência')
    plt.subplot(1, 3, 3)
    plt.hist(analises['B11 (Vão 3) (kV)'], rwidth=0.9, bins=20)
    plt.title('Vão 3 - B11')
    plt.xlabel('Amplitudes (kV)')
    plt.ylabel('Frequência')
    plt.show()

    plt.figure()
    # plt.subplot(1, 2, 1)
    count, bins_count = np.histogram(analise['N_Transição (Vão 1) (kV)'], bins=1000)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 1 (kV)')
    count, bins_count = np.histogram(analise['N_Transição (Vão 2) (kV)'], bins=1000)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 2 (kV)')
    count, bins_count = np.histogram(analise['N_Transição (Vão 3) (kV)'], bins=1000)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 3 (kV)')
    plt.ylabel('Prob. (%)')
    plt.yticks([0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel('V (kV)')
    plt.xticks([0, 100, 300, 500, 700, 900])
    plt.xlim([0, 900])
    plt.grid(True)
    plt.title(f"Probabilidade de determinada tensão ser excedida ({len(analise['KNT'])} simulações)")
    plt.legend()

    plt.figure()
    plt.subplot(1, 3, 1)
    plt.hist(analises['N_Transição (Vão 1) (kV)'], rwidth=0.9, bins=20)
    plt.title('Vão 1 - Transição (XLPE)')
    plt.xlabel('Amplitudes (kV)')
    plt.ylabel('Frequência')
    plt.subplot(1, 3, 2)
    plt.hist(analises['N_Transição (Vão 2) (kV)'], rwidth=0.9, bins=20)
    plt.title('Vão 2 - Transição (XLPE)')
    plt.xlabel('Amplitudes (kV)')
    plt.ylabel('Frequência')
    plt.subplot(1, 3, 3)
    plt.hist(analises['N_Transição (Vão 3) (kV)'], rwidth=0.9, bins=20)
    plt.title('Vão 3 - Transição (XLPE)')
    plt.xlabel('Amplitudes (kV)')
    plt.ylabel('Frequência')
    plt.show()

plota_individual(analises)

#
#
# # 2) Comparações entre modelos iguais variando o comprimento
#
# plt.figure()
# plt.subplot(1, 3, 1)
# count, bins_count = np.histogram(lt_25km['R_60'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 25 km')
# count, bins_count = np.histogram(lt_50km['R_60'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 50 km')
# count, bins_count = np.histogram(lt_75km['R_60'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 75 km')
# count, bins_count = np.histogram(lt_100km['R_60'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 100 km')
# count, bins_count = np.histogram(lt_125km['R_60'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 125 km')
# count, bins_count = np.histogram(lt_150km['R_60'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 150 km')
# count, bins_count = np.histogram(lt_175km['R_60'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 175 km')
# count, bins_count = np.histogram(lt_200km['R_60'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 200 km')
# plt.ylabel('Prob. (%)')
# plt.yticks([0, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
# plt.xlabel('V (p.u.)')
# plt.grid(True)
# plt.title('Bergeron 60 Hz')
# plt.legend()
#
# plt.subplot(1, 3, 2)
# count, bins_count = np.histogram(lt_25km['R_FN'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 25 km')
# count, bins_count = np.histogram(lt_50km['R_FN'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 50 km')
# count, bins_count = np.histogram(lt_75km['R_FN'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 75 km')
# count, bins_count = np.histogram(lt_100km['R_FN'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 100 km')
# count, bins_count = np.histogram(lt_125km['R_FN'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 125 km')
# count, bins_count = np.histogram(lt_150km['R_FN'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 150 km')
# count, bins_count = np.histogram(lt_175km['R_FN'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 175 km')
# count, bins_count = np.histogram(lt_200km['R_FN'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 200 km')
# plt.ylabel('Prob. (%)')
# plt.yticks([0, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
# plt.xlabel('V (p.u.)')
# plt.grid(True)
# plt.title('Bergeron fn')
# plt.legend()
#
# plt.subplot(1, 3, 3)
# count, bins_count = np.histogram(lt_25km['R_JM'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 25 km')
# count, bins_count = np.histogram(lt_50km['R_JM'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 50 km')
# count, bins_count = np.histogram(lt_75km['R_JM'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 75 km')
# count, bins_count = np.histogram(lt_100km['R_JM'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 100 km')
# count, bins_count = np.histogram(lt_125km['R_JM'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 125 km')
# count, bins_count = np.histogram(lt_150km['R_JM'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 150 km')
# count, bins_count = np.histogram(lt_175km['R_JM'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 175 km')
# count, bins_count = np.histogram(lt_200km['R_JM'] / vb_res, bins=20)
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Term. aberto 200 km')
# plt.ylabel('Prob. (%)')
# plt.yticks([0, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
# plt.xlabel('V (p.u.)')
# plt.grid(True)
# plt.title('JMarti')
# plt.legend()
#
# plt.show()
