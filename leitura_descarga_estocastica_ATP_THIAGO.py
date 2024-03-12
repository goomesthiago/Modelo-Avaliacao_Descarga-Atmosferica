# Arquivo para ler saídas das simulações paramétricas no ATP
# Arquivo adequado para as simulações de ferroressonância

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os



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
# Até aqui é a figura, com 3 gráficos, que vai falar sobre as fontes de correntes que usamos para modelar as descargas


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

def plota_individual(analise, pasta_destino):
    

    for i in range(4,len(analise.columns)-1):
    #for i in range(4,len(analise.columns)):
        nome_coluna = analise.columns[i]
        valor_coluna = analise[nome_coluna] / 1000
        
        #conduzindo os valores dos ticks para os múltiplos de 500
        maximo_valor = valor_coluna.max()
        proximo_tick = int(((maximo_valor // 500) + 1) * 500)
        ticks_personalizados = list(range(0, proximo_tick + 1, 500))
        
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,4))
        
        
        #Histograma primeiro subplot
        ax1.hist(valor_coluna, rwidth = 0.9, bins = 20)
        ax1.set_title(nome_coluna)
        ax1.set_xlabel('Amplitudes (kV)')
        ax1.set_ylabel('Frequência')
        
        #CDF no segundo subplot
        count, bins_count = np.histogram(valor_coluna, bins=1000)
        pdf = count / sum(count)
        cdf = np.cumsum(pdf)
        ax2.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: ' + nome_coluna + '(kV)')
        ax2.set_ylabel('Prob. (%)')
        ax2.set_yticks([0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        ax2.set_xlabel('V (kV)')
        ax2.set_xticks(ticks_personalizados)
        ax2.set_xlim([0, proximo_tick])
        ax2.grid(True)
        ax2.set_title(f"Probabilidade de determinada tensão ser excedida ({len(analise['KNT'])} simulações)")
        ax2.legend()
            
        
        # Salvar a fig
        nome_fig = f'CDF_{nome_coluna}.png'
        caminho_figura = os.path.join(pasta_destino, nome_fig)
        plt.savefig(caminho_figura)
        plt.close() # Fechando a figura
           
    

    
    
    # # count, bins_count = np.histogram(analise['Transição (Vão 2) (kV)'], bins=1000)
    # # pdf = count / sum(count)
    # # cdf = np.cumsum(pdf)
    # # plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 2 (kV)')
    # # count, bins_count = np.histogram(analise['Transição (Vão 3) (kV)'], bins=1000)
    # # pdf = count / sum(count)
    # # cdf = np.cumsum(pdf)
    # # plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 3 (kV)')
    
    


    # plt.figure()
    # plt.subplot(1, 3, 1)
    # plt.hist(analises['V___TA-'], rwidth=0.9, bins=20)
    # plt.title('Vão 1 - Transição (Cobertura)')
    # plt.xlabel('Amplitudes (kV)')
    # plt.ylabel('Frequência')
    # plt.subplot(1, 3, 2)
    
    
    
    # # plt.hist(analises['Transição (Vão 2) (kV)'], rwidth=0.9, bins=20)
    # # plt.title('Vão 2 - Transição (Cobertura)')
    # # plt.xlabel('Amplitudes (kV)')
    # # plt.ylabel('Frequência')
    # # plt.subplot(1, 3, 3)
    # # plt.hist(analises['Transição (Vão 3) (kV)'], rwidth=0.9, bins=20)
    # # plt.title('Vão 3 - Transição (Cobertura)')
    # # plt.xlabel('Amplitudes (kV)')
    # # plt.ylabel('Frequência')
    # # plt.show()




    # # plt.figure()
    # # # plt.subplot(1, 2, 1)
    # # count, bins_count = np.histogram(analise['N_Transição (Vão 1) (kV)'], bins=1000)
    # # pdf = count / sum(count)
    # # cdf = np.cumsum(pdf)
    # # plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 1 (kV)')
    # # count, bins_count = np.histogram(analise['N_Transição (Vão 2) (kV)'], bins=1000)
    # # pdf = count / sum(count)
    # # cdf = np.cumsum(pdf)
    # # plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 2 (kV)')
    # # count, bins_count = np.histogram(analise['N_Transição (Vão 3) (kV)'], bins=1000)
    # # pdf = count / sum(count)
    # # cdf = np.cumsum(pdf)
    # # plt.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: Vão 3 (kV)')
    # # plt.ylabel('Prob. (%)')
    # # plt.yticks([0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    # # plt.xlabel('V (kV)')
    # # plt.xticks([0, 100, 300, 500, 700, 900])
    # # plt.xlim([0, 900])
    # # plt.grid(True)
    # # plt.title(f"Probabilidade de determinada tensão ser excedida ({len(analise['KNT'])} simulações)")
    # # plt.legend()


pasta_destino = 'FIGURAS'
if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

plota_individual(analises, pasta_destino)
# tmp = plota_individual(analises.iloc[:,4])